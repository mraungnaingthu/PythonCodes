from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    salary: float

john = Person('John', 22, 20000.0)

print(john.name)
print(john.age)
print(john.salary)