# gradebook_calc/routes.py

from flask import Blueprint, request, jsonify, render_template, session, current_app
import os

# Import the manager modules that contain the business logic.
from .managers import parsing_manager, calculation_manager

main_bp = Blueprint('main', __name__)

# def setup_dummy_data():
#     """Creates dummy data directories and files for the app to use."""
#     # Use the configuration from the current app context
#     curriculum_dir = current_app.config['CURRICULUM_DIR']
#     grades_dir = current_app.config['GRADES_DIR']
    
#     if not os.path.exists(curriculum_dir):
#         os.makedirs(curriculum_dir)
#     if not os.path.exists(grades_dir):
#         os.makedirs(grades_dir)
    
#     dummy_curriculum_path = os.path.join(curriculum_dir, 'engineering_curriculum_2025.csv')
#     if not os.path.exists(dummy_curriculum_path):
#         with open(dummy_curriculum_path, 'w', newline='') as f:
#             f.write("Semester,Teaching unit,Course,Credits\n")
#             f.write("1,Math,Calculus I,5\n")
#             f.write("2,Computer Science,Intro to Programming,4\n")
            
#     dummy_grades_path = os.path.join(grades_dir, 'fall_2025_grades.csv')
#     if not os.path.exists(dummy_grades_path):
#         with open(dummy_grades_path, 'w', newline='') as f:
#             f.write("student_id,student_name,assignment_name,grade\n")
#             f.write("101,Alice,Calculus I Midterm,88\n")
#             f.write("102,Bob,Calculus I Midterm,92\n")
#             f.write("101,Alice,Intro to Programming HW1,95\n")
#             f.write("102,Bob,Intro to Programming HW1,85\n")

# @main_bp.before_app_first_request
# def before_first_request():
#     """This function runs once before the first request to this blueprint."""
#     setup_dummy_data()


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
    """Loads a specific curriculum file by name."""
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
        return jsonify({"message": "Curriculum loaded successfully.", "summary": summary}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


@main_bp.route('/api/load/grades', methods=['POST'])
def load_grades_api():
    """Loads a specific grades file by name."""
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
        
        grades_data = parsing_manager.parse_grades(file_content)
        session['grades'] = grades_data
        
        summary = f"Loaded '{filename}' with {len(grades_data)} grade entries."
        return jsonify({"message": "Grades loaded successfully.", "summary": summary}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


@main_bp.route('/api/calculate', methods=['POST'])
def calculate_api():
    """API endpoint for calculating grades using data stored in the session."""
    try:
        if 'curriculum' not in session:
            return jsonify({"error": "Curriculum data has not been loaded."}), 400
        if 'grades' not in session:
            return jsonify({"error": "Student grades data has not been loaded."}), 400

        curriculum = session['curriculum']
        grades = session['grades']
        
        final_grades = calculation_manager.calculate_final_grades(curriculum, grades)
        
        session.clear()
        
        return jsonify({"data": final_grades}), 200

    except Exception as e:
        print(f"An unexpected error occurred: {e}") 
        return jsonify({"error": "An internal server error occurred."}), 500
