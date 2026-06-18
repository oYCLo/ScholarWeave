#!/usr/bin/env bash
# Pull latest upstream for every vendored repo, rewrite versions.lock with the
# new SHAs, then re-run install.sh so symlinks pick up any new/renamed skills.
#
# Usage:
#   ./update.sh                 # update + re-link layers 1 + 2
#   ./update.sh --with-scholar  # also re-run claude-scholar's installer
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENDOR="$REPO_DIR/vendor"
LOCK="$REPO_DIR/versions.lock"
TMP="$(mktemp)"

{
  echo "# Pinned upstream commits for vendored skill repos."
  echo "# Reproduce with: ./install.sh   |   Bump with: ./update.sh"
  echo
} > "$TMP"

while read -r name url sha; do
  [[ "$name" =~ ^#|^$ ]] && continue
  dir="$VENDOR/$name"
  if [ -d "$dir/.git" ]; then
    echo "updating $name ..."
    git -C "$dir" fetch -q --all
    git -C "$dir" checkout -q "$(git -C "$dir" remote show origin | sed -n 's/.*HEAD branch: //p')" 2>/dev/null || true
    git -C "$dir" pull -q --ff-only || git -C "$dir" reset -q --hard '@{u}'
  else
    git clone -q "$url" "$dir"
  fi
  new="$(git -C "$dir" rev-parse HEAD)"
  printf '%-18s %-52s %s\n' "$name" "$url" "$new" >> "$TMP"
done < "$LOCK"

mv "$TMP" "$LOCK"
echo "versions.lock updated."
"$REPO_DIR/install.sh" "$@"
