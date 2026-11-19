"""Verified-TLS DNS fallback scoped exclusively to the public Daily API.

A local DNS failure may be retried using fresh AliDNS HTTPS answers. The TCP
address changes, never the HTTPS connection hostname, SNI, Host header or trust
policy. No global opener, resolver changes, persistent cache or fixed IPs.
"""
from __future__ import annotations

import http.client
import ipaddress
import json
import math
import socket
import ssl
import sys
import urllib.request

API_HOST = "news-at.zhihu.com"
RESOLVER_URL = "https://dns.alidns.com/resolve?name=news-at.zhihu.com&type=A"
MAX_DNS_BYTES = 64 * 1024
MAX_IPS = 3
MAX_RESOLVER_TIMEOUT = 10.0


class DNSFallbackError(OSError):
    """The scoped DNS fallback did not yield safe, usable public addresses."""


def verified_context(context: ssl.SSLContext | None = None, *, check_hostname=None) -> ssl.SSLContext:
    if check_hostname is False:
        raise ValueError("HTTPS hostname verification cannot be disabled")
    context = ssl.create_default_context() if context is None else context
    if (not isinstance(context, ssl.SSLContext)
            or context.verify_mode != ssl.CERT_REQUIRED or not context.check_hostname):
        raise ValueError("HTTPS requires CERT_REQUIRED and hostname verification")
    return context


class _RejectResolverRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise DNSFallbackError("DNS resolver redirects are not allowed")


def resolve_public_ipv4(timeout=MAX_RESOLVER_TIMEOUT) -> list[str]:
    """Read one bounded, verified HTTPS JSON response; never follow redirects."""
    if isinstance(timeout, (int, float)) and not isinstance(timeout, bool):
        if not math.isfinite(timeout) or timeout <= 0:
            timeout = MAX_RESOLVER_TIMEOUT
        timeout = min(float(timeout), MAX_RESOLVER_TIMEOUT)
    else:
        timeout = MAX_RESOLVER_TIMEOUT
    # A separate standard opener is deliberate: it cannot recurse into the
    # Daily handler, nor carry Daily request headers/cookies/credentials.
    opener = urllib.request.build_opener(
        _RejectResolverRedirects(), urllib.request.HTTPSHandler(context=verified_context()))
    request = urllib.request.Request(RESOLVER_URL, headers={"Accept": "application/dns-json"}, method="GET")
    with opener.open(request, timeout=timeout) as response:
        if response.geturl() != RESOLVER_URL:
            raise DNSFallbackError("DNS resolver response URL mismatch")
        raw = response.read(MAX_DNS_BYTES + 1)
    if len(raw) > MAX_DNS_BYTES:
        raise DNSFallbackError("DNS resolver response exceeds size limit")
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DNSFallbackError("DNS resolver returned invalid JSON") from exc
    if not isinstance(payload, dict) or type(payload.get("Status")) is not int or payload["Status"] != 0:
        raise DNSFallbackError("DNS resolver returned an unsuccessful status")
    answers = payload.get("Answer")
    if not isinstance(answers, list):
        raise DNSFallbackError("DNS resolver has no answer list")
    addresses = []
    for answer in answers:
        if not isinstance(answer, dict):
            raise DNSFallbackError("Malformed DNS answer")
        if type(answer.get("type")) is not int or answer["type"] != 1:
            continue  # CNAME/AAAA records are not TCP destinations here.
        try:
            data = answer["data"]
            if not isinstance(data, str):
                raise ValueError("A record must be a string")
            address = ipaddress.IPv4Address(data)
        except (KeyError, ValueError) as exc:
            raise DNSFallbackError("Invalid DNS IPv4 A record") from exc
        if (not address.is_global or address.is_private or address.is_loopback
                or address.is_reserved or address.is_multicast or address.is_link_local
                or address.is_unspecified):
            raise DNSFallbackError("DNS A record is not a public unicast IPv4 address")
        canonical = str(address)
        if canonical not in addresses:
            addresses.append(canonical)
    if not addresses:
        raise DNSFallbackError("DNS resolver returned no public IPv4 A records")
    return addresses[:MAX_IPS]


class DailyHTTPSConnection(http.client.HTTPSConnection):
    """Let inherited HTTPSConnection.connect perform original-host TLS and SNI."""
    def __init__(self, host, port=None, *, context=None, check_hostname=None, **kwargs):
        context = verified_context(context, check_hostname=check_hostname)
        super().__init__(host, port=port, context=context, **kwargs)
        # HTTPConnection.connect calls this instance hook for the TCP socket.
        # Do not replace self.host, _tunnel_host, connect(), or wrap_socket().
        self._create_connection = self._daily_create_connection

    def _daily_create_connection(self, address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                                 source_address=None, **kwargs):
        # Recheck because a caller could mutate a previously verified context.
        verified_context(self._context)
        try:
            return socket.create_connection(address, timeout, source_address, **kwargs)
        except socket.gaierror as original:
            if address != (API_HOST, 443):
                raise  # Includes proxy DNS failures; never resolve the API instead.
            addresses = resolve_public_ipv4(timeout)
            last_error = original
            for ip in addresses[:MAX_IPS]:
                try:
                    connection = socket.create_connection((ip, 443), timeout, source_address, **kwargs)
                except OSError as exc:
                    last_error = exc
                    continue
                print(f"[DNS fallback] {API_HOST}:443 via public IPv4 {ip}; original-host TLS verification retained", file=sys.stderr)
                return connection
            raise last_error from original


class DailyHTTPSHandler(urllib.request.HTTPSHandler):
    def __init__(self, debuglevel=0, context=None, check_hostname=None):
        context = verified_context(context, check_hostname=check_hostname)
        super().__init__(debuglevel=debuglevel, context=context)

    def https_open(self, req):
        verified_context(self._context)
        return self.do_open(DailyHTTPSConnection, req, context=self._context)
