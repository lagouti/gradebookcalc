# gradebook_calc/managers/calculation_manager.py

# from collections import defaultdict

# def calculate_final_grades(curriculum_data, grades_data, student_name, semester):
#     """
#     Calculates a detailed, multi-format grade summary for a specific student and semester.
    
#     The function returns a list of dictionaries formatted for display, including:
#     - Individual courses with credits, percentage grade, and 20-point scale grade.
#     - Grouping by Teaching Unit.
#     - A summary row for each Teaching Unit with total credits and average grades.
#     - A final summary row for the semester with total credits and overall average grades.
#     """
    
#     # 1. Filter curriculum for the selected semester and create a course lookup.
#     courses_info = {}
#     for course_row in curriculum_data:
#         if course_row.get('Semester') == semester:
#             try:
#                 courses_info[course_row['Course']] = {
#                     'credits': int(course_row.get('Credits', 0)),
#                     'unit': course_row.get('Teaching unit', 'N/A')
#                 }
#             except (ValueError, KeyError):
#                 continue

#     # 2. Filter grades for the selected student.
#     student_grades_list = [g for g in grades_data if g.get('Student Name') == student_name]

#     # 3. Group the student's grades by Teaching Unit.
#     grades_by_unit = defaultdict(list)
#     for grade_info in student_grades_list:
#         course_name = grade_info.get('Course')
#         if course_name in courses_info:
#             teaching_unit = courses_info[course_name]['unit']
#             grades_by_unit[teaching_unit].append(grade_info)

#     # 4. Prepare the detailed summary list for display.
#     final_summary_data = []
#     overall_weighted_sum = 0.0
#     overall_credit_sum = 0

#     # Sort teaching units alphabetically for consistent order.
#     for unit in sorted(grades_by_unit.keys()):
#         unit_grades = grades_by_unit[unit]
#         unit_weighted_grades = 0.0
#         unit_total_credits = 0

#         # Add rows for each course within the teaching unit.
#         for grade_info in unit_grades:
#             course_name = grade_info.get('Course')
#             if course_name in courses_info:
#                 course_credits = courses_info[course_name]['credits']
#                 try:
#                     grade_percent = float(grade_info.get('Grade', '0').strip('%'))
#                 except (ValueError, TypeError):
#                     grade_percent = 0.0
                
#                 grade_20_scale = round((grade_percent / 100) * 20, 2)

#                 final_summary_data.append({
#                     "Teaching Unit": unit,
#                     "Course": course_name,
#                     "Credits": course_credits,
#                     "Grade (%)": f"{grade_percent:.2f}%",
#                     "Grade (0-20)": f"{grade_20_scale:.2f}"
#                 })
                
#                 unit_weighted_grades += grade_percent * course_credits
#                 unit_total_credits += course_credits
        
#         # Calculate and add the average row for the teaching unit.
#         if unit_total_credits > 0:
#             unit_average = unit_weighted_grades / unit_total_credits
#             unit_average_20_scale = round((unit_average / 100) * 20, 2)
#             final_summary_data.append({
#                 "Teaching Unit": f"<strong>{unit}</strong>",
#                 "Course": f"<strong>Unit Average</strong>",
#                 "Credits": f"<strong>{unit_total_credits}</strong>",
#                 "Grade (%)": f"<strong>{unit_average:.2f}%</strong>",
#                 "Grade (0-20)": f"<strong>{unit_average_20_scale:.2f}</strong>"
#             })
#             overall_weighted_sum += unit_weighted_grades
#             overall_credit_sum += unit_total_credits

#     # 5. Calculate and add the final overall semester average row.
#     if overall_credit_sum > 0:
#         final_overall_average = overall_weighted_sum / overall_credit_sum
#         final_overall_average_20_scale = round((final_overall_average / 100) * 20, 2)
#         final_summary_data.append({
#             "Teaching Unit": "<strong>Overall</strong>",
#             "Course": "<strong>Overall Semester Average</strong>",
#             "Credits": f"<strong>{overall_credit_sum}</strong>",
#             "Grade (%)": f"<strong>{final_overall_average:.2f}%</strong>",
#             "Grade (0-20)": f"<strong>{final_overall_average_20_scale:.2f}</strong>"
#         })
        
