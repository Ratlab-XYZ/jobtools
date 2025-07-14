#!/bin/bash
set -e

REPO="Ratlab-XYZ/jobtools"
BIN_NAME="uw"
INSTALL_DIR="$HOME/.local/bin"
PROFILE=""

# Detect shell and set profile file
if [ -n "$ZSH_VERSION" ]; then
  PROFILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
  PROFILE="$HOME/.bashrc"
else
  PROFILE="$HOME/.profile"
fi

echo "Installing $BIN_NAME from latest $REPO release..."

mkdir -p "$INSTALL_DIR"

URL=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r '.assets[] | select(.name | test("'"$BIN_NAME"'")) | .browser_download_url')

if [ -z "$URL" ]; then
  echo "Error: Could not find the download URL for $BIN_NAME in the latest release."
  exit 1
fi

curl -L "$URL" -o "$INSTALL_DIR/$BIN_NAME"
chmod +x "$INSTALL_DIR/$BIN_NAME"

# Add to PATH in profile if not already present
if ! grep -qxF "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$PROFILE"; then
  echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$PROFILE"
  echo "Added ~/.local/bin to PATH in $PROFILE"
fi

echo "Installed $BIN_NAME to $INSTALL_DIR"
echo "Please reload your shell or run: source $PROFILE"
