from lib2to3.pygram import Symbols
import PySimpleGUI as sg


# Dictionary with symbols flags (more in ReadMe)
codecs = {'ascii': '!"#$%&()*+,-./', 'digit': '0123456789',  'arrow': '-><-', 'dollar': '$$$', 'author': 'godovorez', 'uwu': '(UwU)'}

def set_params_window():
    
    """Function of the main dialog box and transfer of the entered data to the main file

    Returns:
        [str]: The path to the file entered by the user
        [int]: User-entered character size
        [str]: Symbols to display (Optional, see Readme)
        
    """
    
    layout = [[sg.Text('                     MATRIX IMAGE')],
              [sg.Text('Enter path to file: '), sg.InputText()],
              [sg.Text('Enter symbols size: '), sg.InputText()],
              [sg.Text('Enter symbols(optional): '), sg.InputText()],
              [sg.Button('OK')]]
    
    
    window = sg.Window('MATRIX IMAGE', layout, (20,300))      
    

    event, values = window.read()    
    window.close()

    path = values[0]  
    size = values[1]

    
    # Check to special flag available
    
    if values[2].lower() in codecs:
        symbols = codecs[values[2]]
    else:
        symbols = [elem for elem in values[2].replace(' ', '')]
    
    if event[0]:
        window.close()
        
    return path, int(size), symbols


def error_popup():
    layout = [[sg.Text('OOPSY')],
              [sg.Text('Error detected\nCheck the correctness of the entered data')],
              [sg.Button('OK')]]
    
    window = sg.Window('ERROR', layout)
    
    event, _ = window.read()
    
    if event[0]:
        window.close()
        

    
    

