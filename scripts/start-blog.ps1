param([switch]$NoBrowser)

$ErrorActionPreference = 'Stop'
$blogRoot = Split-Path -Parent $PSScriptRoot
$blogUrl = 'http://127.0.0.1:4321/'
$blogCli = Join-Path $blogRoot 'node_modules\astro\bin\astro.mjs'
$blogLogs = Join-Path $blogRoot 'artifacts\blog-runs'

function Test-BlogReady {
    try {
        $response = Invoke-WebRequest -Uri $blogUrl -UseBasicParsing -TimeoutSec 15
        return ($response.StatusCode -eq 200 -and $response.Content -match 'shaw')
    } catch {
        return $false
    }
}

try {
    if (Test-BlogReady) {
        Write-Host "Blog is already running: $blogUrl"
        if (-not $NoBrowser) { Start-Process $blogUrl }
        exit 0
    }
    if (Get-NetTCPConnection -LocalPort 4321 -State Listen -ErrorAction SilentlyContinue) {
        throw 'Port 4321 is occupied by another service. No process was stopped.'
    }
    if (-not (Test-Path -LiteralPath $blogCli)) {
        throw 'Astro dependencies are missing. Run pnpm install in the project folder first.'
    }
    $blogNodeCommand = Get-Command node.exe -ErrorAction SilentlyContinue
    $blogNode = if ($blogNodeCommand) { $blogNodeCommand.Source } else {
        Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
    }
    if (-not (Test-Path -LiteralPath $blogNode)) {
        throw 'Node.js was not found. Install Node.js 24 and try again.'
    }
    New-Item -ItemType Directory -Path $blogLogs -Force | Out-Null
    $blogRun = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
    $blogWorker = Join-Path $PSScriptRoot 'run-blog.ps1'
    $blogProcess = Start-Process -FilePath 'powershell.exe' -ArgumentList @(
        '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ('"' + $blogWorker + '"'),
        '-NodePath', ('"' + $blogNode + '"')
    ) -WorkingDirectory $blogRoot -WindowStyle Hidden -PassThru `
      -RedirectStandardOutput (Join-Path $blogLogs "$blogRun-launcher.log") `
      -RedirectStandardError (Join-Path $blogLogs "$blogRun-launcher-error.log")

    # The first development request can compile pages and dependencies.
    $blogDeadline = (Get-Date).AddSeconds(90)
    do {
        if (Test-BlogReady) {
            Write-Host "Blog started: $blogUrl (PID $($blogProcess.Id))"
            Write-Host 'The server runs in the background. After a reboot, double-click the launcher again.'
            if (-not $NoBrowser) { Start-Process $blogUrl }
            exit 0
        }
        if ($blogProcess.HasExited) {
            throw "The supervisor exited. Check logs in $blogLogs"
        }
        Start-Sleep -Milliseconds 500
    } while ((Get-Date) -lt $blogDeadline)
    throw "The server did not become ready in time. Check logs in $blogLogs"
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
