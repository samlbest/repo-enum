repo-enum
=========

This Python script counts the total lines of code in a Github repository or set of repos.

Distribution of code lines by programming language is displayed, along with the total.

## Installation

1. Install PyYAML if not already installed:

* Download version suitable for your OS at http://pyyaml.org/wiki/PyYAML
* Install:

  **Linux:**
  * Navigate to location of PyYAML-x.yy.tar.gz
  * Extract archive: ```tar xvf PyYAML-x.yy.tar.gz```
  * Navigate to newly created folder.
  * Run setup:
      sudo python setup.py install

  **Windows:**
  * Run PyYAML installer.

2. Clone repo:

```git clone https://github.com/samlbest/repo-enum.git```

3. Navigate to new repo-enum directory.

## Usage
    python repo_enum.py -r samlbest/repo-enum -r user/repo

### Options
* ```-r```: Add a repository to be enumerated.
