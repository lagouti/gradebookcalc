# gradebook_calc/managers/calculation_manager.py

from collections import defaultdict

def calculate_final_grades(curriculum_data, grades_data, student_name, semester):
    """
    Calculates a detailed, multi-format grade summary for a specific student and semester.
    
    The function returns a list of dictionaries formatted for display, including:
    - Individual courses with credits, percentage grade, and 20-point scale grade.
    - Grouping by Teaching Unit.
    - A summary row for each Teaching Unit with total credits and average grades.
    - A final summary row for the semester with total credits and overall average grades.
    """
    
    # 1. Filter curriculum for the selected semester and create a course lookup.
    courses_info = {}
    for course_row in curriculum_data:
        if course_row.get('Semester') == semester:
            try:
                courses_info[course_row['Course']] = {
                    'credits': int(course_row.get('Credits', 0)),
                    'unit': course_row.get('Teaching unit', 'N/A')
                }
            except (ValueError, KeyError):
                continue

    # 2. Filter grades for the selected student.
    student_grades_list = [g for g in grades_data if g.get('Student Name') == student_name]

    # 3. Group the student's grades by Teaching Unit.
    grades_by_unit = defaultdict(list)
    for grade_info in student_grades_list:
        course_name = grade_info.get('Course')
        if course_name in courses_info:
            teaching_unit = courses_info[course_name]['unit']
            grades_by_unit[teaching_unit].append(grade_info)

    # 4. Prepare the detailed summary list for display.
    final_summary_data = []
    overall_weighted_sum = 0.0
    overall_credit_sum = 0

    # Sort teaching units alphabetically for consistent order.
    for unit in sorted(grades_by_unit.keys()):
        unit_grades = grades_by_unit[unit]
        unit_weighted_grades = 0.0
        unit_total_credits = 0

        # Add rows for each course within the teaching unit.
        for grade_info in unit_grades:
            course_name = grade_info.get('Course')
            if course_name in courses_info:
                course_credits = courses_info[course_name]['credits']
                try:
                    grade_percent = float(grade_info.get('Grade', '0').strip('%'))
                except (ValueError, TypeError):
                    grade_percent = 0.0
                
                grade_20_scale = round((grade_percent / 100) * 20, 2)

                final_summary_data.append({
                    "Teaching Unit": unit,
                    "Course": course_name,
                    "Credits": course_credits,
                    "Grade (%)": f"{grade_percent:.2f}%",
                    "Grade (0-20)": f"{grade_20_scale:.2f}"
                })
                
                unit_weighted_grades += grade_percent * course_credits
                unit_total_credits += course_credits
        
        # Calculate and add the average row for the teaching unit.
        if unit_total_credits > 0:
            unit_average = unit_weighted_grades / unit_total_credits
            unit_average_20_scale = round((unit_average / 100) * 20, 2)
            final_summary_data.append({
                "Teaching Unit": f"<strong>{unit}</strong>",
                "Course": f"<strong>Unit Average</strong>",
                "Credits": f"<strong>{unit_total_credits}</strong>",
                "Grade (%)": f"<strong>{unit_average:.2f}%</strong>",
                "Grade (0-20)": f"<strong>{unit_average_20_scale:.2f}</strong>"
            })
            overall_weighted_sum += unit_weighted_grades
            overall_credit_sum += unit_total_credits

    # 5. Calculate and add the final overall semester average row.
    if overall_credit_sum > 0:
        final_overall_average = overall_weighted_sum / overall_credit_sum
        final_overall_average_20_scale = round((final_overall_average / 100) * 20, 2)
        final_summary_data.append({
            "Teaching Unit": "<strong>Overall</strong>",
            "Course": "<strong>Overall Semester Average</strong>",
            "Credits": f"<strong>{overall_credit_sum}</strong>",
            "Grade (%)": f"<strong>{final_overall_average:.2f}%</strong>",
            "Grade (0-20)": f"<strong>{final_overall_average_20_scale:.2f}</strong>"
        })
        
    return final_summary_data