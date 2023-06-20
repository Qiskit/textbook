# Qiskit Textbook content

This is the repository for the Qiskit Textbook's content. This page is for
people that want to report issues, or contribute to the Textbook, if you just
want to read about quantum computing, go to [the textbook
webpage](https://qiskit.org/learn/).

If you've found a problem in the textbook, please [make a new
issue](https://github.com/Qiskit/textbook/issues/new/choose).

## Contributing

OSX/Linux users can quickly set up by running

```sh
./install.sh
source .venv/bin/activate
```

then
```sh
python -m jupyter notebook
```

Windows Users can quickly set up by using the following steps.
1st. you need a compiler to run bash commands. You can use the Git Bash for this purpose.
2nd. The following steps are tested for Python 3.11,3.10,3.9, and 3.8. Installation was successful for any python version except the Python 3.11.

```sh
bash install-win.sh
source .venv/Scripts/activate
```

then
```sh
python -m jupyter notebook
```

For a more detailed guide, please check out the
[contributing document](./CONTRIBUTING.md).


## Versioning

We're constantly updating and improving the textbook, but some users find
changes disruptive. For this reason, we release the Textbook content in
_versions_, which are snapshots of the content that cannot change.

The version number tells you what kind of changes have been made from the
previous version. This repo follows a kind of [semantic
versioning](https://semver.org/), adapted to make more sense for non-code
repos.

For a verision number `MAJOR.MINOR.PATCH`, we will increment the:

- `MAJOR` version when changes remove or replace content,
- `MINOR` version for changes that add content, or that do not significantly
  alter the structure of existing pages. Examples include
    - adding new pages,
    - rewording paragraphs for clarity, and
    - small changes to code to make it work with newer Qiskit versions.
- `PATCH` version increments are for 'bugfixes' only. Examples include fixing
    - typos,
    - statements that are incorrect, and
    - code that does not work correctly with the version of Qiskit advertised
      on the page.

For example, if you're teaching using `v1.0.3`, you know you can switch to any
`v1.0.x` version without sections disappearing or code breaking with your
existing setup.
