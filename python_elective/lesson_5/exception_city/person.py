
class Person:
    def __init__(self, _name,_surname,_midname):
        self._name = _name
        self._surname = _surname
        self._middle_name = _midname

    def __str__(self):
        return "{} {} {}".format(self._name, self._surname, self._middle_name)

