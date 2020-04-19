import PySimpleGUI as sg
import logfinder
from pathlib import Path
import os
import shelve

'''shelfFile = shelve.open(str(Path('shelf/prodpath')))
prodPath = Path('Prod/')
shelfFile['prodPath'] = str(prodPath)
shelfFile.close()

shelfFile = shelve.open(str(Path('shelf/prodpath')))
print(list(shelfFile.values()))
shelfFile.close()

quit()'''

#Set default search paths based on OS.
if os.name == 'posix':
    base_path = os.getcwd()    
    prodpath = base_path/Path('Prod/')
    testpath = base_path/Path('Test/')
else:
    prodpath = Path('//scanprodfs1/Services/_Logs')
    testpath = Path('//scantestfs1/Services/_Logs')

# color theme, use sg.theme_previewer() to see all theme options
sg.theme('BrightColors')

menu_def = [ ['File', ['Exit']],
            ['Edit', ['Preferences']] ]

layout = [  [sg.Menu(menu_def)],
            [sg.Text("Work Order #:")],
            [sg.InputText(key='_WO_')],
            [sg.Text("Package Batch #:")],
            [sg.InputText(key='_PACKBATCH_')],
            [sg.Text("Master Batch #:")],
            [sg.InputText(key='_MASTERBATCH_')],
            [sg.Text("Environment:"), sg.Combo(['Prod', 'Test'], key='_ENVIRONMENT_', default_value='Test')],
            [sg.Button('Run'), sg.Button('Reset')],
            [sg.Text("Output:")], 
            [sg.Output(size =(90, 10), key='_OUTPUT_')],
            [sg.Button('Clear')]  ]

# Create actual window to display
window1 = sg.Window('Log Finder', layout)
window2_active = False
window3_active = False

# Event loop
while True:
    event1, values1 = window1.read()
    if event1 in (None, 'Exit'):
        break
    if event1 == 'Run':
        if (values1['_WO_'] == '' and values1['_PACKBATCH_'] == '' and values1['_MASTERBATCH_'] == ''):
            print('Nothing to find.')
        else:
            results = logfinder.hunt(values1['_WO_'], values1['_PACKBATCH_'], values1['_MASTERBATCH_'], values1['_ENVIRONMENT_'], prodpath, testpath)
            results = list(dict.fromkeys(results))
            if len(results) == 0:
                print("No results found")
            else:
                print('\n'.join(results))
    
    elif event1 == 'Reset':
        window1.FindElement('_OUTPUT_').Update('')
        window1.FindElement('_WO_').Update('')
        window1.FindElement('_PACKBATCH_').Update('')
        window1.FindElement('_MASTERBATCH_').Update('')

    elif event1 == 'Clear':
        window1.FindElement('_OUTPUT_').Update('')
    
    if not window2_active and event1 == 'Preferences':
        window2_active = True
            
        layout2 = [ [sg.Text('Change Search Paths:')],
                    [sg.FolderBrowse('Prod', target='_PRODPATH_'), sg.Input(key='_PRODPATH_', default_text=prodpath, disabled=True)],
                    [sg.FolderBrowse('Test', target='_TESTPATH_'), sg.Input(key='_TESTPATH_', default_text=testpath, disabled=True)],
                    [sg.Text('-'*90)],
                    [sg.Button('Modify File Search List')],
                    [sg.Text('-'*90)], 
                    [sg.Button('Ok'), sg.Button('Cancel')] ]
        
        window2 = sg.Window('Preferences', layout2, keep_on_top=True)
    
    if window2_active:
        event2, values2 = window2.Read()
        if event2 in (None, 'Cancel'):
            window2_active = False
            window2.close()

        #TO DO
        if event2 == 'Ok':
            print(os.getcwd())
            print(os.name)
            window2_active = False
            window2.close()
    
    if not window3_active and event2 == 'Modify File Search List':
        window3_active = True

        layout3 = [ [sg.Listbox(values=['File1', 'File2'], key='_FILELIST_', size=(30, 10))] ]

        window3 = sg.Window('Edit File Search List', layout3, keep_on_top=True)
    
    if window3_active:
        event3, values3 = window3.Read()
        if event3 in (None, 'Cancel'):
            window3_active = False
            window3.close()

window1.close()