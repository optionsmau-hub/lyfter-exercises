class Employee:
    def __init__(self, name, salary):
        self._name = name
        self._salary = salary

    @property
    def name(self):
        return self._name

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = value

    def promote(self, percentage):
        self.salary = self._salary + (self._salary * percentage)


# Test
employee = Employee("Ana", 1000)
employee.promote(0.1)
print(employee.salary)  # 1100