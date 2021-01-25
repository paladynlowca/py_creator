from tkinter import Tk

from window.tk_game import TkGameFrame

if __name__ == '__main__':
    window = Tk('PyCreator')
    window.title('PyCreator')
    window.minsize(1000, 700)
    window.resizable(False, False)
    main_frame = TkGameFrame(window)
    window.mainloop()
    pass