#     return final_summary_data
# gradebook_calc/managers/calculation_manager.py

# from collections import defaultdict

# def calculate_final_grades(curriculum_data, grades_data, student_name, semester):
#     """
#     Calculates a detailed, multi-format grade summary for a specific student and semester.
    
#     This function has been rewritten to ensure correct aggregation and calculation by:
#     1.  First, aggregating all grade and credit data for the student.
#     2.  Then, building a structured summary list from the aggregated data.
#     This corrects a flaw in the previous version that caused incorrect calculations for
#     teaching units with more than two courses.
#     """
    
#     # 1. Filter curriculum for the selected semester and create a course lookup.
#     courses_info = {}
#     for course_row in curriculum_data:
#         if course_row.get('Semester') == semester:
#             try:
#                 courses_info[course_row['Course']] = {
#                     'credits': int(course_row.get('Credits', 0)),
#                     'unit': course_row.get('Teaching unit', 'N/A')
#                 }
#             except (ValueError, KeyError):
#                 continue

#     # 2. Filter grades for the selected student.
#     student_grades_list = [g for g in grades_data if g.get('Student Name') == student_name]

#     # 3. Aggregate all course data for the student, grouped by teaching unit.
#     unit_calculations = defaultdict(lambda: {
#         'courses': [],
#         'total_weighted_grades': 0.0,
#         'total_credits': 0
#     })

#     for grade_info in student_grades_list:
#         course_name = grade_info.get('Course')
#         if course_name in courses_info:
#             details = courses_info[course_name]
#             unit = details['unit']
#             credits = details['credits']
            
#             try:
#                 grade_percent = float(grade_info.get('Grade', '0').strip('%'))
#             except (ValueError, TypeError):
#                 grade_percent = 0.0

#             # Store individual course data and update running totals for the unit.
#             unit_calculations[unit]['courses'].append({
#                 'name': course_name,
#                 'credits': credits,
#                 'grade_percent': grade_percent
#             })
#             unit_calculations[unit]['total_weighted_grades'] += grade_percent * credits
#             unit_calculations[unit]['total_credits'] += credits

#     # 4. Build the final, structured summary list from the aggregated data.
#     final_summary_data = []
#     overall_weighted_sum = 0.0
#     overall_credit_sum = 0

#     for unit in sorted(unit_calculations.keys()):
#         calc_data = unit_calculations[unit]
        
#         # Add a row for each individual course in the unit.
#         for course in sorted(calc_data['courses'], key=lambda x: x['name']):
#             grade_20_scale = round((course['grade_percent'] / 100) * 20, 2)
#             final_summary_data.append({
#                 "Teaching Unit": unit,
#                 "Course": course['name'],
#                 "Credits": course['credits'],
#                 "Grade (%)": f"{course['grade_percent']:.2f}%",
#                 "Grade (0-20)": f"{grade_20_scale:.2f}"
#             })
        
#         # Calculate and add the summary row for the teaching unit.
#         unit_credits = calc_data['total_credits']
#         if unit_credits > 0:
#             unit_average = calc_data['total_weighted_grades'] / unit_credits
#             unit_average_20_scale = round((unit_average / 100) * 20, 2)
#             final_summary_data.append({
#                 "Teaching Unit": f"<strong>{unit}</strong>",
#                 "Course": f"<strong>Unit Average</strong>",
#                 "Credits": f"<strong>{unit_credits}</strong>",
#                 "Grade (%)": f"<strong>{unit_average:.2f}%</strong>",
#                 "Grade (0-20)": f"<strong>{unit_average_20_scale:.2f}</strong>"
#             })
#             overall_weighted_sum += calc_data['total_weighted_grades']
#             overall_credit_sum += unit_credits

