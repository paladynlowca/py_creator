from tkinter import Frame


class TkGameTopMenu(Frame):
    def __init__(self, _master_: Frame):
        super().__init__(master=_master_, relwidth=1, height=100, bg='red')
        self.place(in_=self.master)
        pass
    pass
