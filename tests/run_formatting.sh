#!/bin/sh
set -e
python tests/passes/blips.py
python tests/passes/nb_metadata.py
python tests/passes/nb_svg.py
