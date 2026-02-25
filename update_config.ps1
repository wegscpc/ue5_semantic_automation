# Update settings.json to use environment variable

$configPath = "config\settings.json"
$config = Get-Content $configPath -Raw | ConvertFrom-Json

# Set api_key to empty string to use environment variable
$config.llm.api_key = ""

# Save back to file
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath

Write-Host "✓ Updated settings.json to use environment variable OPENAI_API_KEY" -ForegroundColor Green
