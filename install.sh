#!/bin/sh

# Setup Python venv and install packages
echo "Setting up Python virtual environment in ./.venv"
python3.8 -m venv ./.venv
source .venv/bin/activate
python3.8 -m pip install -r environment/requirements.txt

# Create default profile, then copy over our custom settings
export IPYTHONDIR="./environment/ipython"
echo "Creating new ipython profile at ${IPYTHONDIR}"
ipython profile create
cp ./environment/ipython/ipython_kernel_config.py $IPYTHONDIR/profile_default/ipython_kernel_config.py

# Install git hooks
pre-commit install

if command -v direnv &> /dev/null
then
    echo "Note: direnv is installed; navigating to this directory will "
    echo "automatically activate this environment."
    direnv allow .envrc
else
    echo "Note: direnv is not installed; you'll need to manually set up your"
    echo "environment and activate it whenever you want to work on the textbook." 
    echo "See README.md for details. To leave this venv, run `deactivate`."
fi

echo "\nQiskit Textbook setup complete!\n"
