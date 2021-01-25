from tkinter import Frame, Widget, Label, LEFT, N, CENTER, W
from tkinter.font import Font

from data_frame import SceneFrame
from engine.engine_element import Code
from window.tk_settings import functions


class TkGameScene(Frame):
    class _Option(Frame):
        def __init__(self, _master_: Frame, _text_: str, _option_: Code, _position_: int):
            super().__init__(master=_master_, width=900, height=45, relief="sunken", bd=2, bg='lightgray',
                             cursor="hand2")
            self.place(anchor=N, relx=0.5, y=_position_ * 50 + 5)
            self._text = _text_
            self._code = _option_
            self._position = _position_
            self.bind("<Button-1>", self._change_scene())
            self._build()
            pass

        def _build(self):
            self._label = Label(master=self, wraplength=895, text=self._text, bg='lightgray')
            self._label.place(anchor=W, rely=0.5)
            pass

        def _change_scene(self):
            def new_function(_event_, ):
                functions['change_scene'](self._code)
                pass
            return new_function
        pass

    def __init__(self, _master_: Frame, _scene_: SceneFrame):
        super().__init__(master=_master_, bg='darkgray')
        self._code = _scene_.code
        self._title = _scene_.title
        self._description = _scene_.describe
        self._options_list = _scene_.options
        self._build()
        pass

    def place(self):
        super().place(relwidth=1, relheight=1)

    def _build(self):
        self._title_frame = Frame(master=self, relief="raised", bd=2, bg='gray')
        self._title_frame.place(relwidth=1, height=100)
        self._title_label = Label(master=self._title_frame, text=self._title, wraplength=955, justify=CENTER, bg='gray',
                                  font=Font(family="Helvetica", size=18))
        self._title_label.place(anchor=N, width=950, height=94, y=1, relx=0.5)

        self._describe_frame = Frame(master=self, relief="raised", bd=2, bg='gray')
        self._describe_frame.place(relwidth=1, height=100, y=100)
        self._describe_label = Label(master=self._describe_frame, text=self._description, wraplength=955,
                                     justify=LEFT, bg='gray')
        self._describe_label.place(anchor=N, width=950, height=94, y=1, relx=0.5)

        self._options_frame = Frame(master=self, relief="raised", bd=2, bg='gray')
        self._options_frame.place(relwidth=1, height=500, y=200)
        self._options_frames = list()
        position = 0
        for option in self._options_list:
            self._options_frames.append(self._Option(self._options_frame, self._options_list[option], option, position))
            position += 1
            pass
        pass
    pass


class TkGameScene_(Frame):
    class _Option(Label):
        def __init__(self, _master_: Frame, _text_: str, _option_: Code, position: int):
            super().__init__(_master_, text=_text_, font=Font(family="Helvetica", size=12), justify=LEFT,
                             borderwidth=2, relief="raised", cursor="hand2")
            self.code = _option_

            self.bind("<Enter>", self._on_entry)
            self.bind("<Leave>", self._on_leave)
            self.bind("<Button-1>", self._change_scene())
            self.place(in_=_master_, x=5, y=5 + position * 35, height=30)
            pass

        def _on_entry(self, _event_):
            self.config(relief="sunken")
            pass

        def _on_leave(self, _event_):
            self.config(relief="raised")
            pass

        def _change_scene(self):
            def new_function(_event_, ):
                functions['change_scene'](self.code)
                pass
            return new_function

        pass

    def __init__(self, _master_: Widget, _scene_: SceneFrame):
        _master_.update()
        super().__init__(_master_, borderwidth=2, relief="groove")
        self._master = _master_
        self._scene = _scene_
        self._build()
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
                self._Option(self._options_frame, text, code, position))
            position += 1
        pass

    pass
