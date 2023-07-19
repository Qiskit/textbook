# Qiskit Textbook content

> :warning: Unfortunately **we can't accept new pages to the textbook**. If you
> have something you want to share with the community, we highly recommend you
> self-publish. If you need help with self-publishing, or want feedback on your
> work, contact Frank Harkins on the
> [Qiskit Slack workspace](https://qisk.it/join-slack).

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

Windows users should use [Git Bash](https://gitforwindows.org/) and Python version > 3.8 and < 3.11.

```sh
bash install.sh
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
## Bibtex citation
```
@book{qiskitextbook2023,   
    author = {various authors},   
    year = {2023},   
    title = {Qiskit Textbook},   
    publisher = {Github},   
    url = {https://github.com/Qiskit/textbook}, 
}
```
