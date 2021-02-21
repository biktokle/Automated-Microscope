from tkinter import *
from tkinter.ttk import *
from controller import Controller


class ActionConfigurationScreen:

    def __init__(self, menu, root, controller):
        self.menu = menu
        self.root = root
        self.controller = controller

    def run(self):
        self.root.mainloop()

