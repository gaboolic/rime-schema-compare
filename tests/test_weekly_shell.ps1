# Offline integration test: no browser/network/benchmark engine is invoked.
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$caseDir = Join-Path ([System.IO.Path]::GetTempPath()) ('rime-weekly-shell-smoke-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $caseDir -Force | Out-Null
$env:WEEKLY_SYNTAX_DIR = $caseDir
@'
import os
from pathlib import Path
import yaml
w = yaml.load(Path('.github/workflows/weekly-report.yml').read_text(encoding='utf-8'), Loader=yaml.BaseLoader)
out = Path(os.environ['WEEKLY_SYNTAX_DIR'])
for index, step in enumerate(w['jobs']['benchmark']['steps']):
    if 'run' in step:
        (out / f'step-{index}.ps1').write_text(step['run'], encoding='utf-8')
'@ | python -
if ($LASTEXITCODE -ne 0) { throw 'Unable to extract workflow shell blocks' }
foreach ($file in Get-ChildItem $caseDir -Filter '*.ps1') {
    $tokens = $null
    $errors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($file.FullName, [ref]$tokens, [ref]$errors) | Out-Null
    if ($errors.Count) { throw ($errors | Out-String) }
}
function python {
    $position = [array]::IndexOf($args, '--out-dir')
    if ($position -lt 0) { throw 'Benchmark output argument missing' }
    $outputDir = $args[$position + 1]
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    Set-Content (Join-Path $outputDir 'benchmark_fixture_report.txt') 'Offline benchmark fixture summary' -Encoding utf8
    $global:LASTEXITCODE = 0
}
$reportDir = Join-Path $caseDir 'reports'
./scripts/run_test.ps1 -Corpus data/corpus/fixture.txt -ArtifactsDir (Join-Path $caseDir 'results') -ReportDir $reportDir -DateFormat "'2030-01-01'"
if ($LASTEXITCODE -ne 0) { throw "Report script leaked native exit code $LASTEXITCODE" }
if (-not (Test-Path (Join-Path $reportDir '2030-01-01.md'))) { throw 'Explicit date was not used' }
if (-not (Test-Path (Join-Path $reportDir 'latest.md'))) { throw 'Latest staging report missing' }
Write-Output 'PASS: all workflow PowerShell blocks parse; staging report/date/exit-code integration passed'
