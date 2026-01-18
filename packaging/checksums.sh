#!/bin/bash
# Generate checksums for all artifacts

cd "$(dirname "$0")/artifacts"

echo "Generating checksums..."

for file in compass-*; do
    if [[ ! "$file" =~ \.sha256$ ]]; then
        shasum -a 256 "$file" > "${file}.sha256"
        echo "Generated: ${file}.sha256"
    fi
done

# Create combined checksums file
cat *.sha256 > SHA256SUMS
echo "Created SHA256SUMS"
