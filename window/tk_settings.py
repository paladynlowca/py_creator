from typing import Dict

lang: Dict[str, str] = dict()

functions: Dict[str, callable] = dict()


def load_texts(_lang_: str):
    try:
        with open(f'lang/{_lang_}.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.replace('\n', '')
                if len(line) > 0 and not line[0] == '#':
                    key, value = line.split(' = ', maxsplit=1)
                    line.replace('\n', '')
                    lang[key] = value
                    pass
                pass
            pass
        pass
    except FileNotFoundError:
        pass
    pass


def register_function(name: str, _function_: callable):
    functions[name] = _function_
    pass
