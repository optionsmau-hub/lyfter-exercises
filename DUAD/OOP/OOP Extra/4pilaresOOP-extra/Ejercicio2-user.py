# Exercise 2: Abstract User class with AdminUser and RegularUser
from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def has_permission(self, permission):
        pass


class AdminUser(User):
    def get_role(self):
        return "Admin"

    def has_permission(self, permission):
        return True


class RegularUser(User):
    def get_role(self):
        return "Regular"

    def has_permission(self, permission):
        return permission == "read"


# Test
user1 = AdminUser("Carlos")
user2 = RegularUser("Andrea")
print(user1.has_permission("delete"))  # True
print(user2.has_permission("delete"))  # False