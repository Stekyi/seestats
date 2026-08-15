# TradeOps Weekly Pipeline Runner
# Registered in Windows Task Scheduler — runs every Monday at 8:00 AM
# To run manually: .\run_tradeops.ps1

$ScriptDir = "D:\clawing\tradeops"
$PythonScript = "$ScriptDir\scripts\run_pipeline.py"
$LogFile = "$ScriptDir\logs\scheduler.log"

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $LogFile -Value "[$timestamp] Task Scheduler triggered pipeline run"

Set-Location $ScriptDir
python $PythonScript
$exitCode = $LASTEXITCODE

$timestamp2 = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $LogFile -Value "[$timestamp2] Pipeline finished with exit code $exitCode"
