from tkinter import Tk

from window.tk_editor import TkEditorFrame

if __name__ == '__main__':
    window = Tk('PyCreator')
    window.title('PyCreator - edytor scenariuszy')
    window.minsize(800, 600)
    main_frame = TkEditorFrame(window)
    window.mainloop()
    pass
