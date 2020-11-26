class TypeCollision(Exception):
    def __init__(self, _code_: str, _expected_: str, _got_: str):
        self._code = _code_
        self._expected = _expected_
        self._got = _got_
        pass

    def __str__(self):
        return f'Wrong type for element [{self._code}]. Expected [{self._expected}], got [{self._got}].'
    pass
