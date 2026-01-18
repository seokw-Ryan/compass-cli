# Build script for Windows (PowerShell)

$ErrorActionPreference = "Stop"

Write-Host "Building Compass CLI..."

# Change to project root
Set-Location $PSScriptRoot\..

# Detect architecture
$Arch = if ([Environment]::Is64BitOperatingSystem) { "x64" } else { "x86" }
$Platform = "windows"

Write-Host "Platform: $Platform"
Write-Host "Architecture: $Arch"

# Setup Python environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -e python/
pip install --quiet pyinstaller

# Build with PyInstaller
Write-Host "Running PyInstaller..."
pyinstaller packaging/pyinstaller.spec --clean --distpath packaging/artifacts

# Rename binary
$BinaryName = "compass-$Platform-$Arch.exe"
Move-Item -Path "packaging/artifacts/compass.exe" -Destination "packaging/artifacts/$BinaryName" -Force

Write-Host "Build complete: packaging/artifacts/$BinaryName"

# Generate checksum
Set-Location packaging/artifacts
$Hash = Get-FileHash $BinaryName -Algorithm SHA256
"$($Hash.Hash.ToLower())  $BinaryName" | Out-File -Encoding ASCII "${BinaryName}.sha256"
Write-Host "Checksum: $(Get-Content ${BinaryName}.sha256)"
