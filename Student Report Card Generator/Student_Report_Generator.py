# Student Report Card Generator with Word and PDF Export
# Author: Abu Bakar

# Import required libraries
# You need to install these libraries first using:
# pip install python-docx reportlab

import os
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# Create reports directory if it doesn't exist
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

class Student:
    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number
        self.subjects = {}
        self.total_marks = 0
        self.average = 0
        self.grade = ""
    
    def add_subject(self, subject, marks):
        """Add a subject and its marks for the student"""
        try:
            marks = float(marks)
            if 0 <= marks <= 100:
                self.subjects[subject] = marks
                return True
            else:
                print("Error: Marks should be between 0 and 100")
                return False
        except ValueError:
            print("Error: Please enter a valid number for marks")
            return False
    
    def calculate_results(self):
        """Calculate total marks, average, and grade"""
        if not self.subjects:
            return False
            
        self.total_marks = sum(self.subjects.values())
        self.average = self.total_marks / len(self.subjects)
        
        # Determine grade based on average marks
        if self.average >= 90:
            self.grade = "A+"
        elif self.average >= 80:
            self.grade = "A"
        elif self.average >= 70:
            self.grade = "B"
        elif self.average >= 60:
            self.grade = "C"
        elif self.average >= 50:
            self.grade = "D"
        else:
            self.grade = "F"
        
        return True


class ReportCardGenerator:
    def __init__(self):
        self.students = []
    
    def add_student(self, name, roll_number):
        """Create and add a new student"""
        student = Student(name, roll_number)
        self.students.append(student)
        return student
    
    def find_student(self, roll_number):
        """Find a student by roll number"""
        for student in self.students:
            if student.roll_number == roll_number:
                return student
        return None
    
    def generate_text_report(self, student):
        """Generate a text report for a student"""
        if not student.subjects:
            print("No subjects added for this student.")
            return None
            
        # Calculate results before generating report
        student.calculate_results()
        
        report = []
        report.append("=" * 60)
        report.append(f"STUDENT REPORT CARD".center(60))
        report.append("=" * 60)
        report.append(f"Name: {student.name}")
        report.append(f"Roll Number: {student.roll_number}")
        report.append("-" * 60)
        report.append(f"{'Subject':<30}{'Marks':>10}")
        report.append("-" * 60)
        
        for subject, marks in student.subjects.items():
            report.append(f"{subject:<30}{marks:>10.2f}")
        
        report.append("-" * 60)
        report.append(f"{'Total Marks':<30}{student.total_marks:>10.2f}")
        report.append(f"{'Average':<30}{student.average:>10.2f}")
        report.append(f"{'Grade':<30}{student.grade:>10}")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_report_to_text_file(self, student):
        """Save the report card to a text file"""
        report_text = self.generate_text_report(student)
        if not report_text:
            return False
            
        try:
            filename = os.path.join(REPORTS_DIR, f"{student.name}_{student.roll_number}_report.txt")
            with open(filename, 'w') as file:
                file.write(report_text)
            print(f"Report card saved as '{filename}'")
            return True
        except Exception as e:
            print(f"Error saving text file: {e}")
            return False
    
    def save_report_to_word(self, student):
        """Save the report card as a Word document"""
        if not student.subjects:
            print("No subjects added for this student.")
            return False
            
        # Calculate results before generating report
        student.calculate_results()
        
        try:
            doc = Document()
            
            # Add title
            doc.add_heading('STUDENT REPORT CARD', 0)
            
            # Add student details
            doc.add_paragraph(f'Name: {student.name}')
            doc.add_paragraph(f'Roll Number: {student.roll_number}')
            
            # Add subject and marks table
            table = doc.add_table(rows=1, cols=2)
            table.style = 'Table Grid'
            
            # Add header row
            header_cells = table.rows[0].cells
            header_cells[0].text = 'Subject'
            header_cells[1].text = 'Marks'
            
            # Add subjects and marks
            for subject, marks in student.subjects.items():
                row_cells = table.add_row().cells
                row_cells[0].text = subject
                row_cells[1].text = f"{marks:.2f}"
            
            # Add summary row
            doc.add_paragraph('')
            summary_table = doc.add_table(rows=3, cols=2)
            summary_table.style = 'Table Grid'
            
            # Add total, average, and grade
            total_row = summary_table.rows[0].cells
            total_row[0].text = 'Total Marks'
            total_row[1].text = f"{student.total_marks:.2f}"
            
            avg_row = summary_table.rows[1].cells
            avg_row[0].text = 'Average'
            avg_row[1].text = f"{student.average:.2f}"
            
            grade_row = summary_table.rows[2].cells
            grade_row[0].text = 'Grade'
            grade_row[1].text = student.grade
            
            # Save document
            filename = os.path.join(REPORTS_DIR, f"{student.name}_{student.roll_number}_report.docx")
            doc.save(filename)
            print(f"Report card saved as Word document: '{filename}'")
            return True
        except Exception as e:
            print(f"Error saving Word document: {e}")
            return False
    
    def save_report_to_pdf(self, student):
        """Save the report card as a PDF document"""
        if not student.subjects:
            print("No subjects added for this student.")
            return False
            
        # Calculate results before generating report
        student.calculate_results()
        
        try:
            filename = os.path.join(REPORTS_DIR, f"{student.name}_{student.roll_number}_report.pdf")
            doc = SimpleDocTemplate(filename, pagesize=letter)
            
            # Create content list
            elements = []
            
            # Add styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Heading1'],
                alignment=TA_CENTER,
                spaceAfter=12
            )
            
            # Add title
            elements.append(Paragraph("STUDENT REPORT CARD", title_style))
            elements.append(Spacer(1, 12))
            
            # Add student details
            elements.append(Paragraph(f"Name: {student.name}", styles["Normal"]))
            elements.append(Paragraph(f"Roll Number: {student.roll_number}", styles["Normal"]))
            elements.append(Spacer(1, 12))
            
            # Create subject and marks table
            subject_data = [['Subject', 'Marks']]
            for subject, marks in student.subjects.items():
                subject_data.append([subject, f"{marks:.2f}"])
            
            subject_table = Table(subject_data, colWidths=[300, 100])
            subject_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(subject_table)
            elements.append(Spacer(1, 12))
            
            # Create summary table
            summary_data = [
                ['Total Marks', f"{student.total_marks:.2f}"],
                ['Average', f"{student.average:.2f}"],
                ['Grade', student.grade]
            ]
            
            summary_table = Table(summary_data, colWidths=[300, 100])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(summary_table)
            
            # Build PDF
            doc.build(elements)
            print(f"Report card saved as PDF document: '{filename}'")
            return True
        except Exception as e:
            print(f"Error saving PDF document: {e}")
            return False


