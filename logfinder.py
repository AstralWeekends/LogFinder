import os
from os import path
from pathlib import Path
import fnmatch
import re
import shelve

def hunt(workorder, packbatch, masterbatch, environ, prodpath, testpath):
    # Create a list of file regexes to use for search, read in from external file.
    shelfFile = shelve.open((str(Path('shelf/file-regexes'))))
    fileregex = list(shelfFile.values())
    fileregex = [y for x in fileregex for y in x.split('\n')]
    fileregex.pop(-1)
    shelfFile.close()

    if environ == 'Test':
        searchdir = testpath
    elif environ == 'Prod':
        searchdir = prodpath

    # Create regular expressions out of workorder, packbatch, and masterbatch
    regex_list = []
    if workorder != '':
        regex_list.append(re.compile(workorder))
    if packbatch != '':
        regex_list.append(re.compile(packbatch))
    if masterbatch != '':
        regex_list.append(re.compile(masterbatch))

    # Create a list of files in the directory which match one of the regexes in log-regex.txt
    filelist = []
    for regex in fileregex:
        for file in os.listdir(searchdir):
            if fnmatch.fnmatch(file, regex):
                filelist.append(str(searchdir + '/' + file))

    # Check to make sure at least 1 file in the directory matched a file regex:
    if len(filelist) < 1:
        return

    # Write contents of files matching target regex to a dictionary {content_of_file: absolute_path_to_file}:
    filecontents = dict()
    for file in filelist:
        with open(file) as f:
            filedata = f.read().split(", ")
            filecontents.update({str(filedata): file})

    # Iterate through each regex and use it to search in each candidate file for a match.
    results = []
    progress_counter = len(filecontents)
    for regex in regex_list:
        for text in filecontents:
            progress_counter = progress_counter - 1
            print(progress_counter)
            if re.search(regex, text):
                results.append(filecontents.get(text))

    return(results)


#Returns current list of regexes to window3.
def listrefresh():
    shelfFile = shelve.open((str(Path('shelf/file-regexes'))))
    filelist = list(shelfFile.values())
    shelfFile.close()
    refreshed = ('\n'.join(filelist))
    return(refreshed.rstrip('\n'))

#Writes current content of window when user presses 'Save List' in window3.
def listsave(list_input):
    shelfFile = shelve.open((str(Path('shelf/file-regexes'))))
    shelfFile['list_input'] = list_input
    shelfFile.close()

#Writes values of prod/test paths when users presses 'Ok' in window2.
def savepaths(prodpath, testpath):
    pathShelf = shelve.open((str(Path('shelf/paths'))))
    pathShelf['prodpath'] = prodpath
    pathShelf['testpath'] = testpath
    pathShelf.close()

#When user starts program or saves new paths in windows2, gets new path values for program.
def pullpaths():
    if path.exists(Path('shelf/paths')):
        pathShelf = shelve.open((str(Path('shelf/paths'))))
        prodpath = pathShelf['prodpath']
        testpath = pathShelf['testpath']
        pathShelf.close()

    elif os.name == 'posix':
        base_path = os.getcwd()    
        prodpath = base_path/Path('Prod/')
        testpath = base_path/Path('Test/')

    else:
        prodpath = Path('//scanprodfs1/Services/_Logs')
        testpath = Path('//scantestapps1/Services/_Logs')
    
    paths = [prodpath, testpath]
    return(paths)

