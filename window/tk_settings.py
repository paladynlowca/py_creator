from typing import Dict

from exceptions import *

lang: Dict[str, str] = dict()
settings: Dict[str, str] = dict()

functions: Dict[str, callable] = dict()


def parse_file(_file_name_: str, _separator_: str = ' = ', _comment_: str = '#', _ignore_errors_: bool = True):
    try:
        lines = dict()
        with open(_file_name_, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.replace('\n', '').split(_comment_, 1)[0]
                if _separator_ in line:
                    key, value = line.split(_separator_, maxsplit=1)
                    lines[key] = value
                    pass
                elif not _ignore_errors_ and not line.isspace():
                    raise ConfigParseError
                    pass
                pass
            pass
        return lines
    except FileNotFoundError:
        pass
    pass


def register_function(name: str, _function_: callable):
    functions[name] = _function_
    pass


def load_texts(_lang_: str):
    lang.update(parse_file(f'lang/{_lang_}.txt'))
    pass


def init():
    settings.update(parse_file('config.ini'))
    load_texts(settings['lang'])
    pass
