from threading import Thread
from tkinter import *
from tkinter.ttk import *
import time

HEIGHT = 100
WIDTH = 400


class ProgressBarScreen:
    def __init__(self, parent):
        self.menu, self.root = \
            self.create_window(f'{WIDTH}x{HEIGHT}+{(parent.winfo_width()-WIDTH)//2}+{(parent.winfo_height()-HEIGHT)//2}')
        self.progress_bar = self.create_progress_bar()
        self.t = Thread(target=self.run_thread)
        self.loading = True

    def create_window(self, dimensions):
        root = Toplevel()
        root.grab_set()
        root.overrideredirect(1)
        root.geometry(dimensions)
        menu = Label(root)
        return menu, root

    def create_progress_bar(self):
        frame = Frame(self.root)
        label = Label(frame, text='Loading detector. Do not start microscope.')
        progress_bar = Progressbar(frame, orient=HORIZONTAL, length=100, mode='indeterminate')
        frame.place(relwidth=1, relheight=1)
        label.place(rely=0, relwidth=1, relheight=0.5)
        progress_bar.place(rely=0.5, relwidth=1, relheight=0.5)
        return progress_bar

    def run_thread(self):
        counter = 0
        while self.loading:
            self.progress_bar['value'] = (counter % (10 + 1)) * 10
            self.root.update_idletasks()
            counter += 1
            time.sleep(0.5)

    def run(self):
        self.t.start()
        self.root.mainloop()

    def destroy(self):
        self.loading = False
        self.t.join()
        self.root.destroy()
