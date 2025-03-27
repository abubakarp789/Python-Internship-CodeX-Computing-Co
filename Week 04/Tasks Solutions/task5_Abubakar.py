class Shape:
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print("Drawing a circle")

class Rectangle(Shape):
    def draw(self):
        print("Drawing a rectangle")

class Triangle(Shape):
    def draw(self):
        print("Drawing a triangle")

def draw_shape(shape):
    shape.draw()

circle = Circle()
rectangle = Rectangle()
triangle = Triangle()

draw_shape(circle)
draw_shape(rectangle)
draw_shape(triangle)