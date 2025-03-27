from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side

# Create instances of the derived classes
rectangle = Rectangle(4, 5)
triangle = Triangle(3, 6)
square = Square(2)

# Calculate and print the areas
print("Area of Rectangle:", rectangle.area())
print("Area of Triangle:", triangle.area())
print("Area of Square:", square.area())