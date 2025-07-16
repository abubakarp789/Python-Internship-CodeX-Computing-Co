# Student Report Card Generator

A comprehensive command-line application for managing student records and generating professional report cards in multiple formats. Developed with Python 3.x, this tool simplifies the process of creating and managing student academic reports.

## ✨ Features

### Student Management
- 👤 **Student Profiles**: Create and manage student records with names and unique roll numbers
- 🔢 **Duplicate Prevention**: Automatic detection of existing student IDs
- 📊 **Comprehensive Records**: Store and manage complete academic information

### Academic Management
- 📚 **Subject Management**: Add multiple subjects per student
- 🔢 **Marks Tracking**: Record and validate marks (0-100)
- 🎯 **Automatic Grading**: Instant grade calculation based on performance
- 📈 **Performance Analysis**: Calculate total marks, averages, and grades

### Report Generation
- 📝 **Multiple Formats**: Export reports in TXT, DOCX, and PDF formats
- 🎨 **Professional Layouts**: Clean, well-formatted output for all formats
- 🏆 **Grade Summary**: Clear presentation of results with visual indicators

### Data Management
- 💾 **Automatic Saving**: Data is persisted between sessions
- 🔄 **JSON Storage**: Simple, human-readable data storage
- 📂 **Organized Reports**: Generated reports are saved in a dedicated directory

## 🛠️ System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **Dependencies**: python-docx, reportlab

## 🚀 Getting Started

### Prerequisites

1. Ensure Python 3.7+ is installed:
   ```bash
   python --version
   ```

2. Update pip:
   ```bash
   python -m pip install --upgrade pip
   ```

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/abubakarp789/Python-Internship-CodeX-Computing-Co.git
   cd "Python-Internship-CodeX-Computing-Co/Student Report Card Generator"
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   # source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   If requirements.txt doesn't exist:
   ```bash
   pip install python-docx reportlab
   ```

## 🖥️ Usage

1. **Start the application**:
   ```bash
   python Student_Report_Generator.py
   ```

2. **Main Menu Options**:
   - **Add New Student**: Create a new student record
   - **Add Subjects/Marks**: Enter academic information
   - **View Report**: Generate and view a student's report
   - **Save Report**: Export report in preferred format
   - **Exit**: Save data and close the application

### Example Workflow

1. **Add a New Student**:
   - Select "Add New Student" from the main menu
   - Enter student name and roll number
   - The system validates the input and confirms creation

2. **Add Subjects and Marks**:
   - Select "Add Subjects/Marks"
   - Enter the roll number
   - Add subjects and corresponding marks (0-100)
   - The system calculates grades automatically

3. **Generate Reports**:
   - Select "View Report" to see a student's academic summary
   - Choose "Save Report" to export in TXT, DOCX, or PDF format
   - Reports are saved in the `reports/` directory

## 📁 Project Structure

```
Student Report Card Generator/
├── Student_Report_Generator.py  # Main application code
├── student_data.json           # Student records database
├── reports/                    # Generated report cards
├── requirements.txt            # Project dependencies
└── README.md                   # This documentation
```

## 🛠️ Development

### Code Organization
- **Student Class**: Handles student data and grade calculations
- **ReportCardGenerator Class**: Manages data persistence and report generation
- **UserInterface Class**: Handles command-line interactions

### Adding New Features
1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## 📊 Sample Report Output

### Text Format
```
==========================================
          ACADEMIC REPORT CARD           
==========================================

Student Name: Abu Bakar
Roll Number: 41

------------------------------------------
Subject          Marks   Grade   Status  
------------------------------------------
PF                92      A+     Pass    
OOP               88       A     Pass    
DBMS              95      A+     Pass    
DSA               78       B     Pass    
Algebra           92      A+     Pass    
------------------------------------------

Total Marks: 445/500
Average: 89.0%
Overall Grade: A
==========================================
```

## 🐛 Troubleshooting

### Common Issues

#### Missing Dependencies
```bash
ModuleNotFoundError: No module named 'docx'
```
Solution: Install the required packages:
```bash
pip install python-docx reportlab
```

#### Permission Errors
If you encounter permission issues when saving reports:
- Ensure the `reports` directory exists and is writable
- Run the program as administrator (Windows) or use `sudo` (Linux/macOS)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Abu Bakar**  
Python Developer | CodeX Computing Co. Intern  
[GitHub](https://github.com/abubakarp789) | [LinkedIn](https://www.linkedin.com/in/abubakar56/) | [Portfolio](https://abubakar056.netlify.app/)

---
*Developed as part of the Python Internship Program at CodeX Computing Co.*