import PySimpleGUI as sg
import logfinder

# color theme, use sg.theme_previewer() to see all theme options
sg.theme('BrightColors')

layout = [  [sg.Text("Work Order #:")],
            [sg.InputText(key='_WO_')],
            [sg.Text("Package Batch #:")],
            [sg.InputText(key='_PACKBATCH_')],
            [sg.Text("Master Batch #:")],
            [sg.InputText(key='_MASTERBATCH_')],
            [sg.Text("Environment:"), sg.Combo(['Prod', 'Test'], key='_ENVIRONMENT_', default_value='Prod')],
            [sg.Button('Run'), sg.Button('Cancel')] ]

# Create actual window to display
window = sg.Window('Log Finder', layout, location=(500,275)) #note: location of window specific to this computer.

# Event loop
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    if event == 'Run':
        results = logfinder.mainmethod(values['_WO_'], values['_PACKBATCH_'], values['_MASTERBATCH_'], values['_ENVIRONMENT_'])
        if len(results) == 0:
            print("Search complete, no logs found.")
        else:
            results = list(dict.fromkeys(results))
            print(results)
window.close()