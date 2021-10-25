# Chess Tournament Tree Generator

This project is a chess tournament tree generator using the swiss pairing system.

## Installation

clone the project using GitHub CLI

```bash
gh repo clone gichter/p4
```

Open a terminal in the root folder, then create a new virtual environment

```bash
python3 -m venv env
```

Activate the virtual environment
```bash
source env/bin/activate
```

Use the packet manager [pip](https://pip.pypa.io/en/stable/) to install the project dependencies

```bash
pip install -r requirements.txt
```

Launch the script

```bash
python3 chess/main.py
```

Generate flake8 report

```bash
flake8 chess --format=html --htmldir=flake-report
```
