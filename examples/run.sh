#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m gbt_digital_human info
PYTHONPATH=src python -m gbt_digital_human check --payload '{}'
PYTHONPATH=src python -m gbt_digital_human run   --payload '{}'
