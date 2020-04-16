import PySimpleGUI as sg
import shelve
import logfinder
from pathlib import Path

'''shelfFile = shelve.open(str(Path('shelf/prodpath')))
prodPath = Path('Prod/')
shelfFile['prodPath'] = str(prodPath)
shelfFile.close()

shelfFile = shelve.open(str(Path('shelf/prodpath')))
print(list(shelfFile.values()))
shelfFile.close()

quit()'''

# color theme, use sg.theme_previewer() to see all theme options
sg.theme('BrightColors')

menu_def = [ ['File', ['Exit']],
            ['Edit', ['Search Paths']] ]

layout = [  [sg.Menu(menu_def)],
            [sg.Text("Work Order #:")],
            [sg.InputText(key='_WO_')],
            [sg.Text("Package Batch #:")],
            [sg.InputText(key='_PACKBATCH_')],
            [sg.Text("Master Batch #:")],
            [sg.InputText(key='_MASTERBATCH_')],
            [sg.Text("Environment:"), sg.Combo(['Prod', 'Test'], key='_ENVIRONMENT_', default_value='Prod')],
            [sg.Button('Run'), sg.Button('Cancel')],
            [sg.Text("Output:")], 
            [sg.Output(size =(90, 10), key='_OUTPUT_')],
            [sg.Button('Clear')]  ]


# Create actual window to display
window = sg.Window('Log Finder', layout, location=(500,275)) #note: location of window specific to this computer.

# Event loop
while True:
    event, values = window.read()
    if event in (None, 'Cancel', 'Exit'):
        break
    
    if event == 'Run':
        if (values['_WO_'] == '' and values['_PACKBATCH_'] == '' and values['_MASTERBATCH_'] == ''):
            print('Nothing to find.')
        else:
            results = logfinder.hunt(values['_WO_'], values['_PACKBATCH_'], values['_MASTERBATCH_'], values['_ENVIRONMENT_'])
            results = list(dict.fromkeys(results))
            if len(results) == 0:
                print("No results found")
            else:
                print(results)
    
    #elif event == 'Search Paths':
    elif event == 'Clear':
        window.FindElement('_OUTPUT_').Update('')


window.close()