# Check Visual Studio Installation Status
# Run this script to verify VS installations and MSVC versions

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Visual Studio Installation Status Check" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Check for running installers
Write-Host "1. Checking for running installers..." -ForegroundColor Yellow
$installers = Get-Process | Where-Object {$_.ProcessName -like "*setup*" -or $_.ProcessName -like "*installer*" -or $_.ProcessName -like "*vs_*"}
if ($installers) {
    Write-Host "   ⚠️  Installation in progress:" -ForegroundColor Yellow
    $installers | Select-Object ProcessName, Id | Format-Table
    Write-Host "   Please wait for installation to complete." -ForegroundColor Yellow
} else {
    Write-Host "   ✅ No installers running" -ForegroundColor Green
}
Write-Host ""

# Check VS installations
Write-Host "2. Checking Visual Studio installations..." -ForegroundColor Yellow
$vsPath = "C:\Program Files\Microsoft Visual Studio"
if (Test-Path $vsPath) {
    $versions = Get-ChildItem $vsPath -Directory | Select-Object Name
    Write-Host "   Found VS versions:" -ForegroundColor Green
    $versions | ForEach-Object { Write-Host "   - $($_.Name)" -ForegroundColor Cyan }
} else {
    Write-Host "   ❌ No Visual Studio installations found" -ForegroundColor Red
}
Write-Host ""

# Check MSVC versions for each VS installation
Write-Host "3. Checking MSVC toolchain versions..." -ForegroundColor Yellow

$vsVersions = @("2022", "2026")
foreach ($ver in $vsVersions) {
    $editions = @("Community", "Professional", "Enterprise", "BuildTools", "Preview")
    foreach ($edition in $editions) {
        $msvcPath = "C:\Program Files\Microsoft Visual Studio\$ver\$edition\VC\Tools\MSVC"
        if (Test-Path $msvcPath) {
            Write-Host "   VS $ver $edition" -ForegroundColor Cyan
            $toolchains = Get-ChildItem $msvcPath -Directory | Select-Object Name
            foreach ($tc in $toolchains) {
                $version = $tc.Name
                if ($version -match "(\d+)\.(\d+)\.(\d+)") {
                    $major = [int]$matches[1]
                    $minor = [int]$matches[2]
                    
                    # Check if version is >= 14.44
                    if ($major -eq 14 -and $minor -ge 44) {
                        Write-Host "   ✅ $version (Compatible with UE 5.7)" -ForegroundColor Green
                    } elseif ($major -gt 14) {
                        Write-Host "   ✅ $version (Compatible with UE 5.7)" -ForegroundColor Green
                    } else {
                        Write-Host "   ❌ $version (Too old for UE 5.7)" -ForegroundColor Red
                    }
                }
            }
        }
    }
}
Write-Host ""

# Check with vswhere
Write-Host "4. Using vswhere to find installations..." -ForegroundColor Yellow
$vswhere = "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
if (Test-Path $vswhere) {
    $installations = & $vswhere -all -prerelease -products * -format json | ConvertFrom-Json
    if ($installations) {
        foreach ($install in $installations) {
            Write-Host "   $($install.displayName)" -ForegroundColor Cyan
            Write-Host "   Version: $($install.installationVersion)" -ForegroundColor Gray
            Write-Host "   Path: $($install.installationPath)" -ForegroundColor Gray
            Write-Host ""
        }
    }
} else {
    Write-Host "   ⚠️  vswhere.exe not found" -ForegroundColor Yellow
}

# Summary
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

$compatible = $false
foreach ($ver in $vsVersions) {
    $editions = @("Community", "Professional", "Enterprise", "BuildTools", "Preview")
    foreach ($edition in $editions) {
        $msvcPath = "C:\Program Files\Microsoft Visual Studio\$ver\$edition\VC\Tools\MSVC"
        if (Test-Path $msvcPath) {
            $toolchains = Get-ChildItem $msvcPath -Directory
            foreach ($tc in $toolchains) {
                if ($tc.Name -match "(\d+)\.(\d+)") {
                    $major = [int]$matches[1]
                    $minor = [int]$matches[2]
                    if (($major -eq 14 -and $minor -ge 44) -or $major -gt 14) {
                        $compatible = $true
                        Write-Host "✅ READY TO BUILD: Found compatible MSVC $($tc.Name)" -ForegroundColor Green
                        Write-Host "   Location: $msvcPath\$($tc.Name)" -ForegroundColor Gray
                        Write-Host ""
                        Write-Host "Next step: Run plugin build" -ForegroundColor Yellow
                        Write-Host "   cd UE5SemanticAutomation" -ForegroundColor Cyan
                        Write-Host "   python Build.py `"C:\Program Files\Epic Games\UE_5.7`" -TargetPlatforms=Win64" -ForegroundColor Cyan
                    }
                }
            }
        }
    }
}

if (-not $compatible) {
    Write-Host "❌ NO COMPATIBLE MSVC FOUND" -ForegroundColor Red
    Write-Host ""
    Write-Host "Required: MSVC v14.44 or higher" -ForegroundColor Yellow
    Write-Host "Action needed:" -ForegroundColor Yellow
    Write-Host "   1. Wait for VS 2026 Insiders to finish installing" -ForegroundColor Cyan
    Write-Host "   2. Or update VS 2022 Community via Visual Studio Installer" -ForegroundColor Cyan
    Write-Host "   3. Then run this script again to verify" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
