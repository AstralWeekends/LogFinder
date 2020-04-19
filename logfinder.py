import os
from pathlib import Path
import fnmatch
import re

def hunt(workorder, packbatch, masterbatch, environ, prodpath, testpath):
    # Create a list of file regexes to use for search, read in from external file.
    with open('log-regex.txt', 'r') as file:
        fileregex = file.read().splitlines()

    # TO DO: Set absolute path based on environment selected. Could update to read path parameters from a file instead.
    if environ == 'Test':
        searchdir = testpath
    elif environ == 'Prod':
        searchdir = prodpath

    # Create a list of files in the directory which match one of the regexes in log-regex.txt
    filelist = []
    for regex in fileregex:
        for file in os.listdir(searchdir):
            if fnmatch.fnmatch(file, regex):
                filelist.append(str(searchdir/file))

    # Check to make sure at least 1 file in the directory matched a file regex:
    if len(filelist) < 1:
        print("There were no matching service files found.\n" +
            "Please modify log-regex.txt to include additional search strings if needed.")
        quit()

    # Write contents of files matching target regex to a dictionary {content_of_file: absolute_path_to_file}:
    filecontents = dict()
    for file in filelist:
        with open(file) as f:
            filedata = f.read().split(", ")
            filecontents.update({str(filedata): file})

    # Create regular expressions out of workorder, packbatch, and masterbatch
    regex_list = []
    if workorder != '':
        regex_list.append(re.compile(workorder))
    if packbatch != '':
        regex_list.append(re.compile(packbatch))
    if masterbatch != '':
        regex_list.append(re.compile(masterbatch))

    # Iterate through each regex and use it to search in each candidate file for a match.
    results = []
    for regex in regex_list:
        for text in filecontents:
            if re.search(regex, text):
                results.append(filecontents.get(text))

    return(results)