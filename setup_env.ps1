# PowerShell script to set up environment variables for UE5 Semantic Automation

Write-Host "=== UE5 Semantic Automation - Environment Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if API key is already set
$existingKey = [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")

if ($existingKey) {
    Write-Host "✓ OPENAI_API_KEY is already set" -ForegroundColor Green
    Write-Host "  Current value: $($existingKey.Substring(0, [Math]::Min(10, $existingKey.Length)))..." -ForegroundColor Gray
    Write-Host ""
    $overwrite = Read-Host "Do you want to update it? (y/N)"
    if ($overwrite -ne 'y' -and $overwrite -ne 'Y') {
        Write-Host "Keeping existing API key." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "Please enter your Windsurf/OpenAI API key:" -ForegroundColor Yellow
Write-Host "(This will be stored as a USER environment variable)" -ForegroundColor Gray
Write-Host ""
$apiKey = Read-Host "API Key"

if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host ""
    Write-Host "✗ No API key provided. Exiting." -ForegroundColor Red
    exit 1
}

# Set the environment variable
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", $apiKey, "User")

Write-Host ""
Write-Host "✓ Environment variable set successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: You need to restart your applications for the change to take effect:" -ForegroundColor Yellow
Write-Host "  - Close and reopen PowerShell/Command Prompt" -ForegroundColor Gray
Write-Host "  - Restart Unreal Engine" -ForegroundColor Gray
Write-Host "  - Restart Windsurf/VS Code" -ForegroundColor Gray
Write-Host ""
Write-Host "To verify in a NEW PowerShell window, run:" -ForegroundColor Cyan
Write-Host '  $env:OPENAI_API_KEY' -ForegroundColor White
Write-Host ""
Write-Host "Setup complete! 🎉" -ForegroundColor Green
