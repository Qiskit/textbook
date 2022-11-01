#!/usr/bin/env bash
# This script runs pylint on each notebook in NB_PATHS

NB_ROOT="./notebooks"
NB_PATHS="./tests/notebook_paths.txt"

while read line
do
    if [ -z "$line"  ] ; then
        # blank line
        continue
    elif [[ $line = \#* ]] ; then
        echo "Skipping: ${line}"
    else
        echo "Lint check: ${line}.ipynb"
        nbqa pylint --rcfile="${NB_ROOT}/.pylintrc" --fail-under=10 "${NB_ROOT}/${line}.ipynb" || exit 1
    fi
done < "$NB_PATHS"
