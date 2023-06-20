#!/bin/sh
set -e

# Setup Python venv and install packages
echo "Setting up Python virtual environment in ./.venv"
python -m venv ./.venv
. .venv/Scripts/activate
python -m pip install -r environment/requirements-win.txt

# Create default profile, then copy over our custom settings
export IPYTHONDIR="./environment/ipython"
echo "Creating new ipython profile at ${IPYTHONDIR}"
ipython profile create
cp ./environment/ipython/ipython_kernel_config.py $IPYTHONDIR/profile_default/ipython_kernel_config.py

# Install git hooks
pre-commit install

echo ""
echo "Qiskit Textbook setup complete!"
