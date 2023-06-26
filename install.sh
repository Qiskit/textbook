#!/bin/sh
set -e


# Get the operating system name
os_name=$(uname -o)

#print os_name

echo "Setting up Python virtual environment in ./.venv"
python -m venv ./.venv
if [[ "$os_name" == "Cygwin" || "$os_name" == "Msys" ]]; then
    . .venv/Scripts/activate
else
    . .venv/bin/activate
fi
python -m pip install -r environment/requirements.txt

# Create default profile, then copy over our custom settings
export IPYTHONDIR="./environment/ipython"
echo "Creating new ipython profile at ${IPYTHONDIR}"
ipython profile create
cp ./environment/ipython/ipython_kernel_config.py $IPYTHONDIR/profile_default/ipython_kernel_config.py

# Install git hooks
pre-commit install

echo ""
echo "Qiskit Textbook setup complete!"
