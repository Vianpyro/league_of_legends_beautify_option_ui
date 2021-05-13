from tkinter import ttk
import json
import tkinter as tk
import os
import re

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
try:
    persisted_settings:dict = read_file(
        find_file(
            known_path=f'Riot Games{os.path.sep}League of Legends{os.path.sep}Config',
            name='PersistedSettings.json'
        )
    )
except:
    raise ValueError('Unable to locate the League of Legends Config folder.')
else:
    print('Successfuly loaded the League of Legends Config folder.')

# Keyboard layouts
keyboard_layout = {
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
    },
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
    }
}

# Color code
color_code = {
    'attack_move': 'gray',
    'back': 'aqua',
    'camera_select_ally': 'skyblue1',
    'camera_snap_self': 'lightsteelblue',
    'champion_spell': 'tomato',
    'default_color': 'lightgreen',
    'enemy_vision': 'chocolate3',
    'open_shop': 'orange',
    'show_character_menu': 'chartreuse2',
    'summoner_spell': 'yellow',
    'show_scoreboard': 'darkorchid1',
    'use_item': 'pink',
    'ward': 'gold'
}

##################################
# User Interface
##################################
class User_Interface(tk.Frame):
    def __init__(self, master:tk.Tk=None):
        super().__init__(master)
        self.size = (1010, 275 + ((len(color_code) + (len(color_code) % 2)) * 23))
        self.master = master
        self.master.title('League of Legends keyboard parameters UI')
        # self.master.iconbitmap(f'{os.path.sep.join(__file__.split(os.path.sep)[:-1])}{os.path.sep}league_of_help_icon.ico')
        self.master.overrideredirect(False)
        self.master.geometry(f'{self.size[0]}x{self.size[1]}')
        self.master.maxsize(width=self.size[0], height=self.size[1])
        self.master.minsize(width=self.size[0], height=self.size[1])
        self.master['bg'] = '#13181B'

        self.keyboard = 'qwerty'

        self.pack()
        self.load()

    def move_window(self, event):
        self.master.geometry(f'+{event.x_root}+{event.y_root}')

    def load(self, keyboard:str=None):
        self.create_menu_bar()
        self.display_keyboard(keyboard)
        self.display_colors()

    def display_colors(self) -> None:
        for index, color in enumerate(color_code):
            tk.Button(
                self, width=6, bg=color_code[color]
            ).grid(
                row=(len(keyboard_layout[self.keyboard]['keys']) + (index // 2) + 1),
                column=(index % 2) * (len(keyboard_layout[self.keyboard]['keys'][0]) // 2),
                ipadx=6, ipady=10
            )
            tk.Label(
                self, text=color.replace('_', ' '),
                width=6, anchor='w'
            ).grid(
                row=(len(keyboard_layout[self.keyboard]['keys']) + (index // 2) + 1),
                column=((index % 2) * (len(keyboard_layout[self.keyboard]['keys'][0]) // 2) + 1),
                ipadx=(19 * 2), ipady=10, columnspan=2
            )

    def create_menu_bar(self) -> None:
        # Create the title bar
        # title_bar = tk.Frame(self.master, bg='pink', relief='raised', bd=2)
        # close_button = tk.Button(title_bar, text='X', command=self.master.destroy)
        # title_bar.bind('<B1-Motion>', self.move_window)

        # Create the main menu
        menu_bar = tk.Menu(self.master)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Save')
        file_menu.add_command(label='Save as...')
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=root.quit)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        
        assign_key_menu = tk.Menu(edit_menu, tearoff=0)
        assign_option_menus = [
            {
                'menu': tk.Menu(assign_key_menu, tearoff=0),
                'label': persisted_settings['files'][i][j][k]['name'],
                'cascade': [
                    persisted_settings['files'][i][j][k]['settings'][l]['name'][4:]
                    if persisted_settings['files'][i][j][k]['settings'][l]['name'][3] == 't'
                    else persisted_settings['files'][i][j][k]['settings'][l]['name'][3:]
                    for l in range(len(persisted_settings['files'][i][j][k]['settings']))
                ]
            } if 'Events' in persisted_settings['files'][i][j][k]['name'] else None
            for i in range(len(persisted_settings['files']))
            for j in persisted_settings['files'][i]
            for k in range(len([d for d in persisted_settings['files'][i][j] if isinstance(d, dict)]))
        ]
        for o in [p for p in assign_option_menus if p is not None]:
            assign_key_menu.add_cascade(label=o['label'], menu=o['menu'])
            for p in o['cascade']:
                o['menu'].add_command(label=p)
        
        edit_menu.add_cascade(label='Assign Key', menu=assign_key_menu)
        edit_menu.add_separator()
        edit_menu.add_command(label='Reset')

        option_menu = tk.Menu(menu_bar, tearoff=0)

        keyboards_menu = tk.Menu(option_menu, tearoff=0)
        for keyboard in keyboard_layout.keys():
            keyboards_menu.add_command(label=keyboard, command=lambda real_keyboard=keyboard: self.load(keyboard=real_keyboard))

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='Documentation')
        help_menu.add_command(label='Release Notes')
        help_menu.add_separator()
        help_menu.add_command(label='About')

        # title_bar.pack(expand=1, fill='x')
        # close_button.pack(side='right')
        option_menu.add_cascade(label='Keyboard', menu=keyboards_menu)
        menu_bar.add_cascade(label='File', menu=file_menu)
        menu_bar.add_cascade(label='Edit', menu=edit_menu)
        menu_bar.add_cascade(label='Option', menu=option_menu)
        menu_bar.add_cascade(label='Help', menu=help_menu)
        self.master['menu'] = menu_bar

    def display_keyboard(self, keyboard_configuration:str=None) -> None:
        if keyboard_configuration == None or keyboard_configuration != self.keyboard:
            # Remove every widget
            for widget in self.winfo_children()[:len(color_code)]:
                widget.destroy()

            self.keyboard = keyboard_configuration if keyboard_configuration in keyboard_layout else 'qwerty'
            
            buttons_lines = [
                [tk.Button(self, text=letter, width=6, relief='groove', bg='#ddd') for letter in line]
                for line in keyboard_layout[self.keyboard]['keys']
            ]

            for i in range(len(buttons_lines)):
                bonus_index = 0
                for index, character_button in enumerate(buttons_lines[i]):
                    for section in persisted_settings['files'][1]['sections']:
                        for jndex, key in enumerate(section['settings']):
                            if any(e in key['value'].split(',') for e in (
                                f"[{character_button['text'].lower()}]",
                                f"[{character_button['text'][0].upper()}{character_button['text'][1:].lower()}]",
                                f"[{character_button['text']}]")
                            ):
                                setting_name = section['settings'][jndex]['name']

                                if setting_name in ('evtCameraSnap', 'evtSelectSelf'):
                                    character_button['bg'] = color_code['camera_snap_self']
                                elif 'evtCastAvatarSpell' in setting_name:
                                    character_button['bg'] = color_code['summoner_spell']
                                elif 'evtCastSpell' in setting_name:
                                    character_button['bg'] = color_code['champion_spell']
                                elif setting_name == 'evtOpenShop':
                                    character_button['bg'] = color_code['open_shop']
                                elif 'evtPlayerAttackMove' in setting_name:
                                    character_button['bg'] = color_code['attack_move']
                                elif setting_name == 'evtPlayerPingAreaIsWarded':
                                    character_button['bg'] = color_code['enemy_vision']
                                elif 'evtSelectAlly' in setting_name:
                                    character_button['bg'] = color_code['camera_select_ally']
                                elif setting_name == 'evtShowCharacterMenu':
                                    character_button['bg'] = color_code['show_character_menu']
                                elif any(f'evtUseItem{i}' == setting_name for i in range(7)):
                                    character_button['bg'] = color_code['use_item']
                                elif setting_name == 'evtUseItem7':
                                    character_button['bg'] = color_code['back']
                                elif setting_name == 'evtUseVisionItem':
                                    character_button['bg'] = color_code['ward']
                                elif 'Tab' in section['settings'][jndex]['value'] or setting_name == 'evtShowScoreBoard':
                                    character_button['bg'] = color_code['show_scoreboard']
                                else:
                                    character_button['bg'] = color_code['default_color']
                                break

                    # Grid button
                    if character_button['text'] in keyboard_layout[self.keyboard]['spans']:
                        character_button.grid(
                            row=i, column=index + bonus_index,
                            ipadx=int(19 * keyboard_layout[self.keyboard]['spans'][character_button['text']]),
                            ipady=10,
                            columnspan=keyboard_layout[self.keyboard]['spans'][character_button['text']]
                        )
                        bonus_index += keyboard_layout[self.keyboard]['spans'][character_button['text']] - 1
                    elif character_button['text'] == 'space':
                        character_button.grid(row=i, column=index + bonus_index, ipadx=200, ipady=10, columnspan=7)
                        bonus_index += 6
                    else:
                        character_button.grid(row=i, column=index + bonus_index, ipadx=6, ipady=10)


root = tk.Tk()
ui = User_Interface(master=root)
ui.mainloop()
