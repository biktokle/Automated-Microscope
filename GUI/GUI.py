import tkinter as tk


def main():
    window = tk.Tk()
    label = tk.Label(
        text="Hello, Tkinter",
        foreground="white",  # Set the
        # text color to white
        background="black"  # Set the background color to black
    )
    label.pack()
    window.mainloop()


if __name__ == '__main__':
    main()
