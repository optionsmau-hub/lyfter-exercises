class Rectangle:
    def __init__(self, width, height):
        if width < 0 or height < 0:
            raise ValueError("There is a negative value, values must be positive")
        
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return 2 * (self.width + self.height)


# --- Example usage ---
try:
    height = int(input("Enter height: "))
    width = int(input("Enter width: "))

    rectangle = Rectangle(width, height)

    print(rectangle.get_area())       # 75000
    print(rectangle.get_perimeter())  # 1100

except ValueError as e:
    print(e)