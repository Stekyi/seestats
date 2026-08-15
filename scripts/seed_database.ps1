param(
  [string]$AdminKey = $env:ADMIN_KEY,
  [string]$ApiBase = $env:SEESTATS_API_BASE
)
if (-not $ApiBase) { throw 'Set SEESTATS_API_BASE, e.g. https://see-stats.pages.dev' }
if (-not $AdminKey) { throw 'Set ADMIN_KEY in the shell before running.' }
$cfg = Get-Content "$PSScriptRoot\..\config\countries.json" -Raw | ConvertFrom-Json
$headers = @{ 'X-Admin-Key'=$AdminKey; 'Content-Type'='application/json' }
Invoke-RestMethod -Method Post -Uri "$ApiBase/api/admin/countries" -Headers $headers -Body ($cfg | ConvertTo-Json -Depth 8)
Write-Host 'Countries synced.' -ForegroundColor Green
