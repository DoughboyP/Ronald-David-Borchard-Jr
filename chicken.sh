#!/data/data/com.termux/files/usr/bin/bash
# chicken.sh — Termux bootstrap & launcher for Ronald-David-Borchard-Jr
# Usage: bash chicken.sh

set -e

REPO_URL="https://github.com/DoughboyP/Ronald-David-Borchard-Jr.git"
REPO_DIR="$HOME/Ronald-David-Borchard-Jr"

# ── 1. Update Termux packages ──────────────────────────────────────────────────
echo ""
echo "=== Updating Termux packages ==="
pkg update -y && pkg upgrade -y

# ── 2. Install Python (if needed) ─────────────────────────────────────────────
if ! command -v python &>/dev/null; then
    echo ""
    echo "=== Installing Python ==="
    pkg install -y python
else
    echo ""
    echo "=== Python already installed: $(python --version) ==="
fi

# ── 3. Install git (if needed) ────────────────────────────────────────────────
if ! command -v git &>/dev/null; then
    echo ""
    echo "=== Installing git ==="
    pkg install -y git
fi

# ── 4. Clone / update the repo ────────────────────────────────────────────────
echo ""
if [ -d "$REPO_DIR/.git" ]; then
    echo "=== Repo already exists — pulling latest changes ==="
    git -C "$REPO_DIR" pull --ff-only
else
    echo "=== Cloning repo ==="
    git clone "$REPO_URL" "$REPO_DIR"
fi

cd "$REPO_DIR"

# ── 5. Launcher menu ──────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║      Ronald David Borchard Jr — Termux Launcher     ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  1) Ronald David Borchard Jr — Life Adventure Game"
echo "  2) El Capitan — World Simulation Engine"
echo "  3) MOB CHESS — Universe Control"
echo "  4) TRE-UPR — Transcendent Reality Engine"
echo "  0) Exit"
echo ""
read -rp "Select [0-4]: " choice

case "$choice" in
    1)
        echo ""
        python main.py
        ;;
    2)
        echo ""
        python el_capitan_main.py "$@"
        ;;
    3)
        echo ""
        python mob_chess_main.py "$@"
        ;;
    4)
        echo ""
        python tre_upr_main.py "$@"
        ;;
    0)
        echo ""
        echo "Peace out."
        ;;
    *)
        echo ""
        echo "Invalid choice. Run the script again and pick 0-4."
        exit 1
        ;;
esac
