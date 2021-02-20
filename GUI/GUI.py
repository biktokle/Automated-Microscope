from tkinter import *
from tkinter.ttk import *
from controller import Controller
from tkinter import filedialog





BUTTON_WIDTH = 20
COMBO_BOX_WIDTH = 20
BROWSE_WIDTH = 10
PATH_WIDTH = 25
PATH_HEIGHT = 20
SPACEX = 20
SPACEY = 30

TITLE_FONT_SIZE = 30
FONT_SIZE = 15

WINDOW_DIMENSIONS = '800x600+300+100'
TITLE = 'Automated Microscope'
PLACEHOLDER = 'Set Directory'





class GUI:
    def __init__(self):

        self.controller = Controller()

        self.menu, self.root = self.create_menu()
        self.execute_button = self.create_execute(self.menu)
        self.set_directory_button, self.directory_path_label = self.create_set_directory(self.menu)
        self.choose_problem_domain, self.choose_microsope, self.choose_event_detector = self.create_combo_boxes(self.menu)
        self.create_action_button = self.create_action_configuration(self.menu)

        self.menu.pack(side=LEFT)

    def create_menu(self):
        root = Tk()
        root.title(TITLE)
        root.geometry(WINDOW_DIMENSIONS)
        label = Label(root, text=TITLE, font=('Times', TITLE_FONT_SIZE))

        style = Style()
        style.configure('TButton', font=('Times', FONT_SIZE),
                        borderwidth='1')
        style.map('TButton', foreground=[('active', 'black')],
                  background=[('active', 'white')])

        label.pack()
        menu = Label(root)
        return menu, root




    def set_event_detector(self, event):
        choice = event.widget.current()
        self.controller.set_detector(choice)

    def create_execute(self, menu):
        execute_button = Button(menu, text="Execute", command=self.controller.run)
        execute_button.config(width=BUTTON_WIDTH)
        execute_button.pack(padx=SPACEX, pady=SPACEY)
        return execute_button

    def browse_files(self):
        path = filedialog.askdirectory(initialdir="/", title="Select a directory")
        self.directory_path_label.delete(0, 'end')
        self.directory_path_label.insert(0, path)
        self.controller.set_image_path(path)


    def create_set_directory(self, menu):
        set_directory = Label(menu)
        path = Entry(set_directory, font=('Times', FONT_SIZE), foreground='Grey')
        path.insert(0, PLACEHOLDER)
        path.bind("<FocusIn>", lambda args: self.focus_in_entry_box(path))
        path.bind("<FocusOut>", lambda args: self.focus_out_entry_box(path, PLACEHOLDER))
        path.place(width=PATH_WIDTH, height=PATH_HEIGHT)
        path.pack(side=LEFT)

        browse = Button(set_directory, text="Browse", command=self.browse_files)
        browse.config(width=BROWSE_WIDTH)
        browse.pack()
        set_directory.pack(padx=SPACEX, pady=SPACEY)
        return browse, path


    def create_combo_boxes(self, menu):
        choose_problem_domain = Combobox(menu, state="readonly", width=COMBO_BOX_WIDTH, font=('Times', FONT_SIZE))
        choose_problem_domain.option_add('*TCombobox*Listbox.font', ('Times', FONT_SIZE))
        choose_problem_domain.set("Choose Problem Domain")
        choose_problem_domain.pack(padx=SPACEX, pady=SPACEY)

        choose_microscope = Combobox(menu, state="readonly", width=COMBO_BOX_WIDTH, font=('Times', FONT_SIZE))
        choose_microscope.option_add('*TCombobox*Listbox.font', ('Times', FONT_SIZE))
        choose_microscope.set("Choose Microscope")
        choose_microscope.pack(padx=SPACEX, pady=SPACEY)
        choose_microscope['values'] = ["AVI"]

        choose_event_detector = Combobox(menu, state="readonly", width=COMBO_BOX_WIDTH, font=('Times', FONT_SIZE))
        choose_event_detector.option_add('*TCombobox*Listbox.font', ('Times', FONT_SIZE))
        choose_event_detector.set("Choose Event Detector")
        choose_event_detector.pack(padx=SPACEX, pady=SPACEY)
        choose_event_detector.bind("<<ComboboxSelected>>", self.set_event_detector)
        choose_event_detector['values'] = [x.name for x in self.controller.get_detectors()]

        return choose_problem_domain, choose_microscope, choose_event_detector



    def create_action_configuration(self, menu):
        action_configuration = Button(menu, text="Action Configuration")
        action_configuration.config(width=BUTTON_WIDTH)
        action_configuration.pack(padx=SPACEX, pady=SPACEY)
        return action_configuration


    def focus_out_entry_box(self, widget, widget_text):
        if widget['foreground'] != 'Grey' and len(widget.get()) == 0:
            widget.delete(0, 'end')
            widget['foreground'] = 'Grey'
            widget.insert(0, widget_text)


    def focus_in_entry_box(self, widget):
        if widget['foreground'] != 'Black':
            widget['foreground'] = 'Black'
            widget.delete(0, 'end')



    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    GUI().run()