#     # 5. Calculate and add the final overall semester average row.
#     if overall_credit_sum > 0:
#         final_overall_average = overall_weighted_sum / overall_credit_sum
#         final_overall_average_20_scale = round((final_overall_average / 100) * 20, 2)
#         final_summary_data.append({
#             "Teaching Unit": "<strong>Overall</strong>",
#             "Course": "<strong>Overall Semester Average</strong>",
#             "Credits": f"<strong>{overall_credit_sum}</strong>",
#             "Grade (%)": f"<strong>{final_overall_average:.2f}%</strong>",
#             "Grade (0-20)": f"<strong>{final_overall_average_20_scale:.2f}</strong>"
#         })
        
#     return final_summary_data

# gradebook_calc/managers/calculation_manager.py

from collections import defaultdict

def calculate_final_grades(curriculum_data, grades_data, student_name, semester):
    """
    Calculates a detailed, multi-format grade summary for a specific student and semester.
    
    This function has been completely rewritten with a more robust, multi-pass approach 
    to fix a persistent bug related to incorrect calculations for teaching units with
    more than two courses.
    """
    
    # 1. Create a course lookup from the curriculum for the selected semester.
    courses_info = {}
    # for course_row in curriculum_data:
    for i, course_row in enumerate(curriculum_data):    
        if course_row.get('Semester') == semester:
            try:
                courses_info[course_row['Course']] = {
                    'credits': float(course_row.get('Credits', 0)),
                    'unit': course_row.get('Teaching unit', 'N/A')
                }
            except (ValueError, KeyError) as e:
                # Print the error type, the row number, and the problematic data
                print(f"⚠️ Error processing row {i+1}: {e}")
                print(f"   Problematic Row Data: {course_row}")
                continue

    print(f"Courses info for semester '{semester}': {courses_info}")

    # 2. Create a flat list of all relevant grade records for the selected student.
    # Each record is enriched with curriculum data.
    enriched_grades = []
    for grade_info in grades_data:
        is_correct_student = grade_info.get('Student Name') == student_name
        course_name = grade_info.get('Course')
        
        if is_correct_student and course_name in courses_info:
            details = courses_info[course_name]
            try:
                grade_percent = float(grade_info.get('Grade', '0').strip('%'))
            except (ValueError, TypeError):
                grade_percent = 0.0

            enriched_grades.append({
                'unit': details['unit'],
                'course_name': course_name,
                'credits': details['credits'],
                'grade_percent': grade_percent
            })

    # 3. Group the enriched grades by teaching unit.
    grades_by_unit = defaultdict(list)
    for grade in enriched_grades:
        grades_by_unit[grade['unit']].append(grade)

    # 4. Build the final summary table from the grouped data.
    final_summary_data = []
    overall_weighted_sum = 0.0
    overall_credit_sum = 0

    for unit in sorted(grades_by_unit.keys()):
        unit_courses = grades_by_unit[unit]
        unit_weighted_grades = 0.0
        unit_total_credits = 0

        # Add rows for each individual course within the teaching unit.
        for course in sorted(unit_courses, key=lambda x: x['course_name']):
            grade_20_scale = round((course['grade_percent'] / 100) * 20, 2)
            final_summary_data.append({
                "Teaching Unit": unit,
                "Course": course['course_name'],
                "Credits": course['credits'],
                "Grade (%)": f"{course['grade_percent']:.2f}%",
                "Grade (0-20)": f"{grade_20_scale:.2f}"
            })
            unit_weighted_grades += course['grade_percent'] * course['credits']
            unit_total_credits += course['credits']
        
        # Calculate and add the summary row for the teaching unit.
        if unit_total_credits > 0:
            unit_average = unit_weighted_grades / unit_total_credits
            unit_average_20_scale = round((unit_average / 100) * 20, 2)
            final_summary_data.append({
                "Teaching Unit": f"<strong>{unit}</strong>",
                "Course": "<strong>Unit Average</strong>",
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