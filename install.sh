# # Setup Python venv and install packages
echo "\nSetting up Python virtual environment in ./.venv\n"
python3.8 -m venv ./.venv
source .venv/bin/activate
python3.8 -m pip install -r environment/requirements.txt

# # Create default profile, then copy over our custom settings
export IPYTHONDIR="./environment/ipython"
echo "\n\nCreating new ipython profile at ${IPYTHONDIR}"
ipython profile create
cp ./environment/ipython/ipython_kernel_config.py $IPYTHONDIR/profile_default/ipython_kernel_config.py

if command -v direnv &> /dev/null
then
    echo "direnv is installed; navigating to this directory will "
    echo "automatically activate this environment."
    direnv allow .envrc
else
    echo "direnv is not installed; you'll need to manually set up your environment"
    echo "and activate it whenever you want to work on the textbook. See README.md"
    echo "for details"
    # Deactivate in case user doesn't understand they're in a venv and can't
    # escape (direnv won't leave automatically when they navigate away).
    deactivate  
fi

echo "\nQiskit Textbook setup complete!\n"
