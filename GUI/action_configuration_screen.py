from tkinter import *
from tkinter.ttk import *
from controller import Controller

BUTTON_WIDTH = 10
SPACEX = 20
SPACEY = 30
FONT_SIZE = 15
ACTION_CONFIGURATION_DIMENSIONS = '700x500+350+150'
ACTION_CONFIGURATION_TITLE = 'Action Configuration Setup'
TITLE_FONT_SIZE = 30


class ActionConfigurationScreen:

    def __init__(self, controller):
        self.menu, self.root = self.create_window(ACTION_CONFIGURATION_TITLE, ACTION_CONFIGURATION_DIMENSIONS)
        self.controller = controller

        self.root.focus_set()
        self.apply_button, self.save_button = self.create_buttons()

        self.menu.pack()

    def create_window(self, title, dimensions):
        root = Tk()
        root.title(title)
        root.geometry(dimensions)
        label = Label(root, text=title, font=('Times', TITLE_FONT_SIZE))

        style = Style(root)
        style.configure('TButton', font=('Times', FONT_SIZE),
                        borderwidth='1')
        style.map('TButton', foreground=[('active', 'black')],
                  background=[('active', 'white')])

        label.pack()
        menu = Label(root)
        return menu, root

    def create_buttons(self):
        apply_button = Button(self.menu, text="Apply")
        apply_button.config(width=BUTTON_WIDTH)
        apply_button.pack(padx=SPACEX, pady=SPACEY)

        save_button = Button(self.menu, text="Save")
        save_button.config(width=BUTTON_WIDTH)
        save_button.pack(padx=SPACEX, pady=SPACEY)
        return apply_button, save_button

    def create_save(self):
        pass

    def run(self):
        self.root.mainloop()

