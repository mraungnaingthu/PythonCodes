class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def getName(self):
        return self.name

    def getAge(self):
        return self.age

person = Person("John", 36)

print("His name is: ", person.getName())
print("His age is: ", person.getAge())

person.age = 20
while person.age < 60:
    person.age = person.age * 2
print(person.age)