def main():
    print("STUDENT REPORT CARD GENERATOR")
    print("=" * 30)
    
    generator = ReportCardGenerator()
    
    while True:
        print("\nMenu:")
        print("1. Add a new student")
        print("2. Add subjects and marks")
        print("3. Generate and view report card")
        print("4. Save report card (Text, Word, PDF)")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            name = input("Enter student name: ")
            roll_number = input("Enter roll number: ")
            student = generator.add_student(name, roll_number)
            print(f"Student '{name}' added successfully!")
            
        elif choice == '2':
            roll_number = input("Enter student roll number: ")
            student = generator.find_student(roll_number)
            
            if student:
                print(f"\nAdding subjects for {student.name}")
                while True:
                    subject = input("\nEnter subject name (or 'done' to finish): ")
                    if subject.lower() == 'done':
                        break
                        
                    marks = input(f"Enter marks for {subject}: ")
                    if student.add_subject(subject, marks):
                        print(f"Subject '{subject}' added successfully!")
            else:
                print("Student not found.")
                
        elif choice == '3':
            roll_number = input("Enter student roll number: ")
            student = generator.find_student(roll_number)
            
            if student:
                if not student.subjects:
                    print("No subjects added for this student yet.")
                    continue
                    
                print("\nStudent Report Card:")
                report_text = generator.generate_text_report(student)
                print(report_text)
            else:
                print("Student not found.")
                
        elif choice == '4':
            roll_number = input("Enter student roll number: ")
            student = generator.find_student(roll_number)
            
            if student:
                if not student.subjects:
                    print("No subjects added for this student yet.")
                    continue
                
                print("\nSave report card as:")
                print("1. Text file")
                print("2. Word document")
                print("3. PDF document")
                print("4. All formats")
                
                save_choice = input("Enter your choice (1-4): ")
                
                if save_choice == '1':
                    generator.save_report_to_text_file(student)
                elif save_choice == '2':
                    generator.save_report_to_word(student)
                elif save_choice == '3':
                    generator.save_report_to_pdf(student)
                elif save_choice == '4':
                    generator.save_report_to_text_file(student)
                    generator.save_report_to_word(student)
                    generator.save_report_to_pdf(student)
                else:
                    print("Invalid choice.")
            else:
                print("Student not found.")
                
        elif choice == '5':
            print("Thank you for using the Student Report Card Generator!")
            break
            
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()