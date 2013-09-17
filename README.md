repo-enum
=========

This Python script counts the total lines of code in a Github repository or set of repos.

Distribution of code lines by programming language is displayed, along with the total.

## Installation

### Install PyYAML if not already installed:

  * Download version suitable for your OS at http://pyyaml.org/wiki/PyYAML

  **Linux:**
    * Navigate to location of ```PyYAML-x.yy.tar.gz```
    * Extract archive: ```tar xvf PyYAML-x.yy.tar.gz```
    * Navigate to newly created directory.
    * Run setup:
      ```sudo python setup.py install```

    **Windows:**
      * Run PyYAML installer.

### Clone repo:
  * ```git clone https://github.com/samlbest/repo-enum.git```
  * Run tool from new repo-enum directory.

## Usage
    python repo_enum.py -r samlbest/repo-enum -r [github-user]/[reponame] -r [...]

## Options
* ```-r```: Add a repository to be enumerated.

## Planned features
* More options for specifying file extensions.
* Option for displaying file-by-file breakdown in _displayReport()
* Web app version.
