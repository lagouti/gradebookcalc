# gradebook_calc/managers/parsing_manager.py

import csv
from io import StringIO

def parse_curriculum(file_content: str):
    """Parses the curriculum CSV content into a list of dictionaries."""
    if not file_content:
        raise ValueError("Curriculum file content is empty.")
    
    reader = csv.DictReader(StringIO(file_content))
    return [row for row in reader]

def is_numerical(value: str):
    """Checks if a string can be interpreted as a number (int or float). Handles percentages."""
    if not value:
        return False
    value = value.strip()
    if value.endswith('%'):
        value = value[:-1]
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def analyze_and_parse_grades(file_content: str):
    """
    Analyzes a grades CSV file to find student count, a course descriptor column, 
    and grade columns. It then transforms the data from wide format to long format.
    """
    if not file_content:
        raise ValueError("Grades file content is empty.")

    reader = list(csv.reader(StringIO(file_content)))
    header = reader[0]
    data_rows = reader[1:]

    if not data_rows:
        return {"student_count": 0, "grade_columns": [], "parsed_data": []}

    student_count = len(set(row[0] for row in data_rows if row))

    # --- Enhanced Column Identification ---
    student_col_idx = 0
    course_col_idx = -1 # Default to no course column
    grade_col_indices = {}

    for i, col_name in enumerate(header):
        if i == student_col_idx:
            continue
        
        # Check if any cell in the column is numerical to identify it as a grade column
        is_grade_col = any(row and len(row) > i and is_numerical(row[i]) for row in data_rows)

        if is_grade_col:
            grade_col_indices[col_name] = i
        elif course_col_idx == -1:  # Assume the first non-student, non-grade column is the course descriptor
            course_col_idx = i

    grade_columns = list(grade_col_indices.keys())

    # --- Transformation ---
    parsed_data = []
    for row in data_rows:
        if not row or not row[student_col_idx]:
            continue
        
        student_name = row[student_col_idx]
        # Use the identified course column, or default if none was found
        course_name = row[course_col_idx] if course_col_idx != -1 and len(row) > course_col_idx else 'N/A'

        for assignment_name, grade_col_idx in grade_col_indices.items():
            if len(row) > grade_col_idx and row[grade_col_idx] is not None and row[grade_col_idx].strip() != '':
                grade_value = row[grade_col_idx]
                parsed_data.append({
                    "Student Name": student_name,
                    "Course": course_name,
                    "Assignment Name": assignment_name,
                    "Grade": grade_value
                })

    return {
        "student_count": student_count,
        "grade_columns": grade_columns,
        "parsed_data": parsed_data
    }


def parse_grades(file_content: str):
    """
    (Legacy) Parses a simple, long-format grades CSV.
    Replaced by analyze_and_parse_grades for more complex logic.
    """
    if not file_content:
        raise ValueError("Grades file content is empty.")
    
    reader = csv.DictReader(StringIO(file_content))
    expected_cols = {'student_name', 'assignment_name', 'grade'}
    if not expected_cols.issubset(set(reader.fieldnames)):
        raise ValueError("Grades file is missing one of the required columns: student_name, assignment_name, grade")
    return [row for row in reader]