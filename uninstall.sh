#!/usr/bin/env bash
# Remove what ScholarWeave installed. Conservative: only deletes SYMLINKS that
# point into this repo's vendor/. Real directories and your configs are kept.
#
# Usage:
#   ./uninstall.sh             # remove the symlinked add-on skills (layers 1 + 2)
#   ./uninstall.sh --scholar   # ALSO run claude-scholar's own uninstaller
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENDOR="$REPO_DIR/vendor"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
SKILLS="$CLAUDE_HOME/skills"

DO_SCHOLAR=0
[ "${1:-}" = "--scholar" ] && DO_SCHOLAR=1

echo "== removing symlinks that point into $VENDOR =="
removed=0
for link in "$SKILLS"/* "$SKILLS"/_shared/*; do
  [ -L "$link" ] || continue
  case "$(readlink "$link")" in
    "$VENDOR"/*) echo "  rm   ${link#$SKILLS/}"; rm -f "$link"; removed=$((removed+1)) ;;
  esac
done
echo "  ($removed symlinks removed; real dirs and user-config.json preserved)"

if [ "$DO_SCHOLAR" = 1 ]; then
  echo "== running claude-scholar uninstaller =="
  bash "$VENDOR/claude-scholar/scripts/uninstall.sh"
fi
echo "Done."
