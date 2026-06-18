#!/usr/bin/env bash
# ScholarWeave installer — wires the vendored skill repos into ~/.claude.
#
# Non-destructive by design:
#   * Skills already present as REAL directories are never touched.
#   * Add-on skills are SYMLINKED from vendor/, so `./update.sh` keeps them current.
#   * Your dailypaper user-config.json is preserved if it already exists.
#
# Layers:
#   1. obsidian-skills (kepano)   -> Obsidian primitives (always installed, additive)
#   2. dailypaper-skills          -> daily paper pipeline (installed only if missing)
#   3. claude-scholar (FULL)      -> opt-in via --with-scholar (mutates settings.json + hooks)
#
# Usage:
#   ./install.sh                 # layers 1 + 2 (safe, additive, reversible)
#   ./install.sh --with-scholar  # also run claude-scholar's full installer
#   ./install.sh --scholar-only  # only run claude-scholar's full installer
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENDOR="$REPO_DIR/vendor"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
SKILLS="$CLAUDE_HOME/skills"

WITH_SCHOLAR=0
SCHOLAR_ONLY=0
for arg in "$@"; do
  case "$arg" in
    --with-scholar) WITH_SCHOLAR=1 ;;
    --scholar-only) WITH_SCHOLAR=1; SCHOLAR_ONLY=1 ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "unknown arg: $arg" >&2; exit 2 ;;
  esac
done

# ---- ensure vendored repos exist at the pinned SHAs -------------------------
ensure_vendor() {
  local name url sha dir
  while read -r name url sha; do
    [[ "$name" =~ ^#|^$ ]] && continue
    dir="$VENDOR/$name"
    if [ ! -d "$dir/.git" ]; then
      echo "cloning $name ..."
      git clone "$url" "$dir"
    fi
    git -C "$dir" rev-parse -q --verify "$sha^{commit}" >/dev/null 2>&1 || git -C "$dir" fetch --all -q
    git -C "$dir" checkout -q "$sha" 2>/dev/null || echo "  (warn) could not pin $name to $sha; using current HEAD"
  done < "$REPO_DIR/versions.lock"
}

# ---- symlink one skill dir, never clobbering a real install -----------------
link_skill() {
  local src="$1" name dest cur
  name="$(basename "$src")"
  dest="$SKILLS/$name"
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then
    echo "  skip   $name  (real dir already installed — left untouched)"; return
  fi
  if [ -L "$dest" ]; then
    cur="$(readlink "$dest")"
    [ "$cur" = "$src" ] && { echo "  ok     $name  (already linked)"; return; }
  fi
  ln -sfn "$src" "$dest"
  echo "  link   $name"
}

install_obsidian_skills() {
  echo "== Layer 1: obsidian-skills (kepano) =="
  for d in "$VENDOR"/obsidian-skills/skills/*/; do link_skill "${d%/}"; done
}

install_dailypaper() {
  echo "== Layer 2: dailypaper-skills =="
  local src f dest="$SKILLS/_shared"
  for d in "$VENDOR"/dailypaper-skills/skills/*/; do
    [ "$(basename "${d%/}")" = "_shared" ] && continue
    link_skill "${d%/}"
  done
  # _shared: link helper scripts (if missing), preserve any existing user-config.json
  src="$VENDOR/dailypaper-skills/skills/_shared"
  mkdir -p "$dest"
  for f in "$src"/*.py; do
    [ -e "$dest/$(basename "$f")" ] || ln -sfn "$f" "$dest/$(basename "$f")"
  done
  if [ -f "$dest/user-config.json" ]; then
    echo "  keep   _shared/user-config.json  (existing config preserved)"
  else
    cp "$REPO_DIR/config/dailypaper-user-config.json" "$dest/user-config.json"
    echo "  write  _shared/user-config.json  (from ScholarWeave template — verify obsidian_vault path)"
  fi
}

install_scholar() {
  echo "== Layer 3: claude-scholar FULL install =="
  echo "   This delegates to the upstream installer, which:"
  echo "     - merges hooks/mcpServers/enabledPlugins into ~/.claude/settings.json"
  echo "     - installs skills/commands/agents/rules/hooks"
  echo "     - backs up overwritten files to ~/.claude/.claude-scholar-backups/<ts>/"
  echo "   Reverse anytime with: ./uninstall.sh --scholar"
  bash "$VENDOR/claude-scholar/scripts/setup.sh"
}

# ---- run --------------------------------------------------------------------
# Scholar runs FIRST: it installs real dirs (e.g. its own defuddle, wired into
# obsidian-source-ingestion). The symlink layers below then skip any name it
# already owns, so scholar never writes through one of our symlinks into vendor/.
ensure_vendor
mkdir -p "$SKILLS"
[ "$WITH_SCHOLAR" = 1 ] && install_scholar
if [ "$SCHOLAR_ONLY" = 0 ]; then
  install_obsidian_skills
  install_dailypaper
fi

echo
echo "Done. Restart Claude Code (or /reload) to pick up new skills."
if [ "$WITH_SCHOLAR" = 0 ]; then
  echo "Tip: run './install.sh --with-scholar' to add the full claude-scholar suite."
fi
exit 0
