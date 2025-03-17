def trapezoid_area(base1, base2, height):
    return 0.5 * (base1 + base2) * height

def parallelogram_area(base, height):
    return base * height

def cylinder_area_volume(radius, height):
    surface_area = 2 * 3.14159 * radius * (radius + height)
    volume = 3.14159 * radius**2 * height
    return surface_area, volume

if __name__ == "__main__":
    print("Choose a shape to calculate area:")
    print("1. Trapezoid")
    print("2. Parallelogram")
    print("3. Cylinder (Surface Area and Volume)")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        base1 = float(input("Enter base 1 of trapezoid: "))
        base2 = float(input("Enter base 2 of trapezoid: "))
        height = float(input("Enter height of trapezoid: "))
        area = trapezoid_area(base1, base2, height)
        print(f"Area of trapezoid: {area}")
    elif choice == '2':
        base = float(input("Enter base of parallelogram: "))
        height = float(input("Enter height of parallelogram: "))
        area = parallelogram_area(base, height)
        print(f"Area of parallelogram: {area}")
    elif choice == '3':
        radius = float(input("Enter radius of cylinder: "))
        height = float(input("Enter height of cylinder: "))
        surface_area, volume = cylinder_area_volume(radius, height)
        print(f"Surface Area of cylinder: {surface_area}")
        print(f"Volume of cylinder: {volume}")
    else:
        print("Invalid choice")