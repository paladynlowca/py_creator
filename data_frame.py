from pathlib import Path
from typing import Dict, Optional

from element import Code


class SceneFrame:
    """
    Class contains all data use for display scene.
    """

    def __init__(self, _title_: Optional[str] = None, _describe_: Optional[str] = None, _img_: Optional[Path] = None):
        """
        :param _title_: Scene title.
        :type _title_: str
        :param _describe_: Scene describe.
        :type _describe_: str
        :param _img_: Scene image path.
        :type _img_: Path
        """
        self.title: Optional[str] = _title_
        self.describe: Optional[str] = _describe_
        self.img: Optional[Path] = _img_
        self.options: Dict[Code, str] = dict()
        pass

    def add_option(self, _code_: Code, _text_: str) -> bool:
        """
        Adding option to scene.
        :param _code_: Option code.
        :type _code_: Code
        :param _text_: Option text.
        :type _text_: str
        :return: Success of operation.
        :rtype: bool
        """
        if _code_ not in self.options:
            self.options[_code_] = _text_
            return True
        return False
    pass
