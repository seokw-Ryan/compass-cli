#!/bin/bash
# Build script for Unix-like systems (macOS/Linux)

set -e

echo "Building Compass CLI..."

# Change to project root
cd "$(dirname "$0")/.."

# Detect platform and architecture
PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case $ARCH in
    x86_64)
        ARCH="x64"
        ;;
    aarch64|arm64)
        ARCH="arm64"
        ;;
esac

echo "Platform: $PLATFORM"
echo "Architecture: $ARCH"

# Setup Python environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -e python/
pip install -q pyinstaller

# Build with PyInstaller
echo "Running PyInstaller..."
pyinstaller packaging/pyinstaller.spec --clean --distpath packaging/artifacts

# Rename binary to include platform/arch
BINARY_NAME="compass-${PLATFORM}-${ARCH}"
if [ "$PLATFORM" = "windows" ]; then
    BINARY_NAME="${BINARY_NAME}.exe"
fi

mv packaging/artifacts/compass packaging/artifacts/$BINARY_NAME 2>/dev/null || \
   mv packaging/artifacts/compass.exe packaging/artifacts/$BINARY_NAME 2>/dev/null || true

echo "Build complete: packaging/artifacts/$BINARY_NAME"

# Generate checksum
cd packaging/artifacts
shasum -a 256 $BINARY_NAME > ${BINARY_NAME}.sha256
echo "Checksum: $(cat ${BINARY_NAME}.sha256)"
