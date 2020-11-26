class TypeCollision(Exception):
    """"
    Raise for wrong type match.
    """

    def __init__(self, _code_: str, _expected_: str, _got_: str):
        """

        :param _code_: Element str code.
        :type _code_: str
        :param _expected_: Expected element type.
        :type _expected_: str
        :param _got_: Got element type.
        :type _got_: str
        """
        self._code = _code_
        self._expected = _expected_
        self._got = _got_
        pass

    def __str__(self):
        return f'Wrong type for element >{self._code}<. Expected >{self._expected}<, got >{self._got}<.'

    pass


class ExistingRelations(Exception):
    """
    Raise while deleting element with existing relations.
    """

    def __init__(self, _code_: str, _relations_: set):
        """

        :param _code_: Element str code
        :type _code_: str
        :param _relations_: Set of relations
        :type _relations_: set
        """
        self._code = _code_
        self._relations = _relations_
        pass

    def __str__(self):
        return f'Deleting element >{self._code}< relations with existing relations >{self._relations}<.'

    pass
