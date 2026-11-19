"""Offline transport tests: every socket/HTTP operation is mocked."""
import importlib.util
import json
from pathlib import Path
import socket
import ssl
import unittest
from unittest import mock
import urllib.request

spec = importlib.util.spec_from_file_location('public_source_transport_test_module', Path(__file__).resolve().parents[1] / 'scripts/public_source_transport.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def answer(*addresses):
    return {'Status': 0, 'Answer': [{'type': 5, 'data': 'public-cname.example'}] +
            [{'type': 1, 'data': address} for address in addresses]}


class ResolverTests(unittest.TestCase):
    def resolve(self, payload=None, *, raw=None, url=None, timeout=30):
        response = mock.MagicMock()
        response.geturl.return_value = module.RESOLVER_URL if url is None else url
        response.read.return_value = json.dumps(payload).encode('utf-8') if raw is None else raw
        opener = mock.Mock()
        opener.open.return_value.__enter__ = mock.Mock(return_value=response)
        opener.open.return_value.__exit__ = mock.Mock(return_value=False)
        with mock.patch.object(module.urllib.request, 'build_opener', return_value=opener) as build:
            result = module.resolve_public_ipv4(timeout)
        return result, response, opener, build

    def test_public_a_only_deduplicated_and_max_three_addresses(self):
        payload = answer('8.8.8.8', '1.1.1.1', '8.8.8.8', '9.9.9.9', '208.67.222.222')
        payload['Answer'].append({'type': 28, 'data': '2606:4700:4700::1111'})
        result, response, opener, build = self.resolve(payload)
        self.assertEqual(result, ['8.8.8.8', '1.1.1.1', '9.9.9.9'])
        self.assertEqual(response.read.call_args.args, (module.MAX_DNS_BYTES + 1,))
        opener.open.assert_called_once()
        request = opener.open.call_args.args[0]
        self.assertEqual(request.full_url, module.RESOLVER_URL)
        self.assertEqual(request.get_method(), 'GET')
        self.assertFalse(request.has_header('Authorization'))
        self.assertFalse(request.has_header('Cookie'))
        self.assertEqual(opener.open.call_args.kwargs['timeout'], 10)
        handlers = build.call_args.args
        self.assertIsInstance(handlers[0], module._RejectResolverRedirects)
        self.assertIsInstance(handlers[1], urllib.request.HTTPSHandler)
        self.assertNotIsInstance(handlers[1], module.DailyHTTPSHandler)
        self.assertTrue(handlers[1]._context.check_hostname)
        self.assertEqual(handlers[1]._context.verify_mode, ssl.CERT_REQUIRED)

    def test_finite_resolver_timeout_preserves_shorter_caller_timeout(self):
        for supplied, expected in ((2, 2), (float('inf'), 10), (float('nan'), 10), (None, 10), (-1, 10)):
            with self.subTest(timeout=supplied):
                _, _, opener, _ = self.resolve(answer('8.8.8.8'), timeout=supplied)
                self.assertEqual(opener.open.call_args.kwargs['timeout'], expected)

    def test_unsuccessful_or_missing_status_is_rejected(self):
        for payload in ({'Status': 3}, {'Status': False}, {'Status': '0'}, {}, []):
            with self.subTest(payload=payload), self.assertRaises(module.DNSFallbackError):
                self.resolve(payload)

    def test_nonpublic_and_non_ipv4_a_records_are_rejected(self):
        for address in ('127.0.0.1', '10.0.0.1', '172.16.0.1', '192.168.1.1', '169.254.169.254',
                        '0.0.0.0', '240.0.0.1', '224.0.0.1', '192.0.2.1', '100.64.0.1', '::1', 'not-an-ip'):
            with self.subTest(address=address), self.assertRaises(module.DNSFallbackError):
                self.resolve(answer(address))

    def test_invalid_later_answer_cannot_hide_behind_limit(self):
        with self.assertRaises(module.DNSFallbackError):
            self.resolve(answer('8.8.8.8', '1.1.1.1', '9.9.9.9', '127.0.0.1'))

    def test_empty_and_malformed_answer_lists_rejected(self):
        for records in (None, [], {}, ['invalid'], [{'type': 1}], [{'type': 1, 'data': 123}], [{'type': 5, 'data': 'cname'}]):
            with self.subTest(records=records), self.assertRaises(module.DNSFallbackError):
                self.resolve({'Status': 0, 'Answer': records})

    def test_oversized_and_invalid_json_rejected(self):
        for raw in (b'x' * (module.MAX_DNS_BYTES + 1), b'<html>not json</html>', b'\xff'):
            with self.subTest(size=len(raw)), self.assertRaises(module.DNSFallbackError):
                self.resolve(raw=raw)

    def test_response_url_mismatch_rejected(self):
        for url in ('https://other.example/resolve', 'http://dns.alidns.com/resolve', module.RESOLVER_URL + '&extra=1'):
            with self.subTest(url=url), self.assertRaises(module.DNSFallbackError):
                self.resolve(answer('8.8.8.8'), url=url)

    def test_all_resolver_redirects_are_rejected(self):
        handler = module._RejectResolverRedirects()
        request = urllib.request.Request(module.RESOLVER_URL)
        for destination in ('https://other.example/', module.RESOLVER_URL):
            with self.subTest(destination=destination), self.assertRaises(module.DNSFallbackError):
                handler.redirect_request(request, None, 302, 'redirect', {}, destination)


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.context = ssl.create_default_context()
        self.connection = module.DailyHTTPSConnection(module.API_HOST, context=self.context)
        self.addCleanup(self.connection.close)

    def test_normal_dns_success_has_no_fallback(self):
        sock = mock.Mock()
        with mock.patch.object(module.socket, 'create_connection', return_value=sock) as connect, \
                mock.patch.object(module, 'resolve_public_ipv4') as resolve:
            self.assertIs(self.connection._create_connection((module.API_HOST, 443), 30, None), sock)
        connect.assert_called_once_with((module.API_HOST, 443), 30, None)
        resolve.assert_not_called()
        self.assertEqual(self.connection.host, module.API_HOST)
        self.assertIs(self.connection._context, self.context)

    def test_dns_failure_routes_tcp_but_keeps_tls_sni_and_host_header(self):
        tcp, tls = mock.Mock(), mock.Mock()
        with mock.patch.object(module.socket, 'create_connection', side_effect=[socket.gaierror(11001, 'DNS error'), tcp]) as connect, \
                mock.patch.object(module, 'resolve_public_ipv4', return_value=['8.8.8.8']) as resolve, \
                mock.patch.object(self.context, 'wrap_socket', return_value=tls) as wrap, \
                mock.patch.object(module.sys, 'stderr'):
            self.connection.connect()
            self.connection.putrequest('GET', '/api/4/news/latest')
        self.assertEqual(connect.call_args_list[0].args[0], (module.API_HOST, 443))
        self.assertEqual(connect.call_args_list[1].args[0], ('8.8.8.8', 443))
        resolve.assert_called_once()
        wrap.assert_called_once_with(tcp, server_hostname=module.API_HOST)
        self.assertEqual(self.connection.host, module.API_HOST)
        self.assertIn(b'Host: news-at.zhihu.com', self.connection._buffer)
        self.assertIs(self.connection._context, self.context)
        self.assertTrue(self.context.check_hostname)
        self.assertEqual(self.context.verify_mode, ssl.CERT_REQUIRED)

    def test_proxy_and_other_addresses_never_use_fallback(self):
        for address in (('proxy.example', 443), ('127.0.0.1', 8080), ('other.example', 443), (module.API_HOST, 80)):
            original = socket.gaierror(11001, 'DNS error')
            with self.subTest(address=address), \
                    mock.patch.object(module.socket, 'create_connection', side_effect=original), \
                    mock.patch.object(module, 'resolve_public_ipv4') as resolve:
                with self.assertRaises(socket.gaierror) as caught:
                    self.connection._create_connection(address, 30, None)
                self.assertIs(caught.exception, original)
                resolve.assert_not_called()

    def test_nondns_network_error_never_uses_fallback(self):
        with mock.patch.object(module.socket, 'create_connection', side_effect=TimeoutError('timeout')), \
                mock.patch.object(module, 'resolve_public_ipv4') as resolve:
            with self.assertRaises(TimeoutError):
                self.connection._create_connection((module.API_HOST, 443), 30, None)
        resolve.assert_not_called()

    def test_all_candidate_failures_are_finite_and_preserve_source_address(self):
        source = ('0.0.0.0', 0)
        errors = [socket.gaierror(11001, 'DNS'), OSError('first'), OSError('second'), OSError('third')]
        with mock.patch.object(module.socket, 'create_connection', side_effect=errors) as connect, \
                mock.patch.object(module, 'resolve_public_ipv4', return_value=['8.8.8.8', '1.1.1.1', '9.9.9.9', '208.67.222.222']) as resolve:
            with self.assertRaisesRegex(OSError, 'third'):
                self.connection._create_connection((module.API_HOST, 443), 30, source)
        self.assertEqual(connect.call_count, 4)
        self.assertTrue(all(call.args[1:] == (30, source) for call in connect.call_args_list))
        resolve.assert_called_once_with(30)

    def test_second_candidate_can_succeed(self):
        sock = mock.Mock()
        with mock.patch.object(module.socket, 'create_connection', side_effect=[socket.gaierror(), OSError(), sock]) as connect, \
                mock.patch.object(module, 'resolve_public_ipv4', return_value=['8.8.8.8', '1.1.1.1']), \
                mock.patch.object(module.sys, 'stderr'):
            self.assertIs(self.connection._create_connection((module.API_HOST, 443), 5, None), sock)
        self.assertEqual(connect.call_count, 3)

    def test_context_mutated_to_insecure_is_rejected_before_network(self):
        self.context.check_hostname = False
        with mock.patch.object(module.socket, 'create_connection') as connect:
            with self.assertRaises(ValueError):
                self.connection._create_connection((module.API_HOST, 443), 30, None)
        connect.assert_not_called()


class HandlerTests(unittest.TestCase):
    def test_default_handler_and_connection_contexts_are_verified(self):
        for item in (module.DailyHTTPSHandler(), module.DailyHTTPSConnection(module.API_HOST)):
            self.assertTrue(item._context.check_hostname)
            self.assertEqual(item._context.verify_mode, ssl.CERT_REQUIRED)

    def test_insecure_contexts_and_false_hostname_parameter_are_rejected(self):
        insecure = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        insecure.check_hostname = False
        insecure.verify_mode = ssl.CERT_NONE
        hostname_off = ssl.create_default_context()
        hostname_off.check_hostname = False
        for factory in (module.DailyHTTPSHandler, lambda **kwargs: module.DailyHTTPSConnection(module.API_HOST, **kwargs)):
            for context in (insecure, hostname_off):
                with self.subTest(context=context), self.assertRaises(ValueError):
                    factory(context=context)
            with self.assertRaises(ValueError):
                factory(check_hostname=False)

    def test_handler_passes_original_request_and_context_without_rewriting_host(self):
        context = ssl.create_default_context()
        handler = module.DailyHTTPSHandler(context=context)
        request = urllib.request.Request('https://news-at.zhihu.com/api/4/news/latest')
        with mock.patch.object(handler, 'do_open', return_value='response') as do_open:
            self.assertEqual(handler.https_open(request), 'response')
        do_open.assert_called_once_with(module.DailyHTTPSConnection, request, context=context)
        self.assertEqual(request.host, module.API_HOST)


if __name__ == '__main__':
    unittest.main()
