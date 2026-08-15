<#
 See Stats Admin Console
 - Maintains country/source configuration.
 - Runs the weekly Python extraction pipeline for enabled countries.
 - Publishes completed report JSON to Cloudflare Pages Functions / D1.
 - Manages subscriber entitlements.

Prerequisites: Python, Node/Wrangler, Git, and environment variables:
  SEESTATS_API_BASE=https://your-pages-domain
  ADMIN_KEY=your-secret
  (RESEND_API_KEY / FROM_EMAIL live in Cloudflare for email delivery)
#>
$ErrorActionPreference='Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigPath = Join-Path $Root 'config\countries.json'
$ApiBase = $env:SEESTATS_API_BASE
$AdminKey = $env:ADMIN_KEY
if (-not $ApiBase) { Write-Host 'SEESTATS_API_BASE is not set.' -ForegroundColor Yellow; $ApiBase = Read-Host 'Cloudflare API base URL' }
if (-not $AdminKey) { $AdminKey = Read-Host 'Cloudflare admin key' }
$Headers = @{'X-Admin-Key'=$AdminKey;'Content-Type'='application/json'}

function Load-Config { return (Get-Content $ConfigPath -Raw | ConvertFrom-Json) }
function Save-Config($cfg) { $cfg | ConvertTo-Json -Depth 12 | Set-Content $ConfigPath -Encoding UTF8 }
function Sync-Countries { $cfg=Load-Config; Invoke-RestMethod -Method Post -Uri "$ApiBase/api/admin/countries" -Headers $Headers -Body (@{countries=$cfg.countries} | ConvertTo-Json -Depth 12) | Out-Null; Write-Host 'Country/source registry synced to Cloudflare.' -ForegroundColor Green }
function Show-Countries { $cfg=Load-Config; $i=0; $cfg.countries | ForEach-Object { Write-Host ("[{0}] {1} ({2}) - {3} - sources: {4}" -f $i,$_.name,$_.code,($(if($_.enabled){'ENABLED'}else{'DISABLED'})),$_.sources.Count); $i++ } }
function Toggle-Country {
  Show-Countries; $n=[int](Read-Host 'Country number'); $cfg=Load-Config; $c=$cfg.countries[$n]; $c.enabled=-not [bool]$c.enabled; Save-Config $cfg; Sync-Countries
  Write-Host "$($c.name): enabled=$($c.enabled)" -ForegroundColor Green
}
function Add-Source {
  Show-Countries; $n=[int](Read-Host 'Country number'); $cfg=Load-Config; $c=$cfg.countries[$n]; $name=Read-Host 'Source name'; $url=Read-Host 'Source URL'; $c.sources += [pscustomobject]@{name=$name;url=$url}; Save-Config $cfg; Sync-Countries; Write-Host 'Source added.' -ForegroundColor Green
}
function Add-Country {
  $cfg=Load-Config; $code=(Read-Host 'ISO 3-letter code').ToUpper(); $name=Read-Host 'Country name'; $cfg.countries += [pscustomobject]@{code=$code;name=$name;enabled=$false;sources=@()}; Save-Config $cfg; Sync-Countries; Write-Host 'Country added as disabled.' -ForegroundColor Green
}

