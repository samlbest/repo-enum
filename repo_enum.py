"""Downloads a Github repository and generates a report about the lines of code for each language."""

import os
import shutil
import contextlib
import tempfile
import argparse
import zipfile
import urllib2
import json

import yaml

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

        url = self._buildUrl(repo, 'repolanguages')

        #Fetch JSON Object containing languages used in repo from Github
        userAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':userAgent,}
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)

        result = json.load(response)

        #If "message" present in Github's response, error occurred:
        if "message" in result:
            return None

        #Return list of languages:
        return result.keys()


    def _buildUrl(self, repo, urlType):
        """Returns a URL for retrieving data from github

        Valid options for urlType:
            repolanguages
            repozip
        """

        #Parse username and repo name from argument:
        username = repo[:repo.find('/')]
        reponame = repo[repo.find('/')+1:]

        #Build URL corresponding to urlType arg:
        if urlType == 'repolanguages':
            return os.path.join("https://api.github.com/repos", username, reponame, "languages").replace("\\", "/")

        elif urlType == 'repozip':
            #Retrieve zip location for master branch
            return os.path.join("https://github.com", username, reponame, "zipball", "master").replace("\\", "/")

        else:
            raise Exception("Invalid URL type.\nValid options: repolanguages, repozip")

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

        return response

    def _retrieveRepo(self, repo, repodir):
        """Retrieves files from repository, stores in temp directory"""
        url = self._buildUrl(repo, 'repozip')

        #Download file from github:
        userAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':userAgent,}
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)

        data = response.read()
        with open(os.path.join(repodir, "temp.zip"), "wb") as output:
            output.write(data)

        #zipFile, headers = urllib.urlretrieve(url, os.path.join(repodir, "temp.zip"))
        return os.path.join(repodir, "temp.zip")

    @contextlib.contextmanager
    def _tempdir(self):
        """Creates a temp directory which will be deleted automatically"""
        tmpdir = tempfile.mkdtemp()
        try:
            yield tmpdir
        finally:
            shutil.rmtree(tmpdir)

    def _extractZip(self, repozip, extractTo):
        """Extracts zipfile 'repozip' to directory 'extractTo'"""
        if zipfile.is_zipfile(repozip):
            z = zipfile.ZipFile(repozip)
            z.extractall(extractTo)
            return z.namelist()
        return None

    def _countFileLines(self, filepath):
        f = open(filepath, 'r')

        #Creates enumeration from lines in file
        for i, l in enumerate(f):
            pass

        return i+1

    def _displayReport(self):
        """Displays a formatted report of line counts of all programming languages found in repos"""
        for ko, vo in self._repos.iteritems():
            total = self._repos[ko]['total']
            print "Repository: ", ko
            for k, v in vo.iteritems():
                print "*%s: %d %.2f%%" % (k, v,  100.0*v/total)
            print "-"*50

    def countRepos(self):
        """Counts files and generates a report for each programming language"""
        for r in self._args.repo:
            try:
                langs = self._updateLangDict(r)
            except Exception as e:
                print "Error processing repo ["+ r +"]\nServer response: ",e
                continue

            with self._tempdir() as tempdir:
                #Retrieve zip file:
                print "Downloading repository:", r + "..."
                try:
                    repozip = self._retrieveRepo(r, tempdir)
                except Exception as e:
                    print "Error retrieving zip file\nServer response: ",e
                    continue

                #Extract zip file:
                try:
                    repoFiles = self._extractZip(repozip, tempdir)
                except Exception as e:
                    print "Error extracting zip file\nMessage: ",e
                    continue

                self._repos[r]['total'] = 0 #Track total number of lines

                #Create list of files (excluding directories):
                fileList = [os.path.join(tempdir, f) for f in repoFiles if not os.path.isdir(os.path.join(tempdir, f))]

                #TODO: create option to count all files, selective extensions, etc
                if True:
                    #Load GitHub languages yaml:
                    langRef = yaml.load(open("languages.yml", 'r'))

                    for f in fileList:
                        ext = os.path.splitext(f)[1]

                        #Check if extension is valid for each language contained in repo:
                        for l in langs:
                            if ext == "":
                                continue
                            elif ext not in langRef[l]['primary_extension']:
                                if 'extensions' not in langRef[l].keys() or ext not in langRef[l]['extensions']:
                                    continue

                            #Add file line count to self._repos
                            count = self._countFileLines(f)
                            self._repos[r]['total'] += count
                            self._repos[r][l] += count

        self._displayReport()

if __name__ == '__main__':
    repoenum = RepoEnum()
    repoenum.countRepos()
