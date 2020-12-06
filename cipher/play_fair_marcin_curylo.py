from typing import Callable, List


class MenuError(Exception):
    pass


# Uniwersala klasa menu przygotowana z myślą o przyszłych implementacjach
class Menu:
    class MenuOption:
        def __init__(self, text: str, key: str, action: Callable[[], None]):
            self._text = text
            self._key = key.upper()
            self._action = action
            pass

        @property
        def action(self):
            return self._action

        @property
        def key(self):
            return self._key

        def __str__(self):
            return f'{self._key} - {self._text}'

        def __eq__(self, other: str):
            if self._key == other.upper():
                return True
            return False

        pass

    def __init__(self):
        self._options: List[Menu.MenuOption] = list()
        pass

    @property
    def keys(self):
        keys = list()
        keys.append('X')
        for option in self._options:
            keys.append(option.key)
        return keys

    def add_option(self, text: str, key: str, action: Callable[[], None]):
        if key.upper() not in self.keys:
            self._options.append(self.MenuOption(text, key, action))
            return True
        return False

    def print(self):
        print()
        for option in self._options:
            print(option)
            pass
        print('X - Wyjście')
        pass

    def choose(self):
        print('Dokonaj wyboru')
        choice = input('>>')
        if choice.upper() == 'X':
            print('Do widzenia.\n<ENTER żeby zakończyć>')
            input()
            exit(0)
        for option in self._options:
            if option == choice:
                return option.action
            pass
        print('Błędny wybór.')
        return False

    def run(self):
        while True:
            self.print()
            action = self.choose()
            if action:
                try:
                    action()
                    pass
                except MenuError as exception:
                    print(f'Nastapił błąd przetwazania polecenia z wiadomością: {exception}')
                pass
            pass
        pass
    pass


chars_letters = ['A', 'B', 'C', 'D', 'E',
                 'F', 'G', 'H', 'I', 'K',
                 'L', 'M', 'N', 'O', 'P',
                 'Q', 'R', 'S', 'T', 'U',
                 'V', 'W', 'X', 'Y', 'Z']


# Pobieranie tekstu do za/rozszyfrowania od użytkownika
def get_input(reverse: bool = False):
    word = 'zaszyfrowania' if not reverse else 'odszyfrowania'
    # pobieranie tekstu do zaszyfrowania
    print(f'Wprowadź ciąg do {word}:')
    output = list()
    # Zamiana na wielkie litery oraz podmiana J na I
    raw = input('>>').upper().replace('J', 'I')
    data = ''
    # Wyrzucenie wszystkich znaków spoza alfabetu łacińskiego oraz J
    for char in raw:
        if char in chars_letters:
            data += char
            pass
        pass
    # Podział na pary znaków z zabezpieczeniem przed dodaniem do pary dwóch takich samych znaków
    pos = 2
    while True:
        # Pobranie dwóch kolejnych znaków
        pair = data[pos - 2:pos]
        # Jeżeli nie pobrano, to wyjdź
        if len(pair) == 0:
            return output
        # Jeżeli został tylko jeden, to dodaj mu znak X (jeżeli jest to znak X, to Y), dodaj do wyjścia i wyjdź
        elif len(pair) == 1:
            output.append(pair + ('Y' if pair == 'X' else 'X'))
            return output
        # Jeżeli są to te same znaki, to zamień drugi na znak X(jeżeli są to znaki X, to Y) i przesuń wskaźnik o 1
        elif pair[0] == pair[1]:
            pair = pair[0] + ('Y' if pair[0] == 'X' else 'X')
            pos += 1
            pass
        # W przeciwnym wypadku przesuń wskaźnik o 2
        else:
            pos += 2
            pass
        # Dodaj do listy par tą aktualną
        output.append(pair)
        pass


# Pobieranie hasła szyfrogramu
def get_password():
    print('Podaj hasło')
    return input('>>').upper()


# Iterator zwracający krotkę z kolejnymi współżędnymi znaku
class Numbers:
    def __init__(self):
        self._x = -1
        self._y = -1
        pass

    def __iter__(self):
        return self

    def __next__(self):
        self._y = (self._y + 1) % 5
        if self._y == 0:
            self._x += 1
            pass
        if self._x > 4:
            raise StopIteration
        return self._x, self._y

    pass


def prepare_table():
    # Tworzenie tablicy wyjściowej i iteratora z którego pobierane będą kolejne wartości szyfru
    password = get_password()
    output = dict()
    iterator = iter(Numbers())
    # Iterowanie po literach hasła
    for char in password:
        if char not in output and char in chars_letters:  # Sprawdzenie, czy znak jest literą i nie ma go w tablicy
            output[char] = next(iterator)  # Przypisanie do każdej litery kolejnej wartości szyfru
            pass
        pass
    # Dodanie do tablicy liter niewystępujących w haśle
    for char in chars_letters:
        if char not in output:  # Sprawdzenie, czy znaku nie ma w tablicy
            output[char] = next(iterator)  # Przypisanie do każdej litery kolejnej wartości szyfru
    return output
    pass


def encode(reverse: bool = False):
    # Ustaw współczynnik przesunięcia (+1 dla szyfrowania, -1 dla deszyfrowania)
    switch = -1 if reverse else 1
    # Pobranie tekstu od użytkownika i przygotowanie tablicy z szyfrem
    pairs = get_input(reverse)
    table = prepare_table()
    table_reverse = {table[key]: key for key in table}
    # Zaszyfrowanie kolejnych znaków
    output = ''
    # Dla każdej pary znaków
    for pair in pairs:
        # Znajdź współżędne znaków
        c1 = table[pair[0]]
        c2 = table[pair[1]]
        # Jeżeli sa w jednej kolumnie to przesuń zgodnie z ustalonym kierunkiem
        if c1[1] == c2[1]:
            output += table_reverse[((c1[0] + switch) % 5, c1[1])] + table_reverse[((c2[0] + switch) % 5, c2[1])]
            pass
        # Jeżeli sa w jednym wierszu to przesuń zgodnie z ustalonym kierunkiem
        elif c1[0] == c2[0]:
            output += table_reverse[(c1[0], (c1[1] + switch) % 5)] + table_reverse[(c2[0], (c2[1] + switch) % 5)]
            pass
        # W przeciwnym wypadku weź znak o współżedych (jego x, y drugiego znaku z pary)
        else:
            output += table_reverse[(c1[0], c2[1])] + table_reverse[(c2[0], c1[1])]
            pass

        pass
    # Wypisywanie wyniku
    print('Zaszyfrowana wiadomość to:')
    print(output)
    pass


def decode():
    # Wywołaj szyftowania z odwróconym przesunięciem
    encode(True)
    pass


if __name__ == '__main__':
    # Inicjowanie menu i dodawanie opcji szyfrowania oraz rozszyfrowania
    menu = Menu()
    menu.add_option('Szyfowanie Playfaira', '1', encode)
    menu.add_option('Deszyfowanie Playfaira', '2', decode)
    # Uruchomienie pętli głównej programu
    menu.run()
    pass
