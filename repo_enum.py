#!/usr/bin/env python
# repo_enum.py
# Author: Sam Best

import os
import argparse
import tarfile
import urllib2
import json

class RepoEnum:
    def __init__(self):
        self._parser = argparse.ArgumentParser(description='Counts the number of lines of code in a Github repository.')
        self._args = []
        self._parseArgs()

    def _parseArgs(self):
        self._parser.add_argument('-r', dest='repo', action='append',
                                  help="Repo location in the format 'user/repo'")
        self._args = self._parser.parse_args()

        for a in self._args.repo:
            assert a.find('/') != -1

    def _getRepoLang(self, repo):
        url = ""


    def _buildUrl(self, repo, urlType):
        """Returns a URL for retrieving data from github

        Valid options for urlType:
            repolanguages

        """
        username = repo[:repo.find('/')]
        reponame = repo[repo.find('/')+1:]

        if urlType == 'repolanguages':
            return os.path.join("https://api.github.com/repos/", username, reponame, "languages")

        else:
            return None

    def countRepos(self):
        for r in self._args.repo:
            print self._getRepoLang(r)

if __name__ == '__main__':
    test = RepoEnum()
    test.countRepos()

