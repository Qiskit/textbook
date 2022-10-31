#!/bin/sh
set -e
./tests/passes/nb_pylint.sh
python tests/passes/nb_vale.py --CI
