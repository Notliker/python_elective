class Person:
    def __init__(self, first_name, last_name, middle_name=None, gender='M'):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.gender = gender
        self.children = []
        self.spouse = None
    
    def get_full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
    def marry(self, person):
        self.spouse = person
        person.spouse = self
    
    def add_child(self, child):
        self.children.append(child)


class Child(Person):
    def __init__(self, first_name, father=None, mother=None, gender='M', new_branch=False):
        if father and not new_branch:
            last_name = father.last_name
            middle_name = father.first_name 
        else:
            last_name = "New last_name"
            middle_name = None
        
        super().__init__(first_name, last_name, middle_name, gender)
        
        self.father = father
        self.mother = mother
        
        if father:
            father.add_child(self)
        if mother and mother not in [father]:
            mother.add_child(self)


class Family:
    def __init__(self, family_name):
        self.family_name = family_name
        self.members = []
    
    def add_member(self, person):
        self.members.append(person)
    
    def show_family(self):
        print(f"\n{'='*50}")
        print(f"Family {self.family_name}")
        print(f"{'='*50}")
        for member in self.members:
            info = f"  {member.get_full_name()} ({member.gender})"
            if member.children:
                info += f"\n    Kids: {', '.join([c.first_name for c in member.children])}"
            print(info)
        print(f"{'='*50}\n")


class City:
    def __init__(self, name):
        self.name = name
        self.families = []
    
    def add_family(self, family):
        self.families.append(family)
    
    def show_city(self):
        print(f"\n{'='*60}")
        print(f"City: {self.name}")
        print(f"Count of family: {len(self.families)}")
        print(f"{'='*60}")
        for family in self.families:
            family.show_family()


print("="*50)

ivan = Person("Ivan", "Ivanov", gender='M')
anna = Person("Anna", "Smirnova", gender='F')
ivan.marry(anna)

dmitry = Child("Dmitriy", father=ivan, mother=anna, gender='M')

elena = Person("Elena", "Kotova", gender='F')
dmitry.marry(elena)

mikhail = Child("Mikhail", father=dmitry, mother=elena, gender='M')
sofia = Child("Sofia", father=dmitry, mother=elena, gender='F')

print(f"Grandpa: {ivan.get_full_name()}")
print(f"Grandma: {anna.get_full_name()}")
print(f"Son: {dmitry.get_full_name()}")
print(f"Mother: {elena.get_full_name()}")
print(f"Grandson: {mikhail.get_full_name()}")
print(f"Granddaughter: {sofia.get_full_name()}")

city = City("Москва")

family1 = Family("Ivanov")
family1.add_member(ivan)
family1.add_member(dmitry)
family1.add_member(mikhail)
family1.add_member(sofia)
city.add_family(family1)

family2 = Family("Smirnova")
family2.add_member(anna)
city.add_family(family2)

family3 = Family("Kotova")
family3.add_member(elena)
city.add_family(family3)

city.show_city()
