# import traceback
#
# title = 'hello to the world'
#
# iter = iter(title)
#
# try:
#     while True:
#         print(next(iter))
# except StopIteration as e:
#     print("Iteration finished")

class Person:
    def __init__(self, name):
        self.name = name
        self.index = 0  # Start index at 0 for iteration

    def __iter__(self):
        return self  # Return self as an iterator

    def __next__(self):
        if self.index >= len(self.name):  # Check if index exceeds the name length
            raise StopIteration
        char = self.name[self.index]  # Get the current character
        self.index += 1  # Move to the next character
        return char

# Create an instance of Person
it = Person('Robert')

# Iterate over the Person object
for char in it:
    print(char)