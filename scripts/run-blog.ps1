param([Parameter(Mandatory=$true)][string]$NodePath)

$ErrorActionPreference = 'Stop'
$blogRoot = Split-Path -Parent $PSScriptRoot
$blogCli = Join-Path $blogRoot 'node_modules\astro\bin\astro.mjs'
$blogLogs = Join-Path $blogRoot 'artifacts\blog-runs'
New-Item -ItemType Directory -Path $blogLogs -Force | Out-Null
$blogRun = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
$blogEvents = Join-Path $blogLogs "$blogRun-events.log"

function Write-BlogEvent([string]$Message) {
    Add-Content -LiteralPath $blogEvents -Value "$(Get-Date -Format o) $Message" -Encoding UTF8
}

# Only one supervisor may launch this project's development server.
$blogHash = [System.Security.Cryptography.SHA256]::Create()
$blogKey = [BitConverter]::ToString($blogHash.ComputeHash([Text.Encoding]::UTF8.GetBytes($blogRoot))).Replace('-', '')
$blogHash.Dispose()
$blogMutex = New-Object System.Threading.Mutex($false, "Local\ShawBlog-$blogKey")
$blogLocked = $false
try {
    try { $blogLocked = $blogMutex.WaitOne(0) } catch [System.Threading.AbandonedMutexException] { $blogLocked = $true }
    if (-not $blogLocked) { Write-BlogEvent 'Another supervisor is already running.'; exit 0 }
    Write-BlogEvent "Supervisor started. PID=$PID"
    $env:ASTRO_TELEMETRY_DISABLED = '1'
    for ($blogAttempt = 1; $blogAttempt -le 4; $blogAttempt++) {
        if (Get-NetTCPConnection -LocalPort 4321 -State Listen -ErrorAction SilentlyContinue) {
            Write-BlogEvent 'Port 4321 is occupied. Stopped without changing the existing service.'
            exit 1
        }
        $blogOut = Join-Path $blogLogs "$blogRun-attempt-$blogAttempt.log"
        $blogError = Join-Path $blogLogs "$blogRun-attempt-$blogAttempt-error.log"
        $blogChild = Start-Process -FilePath $NodePath -ArgumentList @(
            ('"' + $blogCli + '"'), 'dev', '--host', '127.0.0.1', '--port', '4321'
        ) -WorkingDirectory $blogRoot -WindowStyle Hidden -PassThru `
          -RedirectStandardOutput $blogOut -RedirectStandardError $blogError
        Write-BlogEvent "Server started. Attempt=$blogAttempt PID=$($blogChild.Id) stdout=$blogOut stderr=$blogError"
        # Retain the process handle so Windows PowerShell can read the exit code.
        $null = $blogChild.Handle
        $blogChild.WaitForExit()
        $blogChild.Refresh()
        $blogExitCode = $blogChild.ExitCode
        Write-BlogEvent "Server exited. PID=$($blogChild.Id) ExitCode=$blogExitCode"
        if ($blogExitCode -eq 0) { break }
        if ($blogAttempt -eq 4) { Write-BlogEvent 'Recovery limit reached (3 retries). Double-click the launcher after fixing the error.'; break }
        Write-BlogEvent 'Unexpected exit. Restarting in 5 seconds.'
        Start-Sleep -Seconds 5
    }
} catch {
    Write-BlogEvent "Supervisor failed: $($_.Exception.Message)"
    exit 1
} finally {
    if ($blogLocked) { $blogMutex.ReleaseMutex() }
    $blogMutex.Dispose()
}
