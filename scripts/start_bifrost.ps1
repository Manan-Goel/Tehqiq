$settings = Get-Content -LiteralPath (Join-Path $PSScriptRoot '..\.env') | ConvertFrom-StringData
if (-not $settings.OPENROUTER_API_KEY) { throw 'OPENROUTER_API_KEY is missing from .env' }
$env:OPENROUTER_API_KEY = $settings.OPENROUTER_API_KEY
if ($settings.BIFROST_API_KEY) { $env:BIFROST_API_KEY = $settings.BIFROST_API_KEY }
Push-Location (Join-Path $PSScriptRoot '..')
try { npx -y @maximhq/bifrost -app-dir ./bifrost }
finally { Pop-Location }
