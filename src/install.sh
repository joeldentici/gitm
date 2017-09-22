#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Installing gitm..."

mkdir -p "$HOME/.gitm"
cp -r $DIR/* "$HOME/.gitm"
rm /bin/gitm > /dev/null 2>&1
ln -s "$HOME/.gitm/gitm.py" /bin/gitm
chown -R "$SUDO_USER:$SUDO_USER" "$HOME/.gitm"
chmod -R 755 "$HOME/.gitm"

echo "gitm installed!"