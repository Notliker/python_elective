
from exception_city.person import Person
from exception_city.city_list import CityList



if __name__ == '__main__':
    try:
        c3 = CityList("City_with_named_persons", 10)

        for i in range(15):
            s = str(i)
            c3.add_person(Person(s,s+s, s+s+s))
        #print(c3)

        for i in range(2,10,2):
            c3.remove_person(i)
        print(c3)
        raise RuntimeWarning("The code is finished")
    except Exception as e:
        print(e)

    finally:
        print("The code block is finished")