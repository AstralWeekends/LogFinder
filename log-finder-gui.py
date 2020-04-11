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
            [sg.Button('Run'), sg.Button('Cancel')] ]

# Create actual window to display
window = sg.Window('Log Finder', layout, location=(500,275)) #note: location of window specific to this computer.

# Event loop
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    if event == 'Run':
        logfinder.testmethod(values['_WO_'], values['_PACKBATCH_'], values['_MASTERBATCH_'])

window.close()