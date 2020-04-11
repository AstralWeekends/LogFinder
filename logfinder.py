import os
import fnmatch
import re

def testmethod(wo_num, pb_num, mb_num):
    print("Work Order: " + wo_num)
    print("Package Batch: " + pb_num)
    print("Master Batch: " + mb_num)

def mainmethod():
    # Create a list of file regexes to use for search, read in from external file.
    with open('/home/alec/Documents/Python/Log-Finder/log-regex.txt', 'r') as file:
        fileregex = file.read().splitlines()

    # Prompt user for needed inputs to run the search:
    workorder = input("Enter the WO: ")
    packbatch = input("Enter the Package Batch: ")
    masterbatch = input("Enter the Master Batch: ")
    environ = input("Enter the Environment ('Test' or 'Prod'): ")[0].lower()

    # TO DO: Set absolute path based on environment selected. Could update to read path parameters from a file instead.
    if environ == 't':
        searchdir = '/home/alec/Documents/Python/Log-Finder/Test/'
    elif environ == 'p':
        searchdir = '/home/alec/Documents/Python/Log-Finder/Prod/'

    trigger = input("Ready to search ('y' or 'n')?: ").lower()

    # Create a list of files in the directory which match one of the regexes in log-regex.txt
    if trigger == 'y':
        filelist = []
        for regex in fileregex:
            for file in os.listdir(searchdir):
                if fnmatch.fnmatch(file, regex):
                    filelist.append(searchdir + file)
    else:
        quit()

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
    workorder_regex = re.compile(workorder)
    packbatch_regex = re.compile(packbatch)
    masterbatch_regex = re.compile(masterbatch)
    regex_list = [workorder_regex, packbatch_regex, masterbatch_regex]

    # Iterate through each regex and use it to search in each candidate file for a match.
    results = []
    for regex in regex_list:
        for text in filecontents:
            if re.search(regex, text):
                results.append(filecontents.get(text))

    # Check if any results - if there are, remove duplicates from result list.
    if len(results) == 0:
        print("Search complete, no logs found.")
    else:
        results = list(dict.fromkeys(results))

    print(results)

#mainmethod()