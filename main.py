import json
import os

def find_file(known_path:str=None, name:str=None) -> (bool, str):
    """
    Function to find a file on the user's computer.
    :param known_path: the part of the path that is constant or known by the user.
    :param name: the name (with the extension) of the file.
    :return: the path to the file or False if the file was not found.
    """
    if os.name == 'nt': # Windows OS
        # Gettings all possible drives on which the file may be found
        hdds = [f'{drive}:{os.path.sep}' for drive in 'CDEIJKRSTVWXY' if os.path.exists(f'{drive}:{os.path.sep}')]
        
        for drive in hdds:
            this_path = f'{drive}{known_path}{os.path.sep}{name}'
            if os.path.exists(this_path):
                return this_path
        return False
    else: # Unix OS
        return False

def read_file(path:str=None) -> (dict, str):
    """
    Function to read a file.
    :param path: the full path to the file.
    :return: the content of the file.
    """
    if path == False:
        return None
    
    with open(path, 'r') as f:
        if path[-5:] == '.json':
            data = json.load(f)
        else:
            data = f.read()
    return data

# Get the LoL file where the options are saved
persisted_settings:dict = read_file(
    find_file(
        known_path=f'Riot Games{os.path.sep}League of Legends{os.path.sep}Config',
        name='PersistedSettings.json'
    )
)

# Display LoL keys types
for e in persisted_settings['files'][1]['sections']:
    print(e['name'])

# Keyboard layouts
keyboard_lines = {
    "qwerty": {
        'keys': [
            ['esc'] + [f'F{i}' for i in range(1, 13)] + ['del'],
            [c for c in '`1234567890-='] + ['back'],
            ['tab'] + [c for c in 'QWERTYUIOP[]\\'],
            ['capslk'] + [c for c in "ASDFGHJKL;'"] + ['enter'],
            ['lshift'] + [c for c in 'ZXCVBNM,./'] + ['rshift'],
            ['lctrl', 'super', 'lalt', 'space',
             'ralt', 'fn', 'menu', 'rctrl']
        ],
        'spans': {key: 2 for key in ('enter', 'lshift', 'rshift')}
    },
    'azerty': {
        'keys': [
            ['esc'] + [f'F{i}' for i in range(1, 13)] + ['del'],
            [c for c in '²&é"\'(-èçà)='] + ['back'],
            ['tab'] + [c for c in 'AZERTYUIOP^$*'],
            ['capslk'] + [c for c in "QSDFGHJKLMù"] + ['enter'],
            ['lshift'] + [c for c in 'WXCVBN,;:!'] + ['rshift'],
            ['lctrl', 'super', 'lalt', 'space',
             'ralt', 'fn', 'menu', 'rctrl']
        ],
        'spans': {key: 2 for key in ('enter', 'lshift', 'rshift', 'back')}
    }
}

##################################
# User Interface
##################################
import tkinter as tk
from tkinter import ttk


class User_Interface(tk.Frame):
    def __init__(self, master:tk.Tk=None):
        super().__init__(master)
        self.master = master
        self.master.title('League of Legends keyboard parameters UI')
        self.master.iconbitmap(f'{os.path.sep.join(__file__.split(os.path.sep)[:-1])}{os.path.sep}league_of_help_icon.ico')
        self.master.geometry('1010x275')
        self.master.maxsize(width=1010, height=275)
        self.master.minsize(width=1010, height=275)
        self.master['bg'] = '#13181B'
        
        self.pack()
        self.create_widgets()
        self.display_keyboard()
    
    def create_widgets(self):
        # Create the main menu
        menu_bar = tk.Menu(self.master)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Save')
        file_menu.add_command(label='Save as...')
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=root.quit)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label='Undo')
        edit_menu.add_command(label='Redo')
        edit_menu.add_separator()
        edit_menu.add_command(label='Reset')

        option_menu = tk.Menu(menu_bar, tearoff=0)
        
        keyboards_menu = tk.Menu(option_menu, tearoff=0)
        keyboards_menu.add_command(label='azerty', command=lambda: self.display_keyboard('azerty'))
        keyboards_menu.add_command(label='qwerty', command=lambda: self.display_keyboard('qwerty'))

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='Documentation')
        help_menu.add_command(label='Release Notes')
        help_menu.add_separator()
        help_menu.add_command(label='About')

        option_menu.add_cascade(label='Keyboard', menu=keyboards_menu)
        menu_bar.add_cascade(label='File', menu=file_menu)
        menu_bar.add_cascade(label='Edit', menu=edit_menu)
        menu_bar.add_cascade(label='Option', menu=option_menu)
        menu_bar.add_cascade(label='Help', menu=help_menu)
        self.master['menu'] = menu_bar

    def display_keyboard(self, keyboard_configuration:str=None):
        # Remove every widget
        for widget in self.winfo_children():
            widget.destroy()

        keyboard = keyboard_configuration if keyboard_configuration in keyboard_lines else 'qwerty'
        buttons_lines = [
            [tk.Button(self, text=letter, width=6, relief='groove', bg='#ddd') for letter in line]
            for line in keyboard_lines[keyboard]['keys']
        ]

        for i in range(len(buttons_lines)):
            bonus_index = 0
            for index, character_button in enumerate(buttons_lines[i]):
                for jndex, key in enumerate(persisted_settings['files'][1]['sections'][0]['settings']):
                    if any(e == key['value'] for e in (
                        f"[{character_button['text'].lower()}]",
                        f"[{character_button['text'][0].upper()}{character_button['text'][1:].lower()}]",
                        f"[{character_button['text']}]")
                    ):
                        if jndex in (5, 69):
                            character_button['bg'] = 'blue'
                        elif 6 <= jndex <= 7:
                            character_button['bg'] = 'orange'
                        elif 8 <= jndex <= 11:
                            character_button['bg'] = 'red'
                        elif jndex == 40:
                            character_button['bg'] = 'yellow'
                        elif 65 <= jndex <= 68:
                            character_button['bg'] = 'brown'
                        elif 142 <= jndex <= 147:
                            character_button['bg'] = 'pink'
                        elif jndex == 148:
                            character_button['bg'] = 'aqua'
                        elif jndex == 149:
                            character_button['bg'] = 'gold'
                        else:
                            character_button['bg'] = 'green'
                        break
                
                # Grid button
                if character_button['text'] in keyboard_lines[keyboard]['spans']:
                    character_button.grid(
                        row=i, column=index + bonus_index,
                        ipadx=int(19 * keyboard_lines[keyboard]['spans'][character_button['text']]),
                        ipady=10,
                        columnspan=keyboard_lines[keyboard]['spans'][character_button['text']]
                    )
                    bonus_index += keyboard_lines[keyboard]['spans'][character_button['text']] - 1
                elif character_button['text'] == 'space':
                    character_button.grid(row=i, column=index + bonus_index, ipadx=200, ipady=10, columnspan=7)
                    bonus_index += 6
                else:
                    character_button.grid(row=i, column=index + bonus_index, ipadx=6, ipady=10)
                    


root = tk.Tk()
ui = User_Interface(master=root)
ui.mainloop()
