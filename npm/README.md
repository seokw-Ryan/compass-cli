# Compass CLI (npm wrapper)

This package provides an npm distribution of the Compass CLI tool.

## Installation

```bash
npm install -g compass-cli
```

## Usage

After installation, the `compass` command will be available:

```bash
compass --help
compass init --vault ~/my-vault
compass chat
```

## How it works

This npm package:
1. Downloads the appropriate prebuilt binary for your platform during `postinstall`
2. Binaries are built with PyInstaller and hosted on GitHub Releases
3. The `compass` command wraps the binary execution

## Supported Platforms

- macOS (x64, arm64)
- Linux (x64, arm64)
- Windows (x64)

## Troubleshooting

If the binary fails to download during installation:

1. Check your internet connection
2. Verify the GitHub Release exists for your version
3. Manually download from: https://github.com/YOUR_USERNAME/compass-cli/releases
4. Place binary in `node_modules/compass-cli/vendor/<platform>-<arch>/`

## Development

This package is automatically built and published from the main repository.

See: https://github.com/YOUR_USERNAME/compass-cli

## License

MIT
