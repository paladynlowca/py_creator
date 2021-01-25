from tkinter import Frame


class TkGameMainMenu(Frame):
    def __init__(self, _master_):
        super().__init__(master=_master_, bg='red')
        self.build()
        super().place(in_=self.master, relheight=1, relwidth=1)
        pass

    def build(self):
        pass
    pass
