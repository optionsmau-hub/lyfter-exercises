from abc import ABC, abstractmethod
import math


# Exercise 1
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraw amount must be greater than 0.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount


class SavingsAccount(BankAccount):
    def __init__(self, balance, min_balance):
        super().__init__(balance)
        self.min_balance = min_balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraw amount must be greater than 0.")
        if self.balance - amount < self.min_balance:
            raise ValueError("Cannot withdraw: balance would go below minimum balance.")
        self.balance -= amount


# Exercise 2
class Shape(ABC):
    @abstractmethod
    def calculate_perimeter(self):
        pass

    @abstractmethod
    def calculate_area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_perimeter(self):
        return 2 * math.pi * self.radius

    def calculate_area(self):
        return math.pi * (self.radius ** 2)


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def calculate_perimeter(self):
        return 4 * self.side

    def calculate_area(self):
        return self.side ** 2


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_perimeter(self):
        return 2 * (self.length + self.width)

    def calculate_area(self):
        return self.length * self.width


# Exercise 3
class Walker:
    def walk(self):
        return "I can walk."


class Speaker:
    def speak(self):
        return "I can speak."


class RobotAssistant(Walker, Speaker):
    def assist(self):
        return "I can assist humans."


# Testing
if __name__ == "__main__":
    print("=== Exercise 1 ===")
    account = BankAccount(1000)
    account.deposit(200)
    account.withdraw(300)
    print("BankAccount balance:", account.balance)

    savings = SavingsAccount(1000, 200)
    savings.withdraw(500)
    print("SavingsAccount balance:", savings.balance)

    print("\n=== Exercise 2 ===")
    circle = Circle(5)
    print("Circle perimeter:", circle.calculate_perimeter())
    print("Circle area:", circle.calculate_area())

    square = Square(4)
    print("Square perimeter:", square.calculate_perimeter())
    print("Square area:", square.calculate_area())

    rectangle = Rectangle(6, 3)
    print("Rectangle perimeter:", rectangle.calculate_perimeter())
    print("Rectangle area:", rectangle.calculate_area())

    print("\n=== Exercise 3 ===")
    robot = RobotAssistant()
    print(robot.walk())
    print(robot.speak())
    print(robot.assist())