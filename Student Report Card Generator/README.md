# **Student Report Card Generator**

## Project Overview
This is my first mini project as part of my Python internship with **CodeX Computing Co.** The Student Report Card Generator is a comprehensive system that allows users to create, manage, and generate student report cards in multiple formats.

## Features
- Create and manage student records
- Add subjects and marks for students
- Generate report cards in multiple formats:
  - Text files (.txt)
  - Word documents (.docx)
  - PDF documents (.pdf)
- Automatic grade calculation based on marks
- Data persistence using JSON storage
- Input validation and error handling
- User-friendly command-line interface

## Technical Details
- **Language**: Python 3.x
- **Dependencies**:
  - python-docx: For Word document generation
  - reportlab: For PDF document generation
  - dataclasses: For structured data handling
  - typing: For type hints and annotations

## Installation
1. Clone the repository:
```bash
git clone https://github.com/abubakarp789/Python-Internship-CodeX-Computing-Co
```

2. Navigate to the Student Report Card Generator folder:
```bash
cd Python-Internship-CodeX-Computing-Co/Student Report Card Generator
```

3. Install the required dependencies:
```bash
pip install python-docx reportlab
```

## Usage
1. Run the program:
```bash
python Student_Report_Generator.py
```

2. Follow the menu prompts to:
   - Add new students
   - Add subjects and marks
   - View report cards
   - Save report cards in different formats

## Project Structure
```
Student Report Card Generator/
├── Student_Report_Generator.py  
├── reports/
│   └── Abu Bakar_41_report.pdf
└── student_data.json 
```

## Features in Detail
1. **Student Management**
   - Add new students with name and roll number
   - Validate student information
   - Prevent duplicate roll numbers

2. **Subject Management**
   - Add multiple subjects for each student
   - Input validation for marks (0-100)
   - Automatic grade calculation

3. **Report Generation**
   - Generate reports in multiple formats
   - Professional formatting for all output types
   - Consistent styling across formats

4. **Data Persistence**
   - Automatic saving of student data
   - JSON-based storage system
   - Data recovery on program restart

## About the Internship
This project was developed as part of my Python internship with CodeX Computing Co. It demonstrates my understanding of:
- Object-oriented programming in Python
- File handling and data persistence
- User interface design
- Error handling and input validation
- Documentation and code organization

## Author
**Abu Bakar**
Python Intern at CodeX Computing Co.

## License
This project is part of the CodeX Computing Co. internship program. 