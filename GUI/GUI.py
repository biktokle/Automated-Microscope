from tkinter import *
from tkinter.ttk import *

BUTTON_WIDTH = 20
BROWSE_WIDTH = 10
PATH_WIDTH = 25
PATH_HEIGHT = 20


def focus_out_entry_box(widget, widget_text):
    if widget['foreground'] == 'Black' and len(widget.get()) == 0:
        widget.delete(0, 'end')
        widget['foreground'] = 'Grey'
        widget.insert(0, widget_text)


def focus_in_entry_box(widget):
    print(widget['foreground'])
    if widget['foreground'] == 'Grey':
        widget['foreground'] = 'Black'
        widget.delete(0, 'end')


def main():
    root = Tk()
    root.title('Automated Microscope')
    root.geometry('800x600+300+100')
    label = Label(
        root, text="Automated Microscope", font=('Times', 30)
    )

    # Create style Object
    style = Style()

    style.configure('TButton', font=('Times', 15),
                    borderwidth='1')
    # Changes will be reflected
    # by the movement of mouse.
    style.map('TButton', foreground=[('active', 'black')],
              background=[('active', 'white')])

    label.pack()
    menu = Label(root)
    execute = Button(menu, text="Execute")
    execute.config(width=BUTTON_WIDTH)
    execute.pack(padx=30, pady=20)

    set_directory = Label(menu)
    path = Entry(set_directory, font=('Times', 15), foreground='Grey')
    path.insert(0, 'Set Directory')
    path.bind("<FocusIn>", lambda args: focus_in_entry_box(path))
    path.bind("<FocusOut>", lambda args: focus_out_entry_box(path, 'Set Directory'))
    path.place(width=PATH_WIDTH, height=PATH_HEIGHT)
    path.pack(side=LEFT)

    browse = Button(set_directory, text="Browse")
    browse.config(width=BROWSE_WIDTH)
    browse.pack()
    set_directory.pack(padx=30, pady=20)

    choose_microscope = Button(menu, text="Choose Microscope")
    choose_microscope.config(width=BUTTON_WIDTH)
    choose_microscope.pack(padx=30, pady=20)

    choose_microscope = Button(menu, text="Choose Event Detector")
    choose_microscope.config(width=BUTTON_WIDTH)
    choose_microscope.pack(padx=30, pady=20)

    choose_problem_domain = Button(menu, text="Choose Problem Domain")
    choose_problem_domain.config(width=BUTTON_WIDTH)
    choose_problem_domain.pack(padx=30, pady=20)

    action_configuration = Button(menu, text="Action Configuration")
    action_configuration.config(width=BUTTON_WIDTH)
    action_configuration.pack(padx=30, pady=20)

    menu.pack(side=LEFT, )
    root.mainloop()


if __name__ == '__main__':
    main()
