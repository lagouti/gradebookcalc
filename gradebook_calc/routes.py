# gradebook_calc/routes.py

from flask import Blueprint, request, jsonify, render_template, session, current_app
import os

# Import the manager modules that contain the business logic.
from .managers import parsing_manager, calculation_manager

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Serves the main user interface."""
    session.clear()
    return render_template('index.html')


@main_bp.route('/api/curriculums', methods=['GET'])
def list_curriculums_api():
    """Scans the curriculum directory and returns a list of available CSV files."""
    try:
        curriculum_dir = current_app.config['CURRICULUM_DIR']
        files = [f for f in os.listdir(curriculum_dir) if f.endswith('.csv')]
        return jsonify(files), 200
    except Exception as e:
        print(f"Error listing curriculum files: {e}")
        return jsonify({"error": "Could not read curriculum directory."}), 500


@main_bp.route('/api/grades', methods=['GET'])
def list_grades_api():
    """Scans the grades directory and returns a list of available CSV files."""
    try:
        grades_dir = current_app.config['GRADES_DIR']
        files = [f for f in os.listdir(grades_dir) if f.endswith('.csv')]
        return jsonify(files), 200
    except Exception as e:
        print(f"Error listing grades files: {e}")
        return jsonify({"error": "Could not read grades directory."}), 500


@main_bp.route('/api/load/curriculum', methods=['POST'])
def load_curriculum_api():
    """Loads a specific curriculum file by name and returns its content."""
    try:
        data = request.get_json()
        filename = data.get('filename')
        if not filename:
            return jsonify({"error": "Filename not provided."}), 400

        curriculum_dir = current_app.config['CURRICULUM_DIR']
        file_path = os.path.abspath(os.path.join(curriculum_dir, filename))
        if not file_path.startswith(os.path.abspath(curriculum_dir)):
            return jsonify({"error": "Invalid file path."}), 400
        
        if not os.path.exists(file_path):
            return jsonify({"error": f"File '{filename}' not found."}), 404

        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        curriculum_data = parsing_manager.parse_curriculum(file_content)
        session['curriculum'] = curriculum_data
        
        summary = f"Loaded '{filename}' with {len(curriculum_data)} courses."
        return jsonify({
            "message": "Curriculum loaded successfully.",
            "summary": summary,
            "data": curriculum_data
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


@main_bp.route('/api/load/grades', methods=['POST'])
def load_grades_api():
    """Analyzes a grades file and returns a summary."""
    try:
        data = request.get_json()
        filename = data.get('filename')
        if not filename:
            return jsonify({"error": "Filename not provided."}), 400

        grades_dir = current_app.config['GRADES_DIR']
        file_path = os.path.abspath(os.path.join(grades_dir, filename))
        if not file_path.startswith(os.path.abspath(grades_dir)):
            return jsonify({"error": "Invalid file path."}), 400
        
        if not os.path.exists(file_path):
            return jsonify({"error": f"File '{filename}' not found."}), 404

        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        analysis = parsing_manager.analyze_and_parse_grades(file_content)
        session['grades'] = analysis['parsed_data']
        
        summary = f"Loaded and analyzed '{filename}'."
        
        return jsonify({
            "message": "Grades analyzed successfully.",
            "summary": summary,
            "data": {
                "student_count": analysis['student_count'],
                "grade_columns": analysis['grade_columns']
            }
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


@main_bp.route('/api/students', methods=['GET'])
def get_students_api():
    """Returns a list of unique student names from the loaded grades data."""
    if 'grades' not in session:
        return jsonify({"error": "Grades data not loaded."}), 400
    
    grades = session['grades']
    student_names = sorted(list(set(entry['Student Name'] for entry in grades)))
    return jsonify(student_names), 200


@main_bp.route('/api/grades/<student_name>', methods=['GET'])
def get_student_grades_api(student_name):
    """
    Returns all grade entries for a specific student, joined with curriculum data
    and with grades converted to a 20-point scale.
    """
    if 'grades' not in session or 'curriculum' not in session:
        return jsonify({"error": "Both grades and curriculum data must be loaded."}), 400
        
    grades = session['grades']
    curriculum = session['curriculum']
    
    curriculum_lookup = {course['Course']: course for course in curriculum}
    
    student_grades = [entry for entry in grades if entry['Student Name'] == student_name]
    
    if not student_grades:
        return jsonify({"error": "Student not found."}), 404
    
    enriched_grades = []
    for grade_entry in student_grades:
        course_name = grade_entry.get('Course')
        curriculum_info = curriculum_lookup.get(course_name)
        
        grade_20_scale = "N/A"
        try:
            percentage_str = grade_entry.get('Grade', '0').strip().replace('%', '')
            percentage_float = float(percentage_str)
            grade_20_scale = round((percentage_float / 100) * 20, 2)
        except (ValueError, TypeError):
            pass

        enriched_entry = {
            **grade_entry,
            "Credits": "N/A",
            "Teaching unit": "N/A",
            "Semester": "N/A",
            "Grade (0-20)": grade_20_scale
        }

        if curriculum_info:
            enriched_entry["Credits"] = curriculum_info.get('Credits', 'N/A')
            enriched_entry["Teaching unit"] = curriculum_info.get('Teaching unit', 'N/A')
            enriched_entry["Semester"] = curriculum_info.get('Semester', 'N/A')
            
        enriched_grades.append(enriched_entry)
            
    return jsonify(enriched_grades), 200


@main_bp.route('/api/semesters', methods=['GET'])
def get_semesters_api():
    """Extracts and returns a list of unique semesters from the curriculum data."""
    if 'curriculum' not in session:
        return jsonify({"error": "Curriculum data not loaded."}), 400
    
    curriculum = session['curriculum']
    semesters = sorted(list(set(c.get('Semester') for c in curriculum if c.get('Semester'))))
    return jsonify(semesters), 200


@main_bp.route('/api/calculate', methods=['POST'])
def calculate_api():
    """API endpoint for calculating final grade averages for a specific student and semester."""
    try:
        if 'curriculum' not in session or 'grades' not in session:
            return jsonify({"error": "Required data not loaded."}), 400
        
        data = request.get_json()
        student_name = data.get('student_name')
        semester = data.get('semester')

        if not student_name or not semester:
            return jsonify({"error": "Student name and semester must be provided."}), 400

        curriculum = session['curriculum']
        grades = session['grades']
        
        final_grades_summary = calculation_manager.calculate_final_grades(curriculum, grades, student_name, semester)
        
        return jsonify({"data": final_grades_summary}), 200

    except Exception as e:
        print(f"An unexpected error occurred: {e}") 
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500