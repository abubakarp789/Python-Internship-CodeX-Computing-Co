class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def display_info(self):
        print("Student ID:", self.student_id)
        print("Name:", self.name)


class Marks(Student):
    def __init__(self, student_id, name, marks_algo, marks_dataScience, marks_calculus):
        super().__init__(student_id, name)
        self.marks_algo = marks_algo
        self.marks_dataScience = marks_dataScience
        self.marks_calculus = marks_calculus

    def display_marks(self):
        print("Marks in Algorithm:", self.marks_algo)
        print("Marks in Data Science:", self.marks_dataScience)
        print("Marks in Calculus:", self.marks_calculus)


class Result(Marks):
    def calculate_total_marks(self):
        total_marks = self.marks_algo + self.marks_dataScience + self.marks_calculus
        return total_marks

    def calculate_average_marks(self):
        total_marks = self.calculate_total_marks()
        average_marks = total_marks / 3
        return average_marks

    def display_result(self):
        self.display_info()
        self.display_marks()
        total_marks = self.calculate_total_marks()
        average_marks = self.calculate_average_marks()
        print("Total Marks:", total_marks)
        print("Average Marks:", average_marks)


# Create an object of the Result class
result = Result(41, "Abu Bakar", 90, 85, 95)

# Display student details, marks, total marks, and average marks
result.display_result()