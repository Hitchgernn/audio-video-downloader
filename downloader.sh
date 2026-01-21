#!/usr/bin/env bash
set -euo pipefail

# Find this script's directory so it works from anywhere
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Prefer python3, fallback to python
PYTHON_BIN="$(command -v python3 || true)"
if [[ -z "${PYTHON_BIN}" ]]; then
  PYTHON_BIN="$(command -v python || true)"
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "Error: Python not found. Install python3 first."
  exit 1
fi

# Optional: create venv automatically (nice for GitHub users)
VENV_DIR="${SCRIPT_DIR}/.venv"
if [[ ! -d "${VENV_DIR}" ]]; then
  echo "Creating virtual environment..."
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

# Activate venv
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

# Install deps
python -m pip install -U pip >/dev/null
python -m pip install -U yt-dlp >/dev/null

# Check ffmpeg (required)
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "Error: ffmpeg not found. Install it:"
  echo "  Fedora: sudo dnf install ffmpeg"
  echo "  Ubuntu/Debian: sudo apt install ffmpeg"
  exit 1
fi

# Run the python script (pass args through)
python "${SCRIPT_DIR}/downloader.py" "$@"
