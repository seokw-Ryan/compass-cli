#!/usr/bin/env node

const https = require('https');
const fs = require('fs');
const path = require('path');
const { pipeline } = require('stream');
const { promisify } = require('util');

const streamPipeline = promisify(pipeline);

// Get package version
const packageJson = require('../package.json');
const VERSION = packageJson.version;

function getPlatformInfo() {
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
    console.error('Compass CLI supports:');
    console.error('  - macOS (x64, arm64)');
    console.error('  - Linux (x64, arm64)');
    console.error('  - Windows (x64)');
    process.exit(1);
  }

  return { platform: mappedPlatform, arch: mappedArch };
}

function getBinaryInfo() {
  const { platform, arch } = getPlatformInfo();
  const ext = platform === 'windows' ? '.exe' : '';

  const binaryName = `compass-${platform}-${arch}${ext}`;
  const downloadUrl = `https://github.com/YOUR_USERNAME/compass-cli/releases/download/v${VERSION}/${binaryName}`;

  const vendorDir = path.join(__dirname, '..', 'vendor', `${platform}-${arch}`);
  const binaryPath = path.join(vendorDir, `compass${ext}`);

  return { binaryName, downloadUrl, vendorDir, binaryPath };
}

async function downloadBinary() {
  const { binaryName, downloadUrl, vendorDir, binaryPath } = getBinaryInfo();

  console.log('Compass CLI postinstall');
  console.log('========================');
  console.log(`Version: ${VERSION}`);
  console.log(`Platform: ${process.platform}-${process.arch}`);
  console.log('');
  console.log('Download information:');
  console.log(`  Binary: ${binaryName}`);
  console.log(`  URL: ${downloadUrl}`);
  console.log(`  Destination: ${binaryPath}`);
  console.log('');

  // For now, just print what WOULD be downloaded
  // In production, this would actually download the binary
  console.log('NOTE: Binary download not yet implemented.');
  console.log('This is a skeleton setup. In production, this script would:');
  console.log('  1. Download the binary from GitHub Releases');
  console.log('  2. Verify the checksum');
  console.log('  3. Extract and place in vendor directory');
  console.log('  4. Make executable (Unix-like systems)');
  console.log('');
  console.log('For now, you can manually build and place binaries in:');
  console.log(`  ${vendorDir}/`);

  // Create vendor directory structure
  if (!fs.existsSync(vendorDir)) {
    fs.mkdirSync(vendorDir, { recursive: true });
    console.log(`Created directory: ${vendorDir}`);
  }

  console.log('');
  console.log('Postinstall complete.');
}

// Run installation
downloadBinary().catch((err) => {
  console.error('Installation failed:', err.message);
  console.error('');
  console.error('You can manually download the binary from:');
  console.error(`  https://github.com/YOUR_USERNAME/compass-cli/releases/tag/v${VERSION}`);
  // Don't exit with error to allow npm install to succeed
  process.exit(0);
});
