from threading import Thread
from tkinter import *
from tkinter.ttk import *
import time

class ProgressBarScreen:

    def __init__(self):
        self.menu, self.root = self.create_window('300x50')
        self.progress_bar = self.create_progress_bar()

    def create_window(self, dimensions):
        root = Toplevel()
        root.grab_set()
        root.title('Loading...')
        root.geometry(dimensions)
        menu = Label(root)
        return menu, root

    def create_progress_bar(self):
        progress_bar = Progressbar(self.root, orient=HORIZONTAL, length=100, mode='indeterminate')
        progress_bar.place(relwidth=1, relheight=1, anchor='nw')
        return progress_bar

    def run_thread(self):
        counter = 0
        while 1:
            self.progress_bar['value'] = (counter % (10 + 1)) * 10
            self.root.update_idletasks()
            counter += 1
            time.sleep(0.5)

    def run(self):
        Thread(target=self.run_thread).start()
        self.root.mainloop()
