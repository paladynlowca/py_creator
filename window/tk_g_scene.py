from tkinter import Frame, Widget, Label, LEFT
from tkinter.font import Font

from data_frame import SceneFrame
from engine.engine_element import Code


class TkScenePane(Frame):
    class _TkSceneOption(Label):
        def __init__(self, _master_: Frame, _text_: str, _option_: Code, position: int, _on_click_: callable):
            super().__init__(_master_, text=_text_, font=Font(family="Helvetica", size=12), justify=LEFT,
                             borderwidth=2, relief="raised", cursor="hand2")
            self.code = _option_
            self.bind("<Enter>", self._on_entry)
            self.bind("<Leave>", self._on_leave)
            self.bind("<Button-1>", self._decorate(_on_click_))
            self.place(in_=_master_, x=5, y=5 + position * 35, height=30)
            pass

        def resize(self, _width_: int):
            self.config(wraplength=_width_ - 40)
            pass

        def _on_entry(self, _event_):
            self.config(relief="sunken")
            pass

        def _on_leave(self, _event_):
            self.config(relief="raised")
            pass

        def _decorate(self, function: callable):
            def new_function(_event_, ):
                function(self.code)
                pass

            return new_function

        pass

    def __init__(self, _master_: Widget, _scene_: SceneFrame, _scene_changer_: callable):
        _master_.update()
        super().__init__(_master_, borderwidth=2, relief="groove")
        self._master = _master_
        self._scene = _scene_
        self._scene_changer = _scene_changer_
        self._build()
        pass

    def resize(self):
        width = self._master.winfo_width()
        height = self._master.winfo_height()
        self.config(width=width, height=height - 50)
        self._title.config(wraplength=width - 8)
        self._describe_frame.config(width=width - 4)
        self._describe.config(wraplength=width - 8)
        self._options_frame.config(width=width - 4, height=height - 284)
        for option in self._options_list:
            option.resize(width)
        pass

    def place(self):
        super().place(in_=self._master, x=0, y=50)
        pass

    def _build(self):
        self._title = Label(self, text=self._scene.title, font=Font(family="Helvetica", size=18), justify=LEFT)
        self._title.place(in_=self, x=10, y=10, height=50)

        self._describe_frame = Frame(self, height=154, borderwidth=2, relief="groove")
        self._describe_frame.place(in_=self, x=0, y=70)
        self._describe = Label(self._describe_frame, text=self._scene.describe, font=Font(family="Helvetica", size=12),
                               justify=LEFT)
        self._describe.place(in_=self._describe_frame, x=5, y=0, height=150)
        self._options_list = list()
        self._options_frame = Frame(self, width=796, height=366, borderwidth=2, relief="groove")
        self._options_frame.place(in_=self, x=0, y=230)
        position = 0
        for code, text in self._scene.options.items():
            self._options_list.append(
                self._TkSceneOption(self._options_frame, text, code, position, self._scene_changer))
            position += 1
        pass

    pass
