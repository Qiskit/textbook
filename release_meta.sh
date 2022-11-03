#!/bin/sh

# === Warning: this is for maintainers only ===
# This script packages the repo for a 'meta release', which includes only the
# information needed to build qiskit.org/learn.
# To use, commit your changes, and make a new branch with 'release-meta' in the
# name (e.g. v2.1.3-release-meta) and run this script.

echo "\nWarning: This script will destroy any un-committed work. Please make sure"
echo "you have committed all changes, and are on a dedicated meta-release branch with"
echo "no untracked files.\n"

read -p "Would you like to proceed? (n/y) " -r
echo

if [[ $REPLY != "y" ]]; then
    echo "Exiting with no changes."
    exit 1
fi

rm -r tests
rm -r environment
rm -r .github
rm README.md install.sh .vale.ini .pre-commit-config.yaml .envrc 
find notebooks -type f -not -path "**/overview/**" -not -name 'toc.yaml' -delete
find notebooks -type d -empty -delete
mv ./notebooks ./content

cat > README.md << EOF
# Qiskit Textbook metadata

This folder contains the meta-information associated with the Qiskit
Textbook required to build https://qiskit.org/learn

To view the textbook repo, go to https://github.com/Qiskit/textbook
EOF

cat > package.json << EOF
{
  "name": "qiskit-textbook-meta",
  "version": "x.x.x"
}
EOF

nvim package.json +3

rm release_meta.sh

git add .
rm .gitignore && git add .gitignore
git commit --no-verify
echo "Committed and ready to push."
