#!/bin/sh

# === Warning: this is for maintainers only ===
# This script packages the repo for a 'meta release', which includes only the
# information needed to build qiskit.org/learn.
# To use, make a new branch with 'release-meta' in the name (e.g.
# v2.1.3-release-meta) and run this script.

if [ "$(git branch --show-current)" != *"release-meta"* ]; then
    echo "Commit your changes and switch to a new branch with 'release-meta' in"
    echo "the name to generate a meta release."
    exit 1
fi

rm -r ./tests
rm -r ./environment
rm ./README.md
rm ./install.sh
find ./notebooks -type f -not -path "./notebooks/**/overview/**" -not -name 'toc.yaml' -delete
find ./notebooks -type d -empty -delete
mv notebooks/* notebooks/.* .
rm -r ./notebooks

cat > README.md << EOF
# Qiskit Textbook metadata

This folder contains the meta-information associated with the Qiskit
Textbook required to build https://qiskit.org/learn

To view the textbook repo, go to https://github.com/Qiskit/textbook
EOF
