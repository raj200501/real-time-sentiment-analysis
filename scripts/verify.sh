#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export PYTHONPATH="$ROOT_DIR/src"

python -m unittest discover -s "$ROOT_DIR/tests"
python "$ROOT_DIR/scripts/smoke_test.py"
