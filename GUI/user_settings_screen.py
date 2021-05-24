from tkinter import *
from tkinter.ttk import *

FONT_SIZE = 15
USER_SETTINGS_DIMENSIONS = '700x500+350+150'
USER_SETTINGS_TITLE = 'User Settings Setup'
TITLE_FONT_SIZE = 30
TEXT_HEIGHT = 10
TEXT_WIDTH = 10


class UserSettingsScreen:

    def __init__(self, controller, on_close):
        self.entries = []
        self.on_close = on_close
        self.menu, self.root = self.create_window(USER_SETTINGS_TITLE, USER_SETTINGS_DIMENSIONS)
        self.controller = controller
        self.microscope = self.controller.microscopes[(self.controller.problem_domain, self.controller.microscope)]

        self.apply_button = self.create_buttons()
        self.actions_menu = self.build_settings_menu()

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
        apply_button = Button(self.root, text="Apply", command=self.apply_settings)
        apply_button.place(relx=0.4, rely=0.25, relwidth=0.2, relheight=0.1, anchor='nw')
        return apply_button

    def build_settings_menu(self):
        settings_menu = Label(self.root)
        r = 0
        for setting in self.microscope.settings_keys:
            setting_text = Label(settings_menu, text=setting + ": ")
            setting_text.grid(row=r, column=0, sticky=W, pady=2)

            setting_entry = Entry(settings_menu)
            setting_entry.grid(row=r, column=1, pady=2)

            self.entries = self.entries + [setting_entry]
            r = r + 1

        settings_menu.place(relx=0.5, rely=0.6, anchor='center')
        return settings_menu

    def apply_settings(self):
        values = []
        for entry in self.entries:
            values = values + [entry.get()]
        self.controller.apply_settings(values)
        self.on_close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

