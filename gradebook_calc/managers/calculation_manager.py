# gradebook_calc/managers/calculation_manager.py

def calculate_final_grades(curriculum: dict, grades: list[dict]) -> list[dict]:
    """
    Calculates the final weighted grade for each student based on the curriculum.

    Args:
        curriculum: The parsed curriculum dictionary.
        grades: The parsed list of student grade entries.

    Returns:
        A list of dictionaries, each containing a student's ID, name, and final grade.
    """
    
    # 1. Create a quick lookup for category weights.
    category_weights = {item['category']: item['weight'] for item in curriculum['gradingPolicy']}
    
    # 2. Group all grade entries by student ID.
    student_grades = {}
    for grade_entry in grades:
        student_id = grade_entry.get('student_id')
        if not student_id:
            continue # Skip rows without a student ID

        if student_id not in student_grades:
            student_grades[student_id] = {
                'name': grade_entry.get('student_name', 'N/A'),
                'assignments': []
            }
        student_grades[student_id]['assignments'].append(grade_entry)

    # 3. Process each student's grades to calculate their final score.
    final_results = []
    for student_id, data in student_grades.items():
        # Group scores by category for this student
        scores_by_category = {cat: [] for cat in category_weights.keys()}
        
        for assignment in data['assignments']:
            assignment_name = assignment.get('assignment_name', '').lower()
            
            # Find which category this assignment belongs to
            found_category = None
            for category in category_weights.keys():
                if category.lower() in assignment_name:
                    found_category = category
                    break
            
            if found_category:
                try:
                    score = float(assignment['grade'])
                    scores_by_category[found_category].append(score)
                except (ValueError, TypeError):
                    # Ignore grades that are not valid numbers
                    print(f"Warning: Invalid grade '{assignment['grade']}' for student {student_id} on '{assignment_name}'. Skipping.")
                    continue

        # 4. Calculate the weighted average for the student
        final_score = 0.0
        for category, scores in scores_by_category.items():
            if scores: # Only calculate if there are grades for this category
                average_category_score = sum(scores) / len(scores)
                category_weight = category_weights[category] / 100.0
                final_score += average_category_score * category_weight
        
        final_results.append({
            'student_id': student_id,
            'student_name': data['name'],
            'final_grade': round(final_score, 2)
        })
        
    return final_results

