# Quantum Music Project
The goal of this project is to design an alternative way for anyone interested in quantum computing to experience quantum state evolution through music.

## Features
- Intuitive user interface via Jupyter Notebooks
- Optional tutorial with an overview of Quantum Computing
- Example circuits/audio
- Playground to generate your own audio

## How To
The project is driven through Jupyter Notebooks. If you haven't use Jupyter Notebooks before, here is an overview of [what it is](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html) and [how to run them](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html) from the documentation.

Once you are able to run Jupyter Notebooks on your system, you can start running the notebooks in the repository.

## Directory Structure
* `Notebooks/`: code of our learning on Qiskit and audio in a Jupyter Notebook
* `Quantum-Music/`: the Python package for users to use. Note that everything in this directory will be available to the public!

## Quantum-Music Installation
### Install locally from this repository
To install the `quantum-music` package locally, go to `Quantum-Music/` in this repository, then run:
```
pip install -e .
```
This will also install other Python packages that are required for `quantum-music` to run.

Once installed, the functions in `quantum-music` can be imported and directly called:
```
from quantum_music.circuit_functions import *
```

Note that in Python code `quantum_music` (note the underscore `_` in the name) should be used, but when installing the package use the name `quantum-music` (with a hyphen `-`). This will install the state of the code as is in the repository.

### Install in [Quantum Lab](https://quantum-computing.ibm.com/lab/)
Install the latest published version in the Jupyter notebook:
```
! pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple quantum-music
```

## Publish to Test PyPI
When our Python package is uploaded to Test PyPI, the package can be used locally or in Quantum Lab. First you need an [account on Test PyPI](https://test.pypi.org/account/register/ ) then create an [API token](https://test.pypi.org/manage/account/#api-tokens). You should also setup your PyPI credentials (`.pypirc` file) locally to automatically use your token. See [How can I use API tokens to authenticate with PyPI?](https://test.pypi.org/help/#apitoken).


The official documentation for packaging Python projects can be viewed at https://packaging.python.org/tutorials/packaging-projects/.

1. Update the version number in `setup.cfg` (use [semantic versioning](https://semver.org/)):
```
[metadata]
name = quantum-music
version = # Update the version on this line, for example: 0.2.0
author = SuperComposers
```
2. Commit and push the version number change to Git
3. In Github (through the web browser), go to `releases` and then go to `Draft a new release`.
4. In `Tag version` field and the `Release Title` field, use the same version from Step 1 but prefix the version with `v`. For example, if the version is `0.2.0`, then in the `Tag version` and `Release Title` field, type in `v0.2.0`.
5. Then click `Publish Release`.
6. In the terminal, go to the local copy of this repository, then run `git fetch --all`. The new Git tag for the version (for example, `v0.2.0`) would be pulled in.
7. Checkout the the version tag (for example, for `v0.2.0`):
```
git checkout v0.2.0
```
8. Create a source distribution of the package:
```
cd Quantum-Music
python setup.py sdist
```
9. Upload to Test PyPI:
```
twine upload --repository testpypi dist/*
```
