#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

function getBinaryPath() {
  const platform = process.platform;
  const arch = process.arch;

  // Map Node.js platform names to our binary naming
  const platformMap = {
    'darwin': 'darwin',
    'linux': 'linux',
    'win32': 'windows'
  };

  // Map Node.js arch names to our binary naming
  const archMap = {
    'x64': 'x64',
    'arm64': 'arm64'
  };

  const mappedPlatform = platformMap[platform];
  const mappedArch = archMap[arch];

  if (!mappedPlatform || !mappedArch) {
    console.error(`Unsupported platform: ${platform}-${arch}`);
    process.exit(1);
  }

  const binaryName = platform === 'win32'
    ? 'compass.exe'
    : 'compass';

  const binaryPath = path.join(
    __dirname,
    '..',
    'vendor',
    `${mappedPlatform}-${mappedArch}`,
    binaryName
  );

  return binaryPath;
}

function main() {
  const binaryPath = getBinaryPath();

  // Check if binary exists
  if (!fs.existsSync(binaryPath)) {
    console.error('Compass binary not found.');
    console.error('');
    console.error('The Compass CLI binary was not installed correctly.');
    console.error('This usually happens when:');
    console.error('  1. The postinstall script failed to download the binary');
    console.error('  2. Your platform is not supported');
    console.error('  3. You are offline during installation');
    console.error('');
    console.error(`Expected binary at: ${binaryPath}`);
    console.error('');
    console.error('Try reinstalling:');
    console.error('  npm install -g compass-cli --force');
    console.error('');
    console.error('Or check GitHub Releases for manual download:');
    console.error('  https://github.com/YOUR_USERNAME/compass-cli/releases');
    process.exit(1);
  }

  // Make sure binary is executable (Unix-like systems)
  if (process.platform !== 'win32') {
    try {
      fs.chmodSync(binaryPath, 0o755);
    } catch (err) {
      // Ignore errors, binary might already be executable
    }
  }

  // Spawn the binary with all arguments
  const child = spawn(binaryPath, process.argv.slice(2), {
    stdio: 'inherit',
    windowsHide: false
  });

  child.on('error', (err) => {
    console.error('Failed to start Compass:', err.message);
    process.exit(1);
  });

  child.on('exit', (code, signal) => {
    if (signal) {
      process.kill(process.pid, signal);
    } else {
      process.exit(code || 0);
    }
  });
}

main();
