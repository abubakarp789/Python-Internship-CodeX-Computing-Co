class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def calculateBonus(self):
        return 0

class Manager(Employee):
    def hire(self):
        print("Manager is hiring someone")

    def calculateBonus(self):
        bonus = self.salary * 0.2
        return bonus

class Developer(Employee):
    def writeCode(self):
        print("Developer is writing code")

    def calculateBonus(self):
        bonus = self.salary * 0.1
        return bonus

class SeniorManager(Manager):
    def calculateBonus(self):
        bonus = self.salary * 0.3
        return bonus

employee1 = Employee("John Doe", 5000)
manager1 = Manager("Jane Smith", 8000)
developer1 = Developer("Mike Johnson", 6000)
seniorManager1 = SeniorManager("Emily Brown", 10000)

employee1.calculateBonus()
manager1.hire()
developer1.writeCode()
seniorManager1.calculateBonus()