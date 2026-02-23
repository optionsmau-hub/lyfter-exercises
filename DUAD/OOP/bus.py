class Person:
    def __init__(self, name):
        self.name = name


class Bus:
    def __init__(self, max_passengers):
        self.max_passengers = max_passengers
        self.passengers = []

    def add_passenger(self, person):
        if len(self.passengers) < self.max_passengers:
            self.passengers.append(person)
            print(f"{person.name} got on the bus.")
        else:
            print("The bus is full.")

    def remove_passenger(self, person):
        if person in self.passengers:
            self.passengers.remove(person)
            print(f"{person.name} got off the bus.")
        else:
            print("That passenger is not on the bus.")


if __name__ == "__main__":
    bus = Bus(2)

    p1 = Person("Mauro")
    p2 = Person("Ana")
    p3 = Person("Luis")

    bus.add_passenger(p1)
    bus.add_passenger(p2)
    bus.add_passenger(p3)  # Should print "The bus is full."

    bus.remove_passenger(p1)
    bus.remove_passenger(p3)  # Not on bus