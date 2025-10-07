# drstorage

[![GitHub Project](https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub)](https://github.com/kratsg/drstorage)
[![GitHub Actions Status: CI](https://github.com/kratsg/drstorage/workflows/CI/badge.svg?branch=master)](https://github.com/kratsg/drstorage/actions?query=workflow%3ACI+branch%3Amaster)
[![Code Coverage](https://codecov.io/gh/kratsg/drstorage/graph/badge.svg?branch=master)](https://codecov.io/gh/kratsg/drstorage?branch=master)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/kratsg/drstorage/master.svg)](https://results.pre-commit.ci/latest/github/kratsg/drstorage/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Using

From python

```pycon
>>> import drstorage
>>> data = bytearray.fromhex(
...     "abab00471200c5120901000000000000000a10025810000000000000140d0a"
... )
>>> result = drstorage.models.F1_600.parse(data)
>>> print(result)
Container:
    humidity = 7.1
    temperature = 19.7
    model = 600

```

or from command line

```bash
$ python -c 'import sys; sys.stdout.buffer.write(bytes(bytearray.fromhex("abab00471200c5120901000000000000000a10025810000000000000140d0a")))' | drstorage parse --model F1_600
Container:     humidity = 7.1    temperature = 19.7    model = 600
```

### Supported Models

- `generic` (default, the "base" Dr. Storage model)
- `F1_600`
- `F1_1200`
- `X2M_157`

## Installation

In a fresh virtual environment

```
$ python -m pip install "git+https://github.com/kratsg/drstorage.git"
```

The above is actually cloning and installing directly from the Git repository.
However, if you want to, you can of course also install it directly from the Git
repository "locally" by first cloning the repo and then from the top level of it
running

```
$ python -m pip install .
```

## Contributing

As this library is experimental contributions of all forms are welcome. You are
of course also most welcome and encouraged to open PRs.

### Developing

To develop, use a virtual environment. Once the environment is activated, clone
the repo from GitHub

```
git clone git@github.com:kratsg/drstorage.git
```

and install all necessary packages for development

```
python -m pip install --ignore-installed --upgrade -e .[complete]
```

Then setup the Git pre-commit hooks by running

```
pre-commit install
```

## Acknowledgements

- Mike Hance
- Noah Peake
- Will Johansson
- James Tranovich
- Anja Berens
- Paul Ingemi
- Matthew Gignac