function Show-Features {
  $r=Invoke-RestMethod -Method Get -Uri "$ApiBase/api/admin/features" -Headers $Headers
  Write-Host "`nFeature access policy" -ForegroundColor Cyan
  $i=0; $r.features.PSObject.Properties | Sort-Object Name | ForEach-Object { $f=$_.Value; Write-Host ("[{0}] {1} ({2}) - {3} - {4}" -f $i,$f.label,$f.key,$(if($f.enabled){'ENABLED'}else{'DISABLED'}),$(if($f.subscriberOnly){'SUBSCRIBER ONLY'}else{'FREE'})); $i++ }
}
function Set-FeaturePolicy {
  $r=Invoke-RestMethod -Method Get -Uri "$ApiBase/api/admin/features" -Headers $Headers
  $items=@($r.features.PSObject.Properties | Sort-Object Name); if($items.Count -eq 0){Write-Host 'No feature flags found.' -ForegroundColor Yellow;return}
  $i=0; $items | ForEach-Object { $f=$_.Value; Write-Host ("[{0}] {1} - enabled={2}, subscriberOnly={3}" -f $i,$f.label,$f.enabled,$f.subscriberOnly); $i++ }
  $n=[int](Read-Host 'Feature number'); if($n -lt 0 -or $n -ge $items.Count){throw 'Invalid feature number.'}; $f=$items[$n].Value
  Write-Host "Selected: $($f.label) [$($f.key)]" -ForegroundColor Cyan
  Write-Host '1. Toggle subscriber-only'
  Write-Host '2. Toggle enabled/disabled'
  $action=Read-Host 'Action'
  if($action -eq '1'){$f.subscriberOnly=-not [bool]$f.subscriberOnly}
  elseif($action -eq '2'){$f.enabled=-not [bool]$f.enabled}
  else{Write-Host 'No change.' -ForegroundColor Yellow;return}
  $body=@{feature_key=$f.key;label=$f.label;description=$f.description;enabled=[bool]$f.enabled;subscriber_only=[bool]$f.subscriberOnly}|ConvertTo-Json
  Invoke-RestMethod -Method Post -Uri "$ApiBase/api/admin/features" -Headers $Headers -Body $body | Out-Null
  Write-Host "$($f.label): enabled=$($f.enabled), subscriberOnly=$($f.subscriberOnly)" -ForegroundColor Green
}
function Set-FeatureByKey {
  $key=Read-Host 'Feature key (e.g. roadmap)'; $mode=Read-Host 'Access mode: free / subscriber / disabled';
  if($mode -notin @('free','subscriber','disabled')){throw 'Mode must be free, subscriber or disabled.'}
  $body=@{feature_key=$key;enabled=($mode -ne 'disabled');subscriber_only=($mode -eq 'subscriber')}|ConvertTo-Json
  Invoke-RestMethod -Method Post -Uri "$ApiBase/api/admin/features" -Headers $Headers -Body $body | Out-Null
  Write-Host "$key set to $mode." -ForegroundColor Green
}
function Subscriber {
  $email=Read-Host 'Subscriber email'; $days=Read-Host 'Subscription days (default 30)'; if(-not $days){$days=30}; $body=@{email=$email;active=$true;days=[int]$days}|ConvertTo-Json; $r=Invoke-RestMethod -Method Post -Uri "$ApiBase/api/admin/set-subscriber" -Headers $Headers -Body $body; Write-Host "Subscriber active until $($r.subscriberUntil)" -ForegroundColor Green
}
function Run-Pipeline {
  $enabled=(Load-Config).countries | Where-Object enabled
  if(-not $enabled){Write-Host 'No enabled countries.' -ForegroundColor Yellow;return}
  foreach($c in $enabled){Write-Host "Running data pipeline for $($c.name)..." -ForegroundColor Cyan
    $py=Join-Path $Root 'scripts\pipeline_country.py'
    if(Test-Path $py){python $py --country $c.code --config $ConfigPath}
    else { Write-Host 'Country pipeline adapter not present; run the Ghana legacy pipeline and publish its analysis.' -ForegroundColor Yellow }
  }
}

function Publish-PremiumDiscoveries {
  $file=Join-Path $Root 'data\discoveries.json'; if(-not(Test-Path $file)){throw 'Missing data/discoveries.json'}
  $payload=Get-Content $file -Raw | ConvertFrom-Json
  $body=@{content_key='blue_ocean_discoveries';country_code='GHA';payload=$payload}|ConvertTo-Json -Depth 30
  Invoke-RestMethod -Method Post -Uri "$ApiBase/api/admin/publish-premium" -Headers $Headers -Body $body | Out-Null
  Write-Host 'Published premium discovery content to Cloudflare D1.' -ForegroundColor Green
}
function Publish-GhanaSeed {
  $report=Join-Path $Root 'data\ghana-analysis.json'; if(-not(Test-Path $report)){throw 'Missing data/ghana-analysis.json'}; $payload=Get-Content $report -Raw | ConvertFrom-Json; $date=$payload.analysis_date; $body=@{country_code='GHA';report_date=$date;payload=$payload}|ConvertTo-Json -Depth 20; Invoke-RestMethod -Method Post -Uri "$ApiBase/api/admin/publish-report" -Headers $Headers -Body $body | Out-Null; Write-Host "Published Ghana report $date." -ForegroundColor Green
}

while($true){
 Write-Host "`n=== SEE STATS ADMIN ===" -ForegroundColor Cyan
 Write-Host '1. List countries / source URLs'
 Write-Host '2. Enable / disable country'
 Write-Host '3. Add statistical source URL'
 Write-Host '4. Add country'
 Write-Host '5. Activate subscriber'
 Write-Host '6. Run weekly extraction'
 Write-Host '7. Publish Ghana seed report'
 Write-Host '8. Sync country registry'
 Write-Host '9. View feature access policies'
 Write-Host '10. Change a feature access policy'
 Write-Host '11. Set feature by key (free/subscriber/disabled)'
 Write-Host '12. Publish premium discovery content'
 Write-Host '13. Exit'
 $choice=Read-Host 'Select'
 switch($choice){'1'{Show-Countries; (Load-Config).countries|ForEach-Object{Write-Host "  $($_.name):"; $_.sources|ForEach-Object{Write-Host "    - $($_.name): $($_.url)"}}}' '2'{Toggle-Country}' '3'{Add-Source}' '4'{Add-Country}' '5'{Subscriber}' '6'{Run-Pipeline}' '7'{Publish-GhanaSeed}' '8'{Sync-Countries}' '9'{Show-Features}' '10'{Set-FeaturePolicy}' '11'{Set-FeatureByKey}' '12'{Publish-PremiumDiscoveries}' '13'{break} default{Write-Host 'Choose 1-13.' -ForegroundColor Yellow}}
}
