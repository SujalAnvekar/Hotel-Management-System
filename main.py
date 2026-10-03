import tkinter as tk
from ui.login import LoginWindow


root = tk.Tk()

LoginWindow(root)

def main():

    root = tk.Tk()

    LoginWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()