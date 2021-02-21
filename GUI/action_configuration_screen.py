from tkinter import *
from tkinter.ttk import *
from controller import Controller

BUTTON_WIDTH = 10
SPACEX = 20
SPACEY = 30
FONT_SIZE = 15


class ActionConfigurationScreen:

    def __init__(self, menu, root, controller):
        self.menu = menu
        self.root = root
        self.controller = controller

        self.root.focus_set()
        self.apply_button, self.save_button = self.create_buttons()

        self.menu.pack()

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

