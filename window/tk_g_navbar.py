from tkinter import Menu, Tk


class TkNavBar(Menu):
    def __init__(self, _master_: Tk):
        super().__init__(_master_)
        self._master = _master_

        font = ("Courier", 44)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu, tearoff=0)
        file.add_command(label="Exit", command=self._exit)
        menu.add_cascade(label="File", menu=file)
        menu.config(font=font)

        edit = Menu(menu, tearoff=0)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)
        pass

    @staticmethod
    def _exit():
        exit(1)
        pass

    pass
