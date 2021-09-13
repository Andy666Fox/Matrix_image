import PySimpleGUI as sg


def set_params_window():
    layout = [[sg.Text('                     MATRIX IMAGE')],
              [sg.Text('Enter path to file:'), sg.InputText()],
              [sg.Text('Enter symbols size:'), sg.InputText()],
              [sg.Button('OK')]]
    
    window = sg.Window('MATRIX IMAGE', layout, (20,300))      
    

    event, values = window.read()    
    window.close()

    path = values[0]  
    size = values[1]  if type(values[1]) == int else 7
    
    if event[0]:
        window.close()
        
    return path, size


def error_popup():
    layout = [[sg.Text('OOPSY')],
              [sg.Text('Error detected\nCheck the correctness of the entered data')],
              [sg.Button('OK')]]
    
    window = sg.Window('ERROR', layout)
    
    event, _ = window.read()
    
    if event[0]:
        window.close()
        

    
    

