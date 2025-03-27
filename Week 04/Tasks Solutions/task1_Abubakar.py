class Vehicle:
    def __init__(self, seating_capacity):
        self.seating_capacity = seating_capacity

    def calculate_fare(self):
        return self.seating_capacity * 100

class Bus(Vehicle):
    def calculate_fare(self):
        base_fare = super().calculate_fare()
        total_fare = base_fare + (base_fare * 0.1)
        return total_fare

bus = Bus(50)
print(bus.calculate_fare())  # Output: 5500.0

bus = Bus(100)
print(bus.calculate_fare())  # Output: 11000.0