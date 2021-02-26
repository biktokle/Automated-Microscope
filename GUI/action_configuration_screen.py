from tkinter import *
from tkinter.ttk import *

BUTTON_WIDTH = 10
SPACEX = 20
SPACEY = 20
TEXT_FONT_SIZE = 10
FONT_SIZE = 15
ACTION_CONFIGURATION_DIMENSIONS = '700x500+350+150'
ACTION_CONFIGURATION_TITLE = 'Action Configuration Setup'
TITLE_FONT_SIZE = 30
TEXT_HEIGHT = 10
TEXT_WIDTH = 10


class ActionConfigurationScreen:

    def __init__(self, controller):
        self.menu, self.root = self.create_window(ACTION_CONFIGURATION_TITLE, ACTION_CONFIGURATION_DIMENSIONS)
        self.controller = controller
        self.microscope = self.controller.microscopes[self.controller.microscope]

        self.apply_button = self.create_buttons()
        self.actions_menu = self.build_actions_menu()
        self.configuration_text = self.create_configuration_text()
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
        apply_button = Button(self.menu, text="Apply", command=self.apply_configuration)
        apply_button.config(width=BUTTON_WIDTH)
        apply_button.pack(padx=SPACEX, pady=SPACEY)
        return apply_button

    def build_lambda(self, action):
        return lambda: self.add_action(action)

    def build_actions_menu(self):
        actions_menu = Label(self.root)
        for action in self.microscope.actions_mappings:
            action_button = Button(actions_menu, text=action, command=self.build_lambda(action))
            action_button.config(width=BUTTON_WIDTH)
            action_button.place(x=100)
            action_button.pack()

        actions_menu.place(relx=0.25, rely=0.5, anchor='center')
        return actions_menu

    def create_configuration_text(self):
        configuration_text = Text(self.root, height=TEXT_HEIGHT, width=TEXT_WIDTH, font=('Times', TEXT_FONT_SIZE))
        configuration_text.place(relx=0.75, rely=0.5, anchor='center')
        return configuration_text

    def add_action(self, action):
        self.configuration_text.insert('end', action + '\n')

    def apply_configuration(self):
        self.controller.apply_configuration(self.configuration_text.get('0.0', 'end'))

    def run(self):
        self.root.mainloop()

