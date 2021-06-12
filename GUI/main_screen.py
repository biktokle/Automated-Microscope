from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from PIL import Image, ImageTk
from GUI.progress_bar_screen import ProgressBarScreen
from GUI.user_settings_screen import UserSettingsScreen
from controller.controller import Controller
from tkinter import filedialog
from notification.publisher import Events
import sys
IMAGE_CANVAS_WIDTH = 1000
IMAGE_CANVAS_HEIGHT = 1000
IMAGE_BACKGROUND = "gray"

TITLE_FONT_SIZE = 40
FONT_SIZE = 15
DESCRIPTION_SIZE = 10

MAIN_WINDOW_DIMENSIONS = '1800x1000'

TITLE = 'Automated Microscope'

PLACEHOLDER = 'Set Working Directory'
PLACEHOLDER_DETECTORS = 'Set Detectors Directory'

SOFTWARE_CONFIG_PATH = './software_config.json'

class MainScreen:

    def __init__(self):
        self.images = []
        self.controller = Controller(SOFTWARE_CONFIG_PATH)
        self.menu, self.root = self.create_window(TITLE, MAIN_WINDOW_DIMENSIONS)
        self.execute_button = self.create_execute_button()
        self.stop_button = self.create_stop_button()
        self.set_directory_button, self.directory_path_label = self.create_set_directory()
        self.set_detectors_directory_button, self.detectors_directory_path_label = self.create_set_detectors_path()
        self.choose_problem_domain, self.choose_microscope, self.choose_event_detector =\
            self.create_combo_boxes()
        self.create_user_settings = self.create_user_settings(self.menu)
        self.image_canvas = self.create_image_canvas()
        self.ed_description, self.us_description = self.create_description()
        self.progress_bar = None

        # Register Events
        self.controller.publisher.subscribe(Events.popup_event)(self._on_error)
        self.controller.publisher.subscribe(Events.image_event)(self._on_new_image)
        self.controller.publisher.subscribe(Events.detector_loaded)(self.destroy_progress_bar)
        self.controller.publisher.subscribe(Events.start_progress_bar)(self.open_progress_bar)

    def exit(self):
        self.controller.stop(to_exit=True)
        sys.exit(1)

    def open_progress_bar(self):
        self.progress_bar = ProgressBarScreen(self.root)
        self.progress_bar.run()

    def destroy_progress_bar(self):
        if self.progress_bar is not None:
            self.progress_bar.destroy()
            self.progress_bar = None
            self._on_info('Detector loaded.\nWaiting for images from microscope.')


    def create_window(self, title, dimensions):
        root = Tk()
        root.state('zoomed')
        root.title(title)
        root.geometry(dimensions)
        root.protocol("WM_DELETE_WINDOW", self.exit)

        style = Style(root)
        style.configure('TButton', font=('Times', FONT_SIZE),
                        borderwidth='1')
        style.map('TButton', foreground=[('active', 'black')],
                  background=[('active', 'white')])

        title_label = Label(root, text=title, font=('Times', TITLE_FONT_SIZE))
        title_label.place(relx=0.05, rely=0.05, relwidth=0.4, anchor='nw')

        menu = Label(root)
        menu.place(relx=0.1, rely=0.15, relwidth=0.3, relheight=0.8, anchor='nw')
        return menu, root


    def create_execute_button(self):
        execute_button = Button(self.menu, text="Execute", command=self.controller.run)
        execute_button.place(relx=0.15, rely=0.05, relwidth=0.5, anchor='nw')
        return execute_button

    def create_stop_button(self):
        stop_button = Button(self.menu, text="Stop", command=self.controller.stop)
        stop_button.place(relx=0.15, rely=0.15, relwidth=0.5, anchor='nw')
        return stop_button

    def browse_files(self):
        path = filedialog.askdirectory(initialdir="/", title="Select a directory")
        self.directory_path_label.delete(0, 'end')
        self.directory_path_label.insert(0, path)
        self.directory_path_label['foreground'] = 'Black'
        self.controller.set_working_dir(path)

    def browse_files_detectors(self):
        path = filedialog.askdirectory(initialdir="/", title="Select a directory")
        self.detectors_directory_path_label.delete(0, 'end')
        self.detectors_directory_path_label.insert(0, path)
        self.detectors_directory_path_label['foreground'] = 'Black'
        self.controller.set_detectors_path(path)
        self.choose_event_detector['values'] = [x.name for x in self.controller.get_detectors()]

    def create_set_detectors_path(self):
        set_detectors_path = Label(self.menu)
        path = Entry(set_detectors_path, font=('Times', FONT_SIZE), foreground='Grey')
        path.insert(0, PLACEHOLDER_DETECTORS)
        path.bind("<FocusIn>", lambda args: self.focus_in_entry_box(path, PLACEHOLDER_DETECTORS))
        path.bind("<FocusOut>", lambda args: self.focus_out_entry_box(path, PLACEHOLDER_DETECTORS))
        path.place(relwidth=0.7, anchor='nw')

        browse = Button(set_detectors_path, text="Browse", command=self.browse_files_detectors)
        browse.place(relx=0.7, relwidth=0.3, anchor='nw')
        set_detectors_path.place(relx=0.1, rely=0.25, relwidth=0.6, relheight=0.1, anchor='nw')
        return browse, path

    def create_set_directory(self):
        set_directory = Label(self.menu)
        path = Entry(set_directory, font=('Times', FONT_SIZE), foreground='Grey')
        path.insert(0, PLACEHOLDER)
        path.bind("<FocusIn>", lambda args: self.focus_in_entry_box(path, PLACEHOLDER))
        path.bind("<FocusOut>", lambda args: self.focus_out_entry_box(path, PLACEHOLDER))
        path.place(relwidth=0.7, anchor='nw')

        browse = Button(set_directory, text="Browse", command=self.browse_files)
        browse.place(relx=0.7, relwidth=0.3, anchor='nw')
        set_directory.place(relx=0.1, rely=0.35, relwidth=0.6, relheight=0.1, anchor='nw')
        return browse, path

    def create_combo_boxes(self):
        choose_problem_domain = Combobox(self.menu, state="readonly", font=('Times', FONT_SIZE))
        choose_problem_domain.option_add('*TCombobox*Listbox.font', ('Times', FONT_SIZE))
        choose_problem_domain.set("Choose Problem Domain")
        choose_problem_domain.place(relx=0.1, rely=0.45, relwidth=0.6, relheight=0.05, anchor='nw')
        choose_problem_domain.bind("<<ComboboxSelected>>", self.set_problem_domain)
        choose_problem_domain['values'] = self.controller.problem_domains

        choose_microscope = Combobox(self.menu, state="readonly", font=('Times', FONT_SIZE))
        choose_microscope.option_add('*TCombobox*Listbox.font', ('Times', FONT_SIZE))
        choose_microscope.set("Choose Microscope")
        choose_microscope.bind("<<ComboboxSelected>>", self.set_microscope)
        choose_microscope.place(relx=0.1, rely=0.55, relwidth=0.6, relheight=0.05, anchor='nw')

        choose_event_detector = Combobox(self.menu, state="readonly", font=('Times', FONT_SIZE))
        choose_event_detector.option_add('*TCombobox*Listbox.font', ('Times', FONT_SIZE))
        choose_event_detector.set("Choose Event Detector")
        choose_event_detector.place(relx=0.1, rely=0.65, relwidth=0.6, relheight=0.05, anchor='nw')
        choose_event_detector.bind("<<ComboboxSelected>>", self.set_event_detector)

        return choose_problem_domain, choose_microscope, choose_event_detector

    def create_description(self):
        event_detector = Label(self.root, text='Event Detector Description:\n', font=('Times', DESCRIPTION_SIZE),
                               wraplength=200)
        event_detector.place(relx=0.05, rely=0.9, relwidth=0.15, relheight=0.15, anchor='w')

        user_settings = Label(self.root, text='User Settings:\n', font=('Times', DESCRIPTION_SIZE),
                              wraplength=200)
        user_settings.place(relx=0.3, rely=0.9, relwidth=0.15, relheight=0.15, anchor='w')
        return event_detector, user_settings

    def create_image_canvas(self):
        image_canvas = Canvas(self.root, bg=IMAGE_BACKGROUND)
        image_canvas.place(relx=0.5, relwidth=0.5, relheight=1, anchor='nw')
        return image_canvas

    def focus_out_entry_box(self, widget, widget_text):
        if widget['foreground'] != 'Grey' and len(widget.get()) == 0:
            widget.delete(0, 'end')
            widget['foreground'] = 'Grey'
            widget.insert(0, widget_text)

    def focus_in_entry_box(self, widget, widget_text):
        if widget['foreground'] != 'Black':
            widget['foreground'] = 'Black'
            if widget.get() == widget_text:
                widget.delete(0, 'end')

    def stringify_user_settings(self, settings):
        stringified = ''
        for setting in settings:
            stringified += '\n' + setting + ': ' + str(settings[setting])

        return stringified

    def set_user_settings(self):
        self.us_description['text'] = 'User Settings:' + self.stringify_user_settings(self.controller.get_user_settings())

    def open_user_settings(self):
        if self.choose_microscope.get() != "Choose Microscope":
            UserSettingsScreen(self.controller, self.set_user_settings).run()
        else:
            self._on_error("Please choose a microscope")

    def create_user_settings(self, menu):
        user_settings = Button(menu, text="User Settings", command=self.open_user_settings)
        user_settings.place(relx=0.15, rely=0.75, relwidth=0.5, relheight=0.05, anchor='nw')
        return user_settings

    def set_problem_domain(self, event):
        choice = event.widget.current()
        microscopes = self.controller.set_problem_domain(choice)
        self.choose_microscope['values'] = microscopes

    def set_microscope(self, event):
        choice = event.widget.current()
        self.controller.set_microscope(choice)

    def set_event_detector(self, event):
        choice = event.widget.current()
        self.controller.set_detector(choice)
        self.ed_description['text'] = 'Event Detector Description:\n' + self.controller.get_event_detector().description

    def run(self):
        self.root.mainloop()

    def _on_error(self, error_message):
        messagebox.showerror('Error', error_message)

    def _on_info(self, info_message):
        messagebox.showinfo('Info', info_message)

    def _on_new_image(self, image):
        tk_image = ImageTk.PhotoImage(Image.fromarray(image).resize((IMAGE_CANVAS_WIDTH, IMAGE_CANVAS_HEIGHT), Image.ANTIALIAS))
        self.images.append(tk_image)
        self.image_canvas.create_image(0, 0, image=tk_image, anchor="nw")


