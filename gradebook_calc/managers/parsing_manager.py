# gradebook_calc/managers/parsing_manager.py

import json
import csv
import io

def parse_curriculum(csv_string: str) -> list[dict]:
    """
    Parses the curriculum CSV string and performs validation.
    The CSV format must be: Semester,Teaching unit,Course,Credits

    Args:
        csv_string: A string containing the CSV data for the curriculum.

    Returns:
        A list of dictionaries representing the parsed curriculum.

    Raises:
        ValueError: If the CSV is invalid or headers are incorrect.
    """
    try:
        file_like_object = io.StringIO(csv_string)
        reader = csv.DictReader(file_like_object)
        
        # --- Validation ---
        expected_headers = ['Semester', 'Teaching unit', 'Course', 'Credits']
        if not reader.fieldnames or any(h not in reader.fieldnames for h in expected_headers):
            raise ValueError(f"Invalid curriculum format. Headers must be: {', '.join(expected_headers)}")

        curriculum_data = list(reader)
        if not curriculum_data:
            raise ValueError("Curriculum file is empty or contains only a header.")
            
        # Optional: Further validation on rows
        for i, row in enumerate(curriculum_data):
            if not row.get('Credits') or not row.get('Credits').isdigit():
                raise ValueError(f"Invalid 'Credits' value in row {i+2}. Must be a number.")

        return curriculum_data
        
    except Exception as e:
        raise ValueError(f"Error parsing curriculum CSV: {e}")
    

def parse_grades(csv_string: str) -> list[dict]:
    """
    Parses the student grades CSV string and performs validation.

    Args:
        csv_string: A string containing the CSV data for student grades.

    Returns:
        A list of dictionaries, where each dictionary represents a row.

    Raises:
        ValueError: If the CSV is malformed or missing required columns.
    """
    try:
        # Use io.StringIO to treat the string as a file for the csv reader.
        file_like_object = io.StringIO(csv_string)
        reader = csv.DictReader(file_like_object)
        
        # Check for required headers
        required_cols = ['Student Name','Course','Teacher Name','Semestre 1 Grade','Semestre 2 Grade','Comments']
        if not all(col in reader.fieldnames for col in required_cols):
            missing_cols = [col for col in required_cols if col not in reader.fieldnames]
            raise ValueError(f"CSV file is missing required columns: {', '.join(missing_cols)}")

        grades = list(reader)
        if not grades:
            raise ValueError("CSV file is empty or contains only a header row.")
            
        return grades
    except Exception as e:
        # Re-raise validation errors or catch other parsing issues.
        raise ValueError(f"Error parsing CSV: {e}")

