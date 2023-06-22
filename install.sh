#!/bin/sh
set -e


# Get the operating system name
os_name=$(uname -o)

print os_name
# Check if the operating system is Windows
if [[ "$os_name" == "Cygwin" || "$os_name" == "Msys" ]]; then
    echo "Setting up Python virtual environment in ./.venv"
    python -m venv ./.venv
    . .venv/Scripts/activate
    python -m pip install -r environment/requirements.txt
else
    # Setup Python venv and install packages
    echo "Setting up Python virtual environment in ./.venv"
    python3.8 -m venv ./.venv
    . .venv/bin/activate
    python3.8 -m pip install -r environment/requirements.txt
fi

# Create default profile, then copy over our custom settings
export IPYTHONDIR="./environment/ipython"
echo "Creating new ipython profile at ${IPYTHONDIR}"
ipython profile create
cp ./environment/ipython/ipython_kernel_config.py $IPYTHONDIR/profile_default/ipython_kernel_config.py

# Install git hooks
pre-commit install

echo ""
echo "Qiskit Textbook setup complete!"
