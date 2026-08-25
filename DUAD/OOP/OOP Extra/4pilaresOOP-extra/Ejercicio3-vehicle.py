# Exercise 3: Vehicle base class with Car and Motorcycle subclasses
class Vehicle:
    def __init__(self, brand, year):
        self._brand = brand
        self._year = year

    def get_info(self):
        return f"{self._brand} ({self._year})"


class Car(Vehicle):
    def __init__(self, brand, year, doors):
        super().__init__(brand, year)
        self._doors = doors

    def get_info(self):
        return f"{self._brand} ({self._year}) - {self._doors} puertas"


class Motorcycle(Vehicle):
    def __init__(self, brand, year, type):
        super().__init__(brand, year)
        self._type = type

    def get_info(self):
        return f"{self._brand} ({self._year}) - Tipo: {self._type}"


# Test
vehicle1 = Car("Toyota", 2020, 4)
vehicle2 = Motorcycle("Yamaha", 2022, "Deportiva")
print(vehicle1.get_info())  # Toyota (2020) - 4 puertas
print(vehicle2.get_info())  # Yamaha (2022) - Tipo: Deportiva