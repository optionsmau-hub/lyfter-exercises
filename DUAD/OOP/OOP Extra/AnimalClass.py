class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Makes a sound"


class Dog(Animal):
    def speak(self):
        return "Woof"


class Cat(Animal):
    def speak(self):
        return "Meow"


# --- Example ---
dog = Dog("Firulais")
print(dog.speak())  # Woof

cat = Cat("Michi")
print(cat.speak())  # Meow