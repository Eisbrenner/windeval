
[![Linter](https://github.com/windeval/windeval/workflows/Lint/badge.svg)](https://github.com/windeval/windeval/actions?query=workflow%3ALint)
[![Tests](https://github.com/windeval/windeval/workflows/Test/badge.svg)](https://github.com/windeval/windeval/actions?query=workflow%3ATest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/windeval/windeval/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Wind-Product Evaluation Toolkit

## Installation

```bash
$ git clone <repo>
$ cd <repo>
$ pip install .
```

> **Note: publishing on PyPI is conisered; thus installation using `pip install windeval`
> might be possible one day.**

## Usage

Start the locally run minimal web-app with

```python
>>> from windeval import app
>>> app()
```

## Development

windeval is developed using [Poetry](https://github.com/python-poetry/poetry).

### Download windeval package

```bash
$ git clone <repo>
```

### Install [Poetry](https://github.com/python-poetry/poetry)

```bash
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Install package

```bash
$ cd <repo>
$ poetry install
```

### Test environment by running tests

```bash
$ poetry run pytest
```
