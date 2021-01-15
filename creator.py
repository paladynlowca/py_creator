from tkinter import Tk

from window.tk_editor import TkEditorFrame

if __name__ == '__main__':
    window = Tk('PyCreator')
    window.title('PyCreator - edytor scenariuszy')
    window.minsize(1000, 700)
    window.resizable(False, False)
    main_frame = TkEditorFrame(window)
    window.mainloop()
    pass
