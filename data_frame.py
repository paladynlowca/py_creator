from pathlib import Path
from typing import Dict, Optional

from element import Code


class SceneFrame:
    def __init__(self, _title_: Optional[str] = None, _describe_: Optional[str] = None, _img_: Optional[Path] = None):
        self.title: Optional[str] = _title_
        self.describe: Optional[str] = _describe_
        self.img: Optional[Path] = _img_
        self.options: Dict[Code, str] = dict()
        pass

    def add_option(self, _code_: Code, _text_: str) -> bool:
        if _code_ not in self.options:
            self.options[_code_] = _text_
            return True
        return False
    pass
