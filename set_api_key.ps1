# Simple PowerShell script to set API key

Write-Host "=== UE5 Semantic Automation - API Key Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check existing key
$existing = [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")

if ($existing)
{
    Write-Host "Current API key is set: $($existing.Substring(0, 10))..." -ForegroundColor Green
    Write-Host ""
    $response = Read-Host "Update it? (y/N)"
    if ($response -ne 'y' -and $response -ne 'Y')
    {
        Write-Host "Keeping existing key." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "Enter your Windsurf/OpenAI API key:" -ForegroundColor Yellow
$key = Read-Host "API Key"

if ($key)
{
    [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", $key, "User")
    Write-Host ""
    Write-Host "SUCCESS! API key has been set." -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT - Restart required:" -ForegroundColor Yellow
    Write-Host "  1. Close this PowerShell window" -ForegroundColor Gray
    Write-Host "  2. Restart Unreal Engine" -ForegroundColor Gray
    Write-Host "  3. Restart Windsurf" -ForegroundColor Gray
    Write-Host ""
    Write-Host "To verify (in a NEW window): " -NoNewline -ForegroundColor Cyan
    Write-Host '$env:OPENAI_API_KEY' -ForegroundColor White
}
else
{
    Write-Host ""
    Write-Host "ERROR: No API key entered." -ForegroundColor Red
    exit 1
}
