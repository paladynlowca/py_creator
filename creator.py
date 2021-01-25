from tkinter import Tk

from window.tk_editor import TkEditor

if __name__ == '__main__':
    window = Tk('PyCreator')
    window.title('PyCreator - edytor scenariuszy')
    window.minsize(1000, 700)
    window.resizable(False, False)
    main_frame = TkEditor(window)
    window.mainloop()
    pass
