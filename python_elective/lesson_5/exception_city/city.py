

class CitySizeExeption(Exception):
    def __init__(self, msg, count1, count2):
        self.msg = msg
        self.count1 = count1
        self.count2 = count2
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.msg}. The free space is {self.count2}, the number of persons is {self.count1}'
    

class City():
    __max_count = 100
    __free_city_space = 100
    __cur_count = 0

    def __init__(self, name, count):
        val = min(count, City.__max_count)

        self._name = name

        self._max_count = val
        self._cur_count = 0
        City.__free_city_space -= val

    def add_person(self):
        try:
            assert self._cur_count < self._max_count, CitySizeExeption("There is no free places for residents in the city {}".format(self._name), self._cur_count, self._max_count)
            self._cur_count += 1
            City.__cur_count += 1
        except Exception as e:
            raise e


    def remove_person(self):
        try:
            assert self._cur_count > 0, "There is no residents in the city {}".format(self._name)
            self._cur_count -= 1
            City.__cur_count -= 1
        except Exception as e:
            raise e

    def __str__(self):
        s = []
        s.append("------------------------ \n")
        s.append("Agglomeration: \n")
        s.append("------------------------\n")
        s.append("\n")
        s.append("Max_person_count: {}\n".format(City.__max_count))
        s.append("Free_counts_for_city: {}\n".format(City.__free_city_space))
        s.append("\n")

        s.append("------------------------ \n")
        s.append("City: \n")
        s.append("------------------------\n")
        s.append("\n")
        s.append("Name: {}\n".format(self._name))
        s.append("Max_person_count: {}\n".format(self._max_count))
        s.append("Cur_count: {}\n".format(self._cur_count))
        s.append("\n")

        return ''.join(s)