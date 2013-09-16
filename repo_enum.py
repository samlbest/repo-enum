#!/usr/bin/env python
# repo_enum.py
# Author: Sam Best

import time
import sys

import os
import argparse
import tarfile
import urllib2
import json

REPO_TEMPDIR = "repocontents"

class RepoEnum:
    def __init__(self):
        self._parser = argparse.ArgumentParser(description='Counts the number of lines of code in a Github repository.')
        self._args = []
        self._repos = {}
        self._parseArgs()

    def _parseArgs(self):
        """Parse command line arguments and ensure their validity."""
        self._parser.add_argument('-r', dest='repo', action='append',
                                  help="Repo location in the format 'user/repo'")
        self._args = self._parser.parse_args()

        for a in self._args.repo:
            assert a.find('/') != -1

    def _getRepoLang(self, repo):
        """Returns the languages contained in the repo as a list"""

        #Fetch JSON Object containing languages used in repo from Github
        url = self._buildUrl(repo, 'repolanguages')
        gitJson = urllib2.urlopen(url)
        result = json.load(gitJson)

        #If "message" present in Github's response, error occurred:
        if "message" in result:
            return None

        #Return list of languages:
        return result.keys()


    def _buildUrl(self, repo, urlType):
        """Returns a URL for retrieving data from github

        Valid options for urlType:
            repolanguages

        """

        #Parse username and repo name from argument:
        username = repo[:repo.find('/')]
        reponame = repo[repo.find('/')+1:]

        #Build URL corresponding to urlType arg:
        if urlType == 'repolanguages':
            return os.path.join("https://api.github.com/repos/", username, reponame, "languages")

        else:
            raise Exception("Invalid URL type.\nValid options: repolanguages")

    def _updateLangDict(self, repo):
        """Calls self._getRepoLang to query Github API, updates self._repos with results"""
        response = self._getRepoLang(repo)
        if not response:
            raise Exception("Not a valid repository")

        #Add repository to self._repos dictionary
        if repo not in self._repos.keys():
            self._repos[repo] = {}

        #Add languages to repo's subdictionary
        for lang in response:
            if lang not in self._repos[repo].keys():
                self._repos[repo][lang] = 0

    def _retrieveRepo(self, repo):
        """Retrieves files from repository, stores in temp directory"""

    def countRepos(self):
        for r in self._args.repo:
            #self._repos[r] = collections.defaultdict
            try:
                self._updateLangDict(r)
            except Exception as e:
                print "Error processing repo ["+ r +"]\nServer response: ",e
                continue

if __name__ == '__main__':
    test = RepoEnum()
    test.countRepos()

