# This script runs 'prose linting' checks on the notebooks.
# This includes spell checking and writing best practices.
# Requires Vale (https://vale.sh/docs/vale-cli/installation/)
# and nbQA (pip install nbqa).

cd notebooks

notebooks=$(find . -name "*.ipynb" -not -name "*checkpoint*")

python -m nbqa vale ${notebooks} --nbqa-shell --nbqa-md
