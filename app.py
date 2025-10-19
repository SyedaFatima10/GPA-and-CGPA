import streamlit as st
import pandas as pd

# ------------------------------- #
# App Title and Description
# ------------------------------- #
st.set_page_config(page_title="Statistics GPA & CGPA Calculator", page_icon="📊", layout="wide")
st.title("🎓 Statistics GPA & CGPA Calculator (4 Semesters, 6 Courses Each)")

st.markdown("""
Welcome to the **Statistics GPA & CGPA Calculator!**  
Each semester includes **6 courses** — with **Major courses (3 credit hours)** and **Humanities courses (2 credit hours)**.  
Enter your marks (0–100) for each course, then click **Calculate GPA and CGPA**.
""")

# ------------------------------- #
# Grade Conversion Function
# ------------------------------- #
def marks_to_gpa(marks):
    if marks >= 85:
        return 4.00
    elif marks >= 80:
        return 3.70
    elif marks >= 75:
        return 3.30
    elif marks >= 70:
        return 3.00
    elif marks >= 65:
        return 2.70
    elif marks >= 61:
        return 2.30
    elif marks >= 58:
        return 2.00
    elif marks >= 55:
        return 1.70
    elif marks >= 50:
        return 1.00
    else:
        return 0.00

# ------------------------------- #
# Semester Courses Data
# ------------------------------- #
semester_courses = {
    "Semester 1": [
        ("Introduction to Statistics", 3),
        ("Calculus I", 3),
        ("Computer Applications in Statistics", 3),
        ("English Composition", 2),
        ("Pakistan Studies", 2),
        ("Islamic Studies", 2)
    ],
    "Semester 2": [
        ("Probability & Distributions", 3),
        ("Calculus II", 3),
        ("Statistical Inference I", 3),
        ("Communication Skills", 2),
        ("Microeconomics", 2),
        ("Sociology", 2)
    ],
    "Semester 3": [
        ("Regression Analysis", 3),
        ("Design of Experiments", 3),
        ("Statistical Inference II", 3),
        ("Macroeconomics", 2),
        ("Environmental Studies", 2),
        ("Ethics", 2)
    ],
    "Semester 4": [
        ("Sampling Techniques", 3),
        ("Applied Multivariate Analysis", 3),
        ("Non-Parametric Methods", 3),
        ("Research Methodology", 2),
        ("Linear Algebra", 3),
        ("Psychology", 2)
    ]
}

# ------------------------------- #
# Function: Input for a Semester
# ------------------------------- #
def semester_input(sem_name, courses):
    st.subheader(f"📘 {sem_name}")
    data = []
    for course, credit in courses:
        data.append({"Course": course, "Credit Hours": credit, "Marks": 0.0})
    df = pd.DataFrame(data)
    edited_df = st.data_editor(df, use_container_width=True, num_rows="fixed", hide_index=True, key=sem_name)
    return edited_df

# ------------------------------- #
# Input: All Four Semesters
# ------------------------------- #
semesters = {}
for sem, courses in semester_courses.items():
    semesters[sem] = semester_input(sem, courses)

# ------------------------------- #
# GPA & CGPA Calculation
# ------------------------------- #
if st.button("📊 Calculate GPA and CGPA"):
    gpa_results = []
    total_points, total_credits = 0, 0

    for sem_name, sem_data in semesters.items():
        sem_data["GPA Points"] = sem_data["Marks"].apply(marks_to_gpa)
        sem_data["Weighted Points"] = sem_data["GPA Points"] * sem_data["Credit Hours"]

        sem_gpa = sem_data["Weighted Points"].sum() / sem_data["Credit Hours"].sum()
        gpa_results.append({"Semester": sem_name, "GPA": round(sem_gpa, 2)})

        total_points += sem_data["Weighted Points"].sum()
        total_credits += sem_data["Credit Hours"].sum()

    cgpa = total_points / total_credits if total_credits > 0 else 0

    # ------------------------------- #
    # Display Results
    # ------------------------------- #
    st.success(f"🎯 **Cumulative CGPA (After 4 Semesters): {cgpa:.2f}**")

    results_df = pd.DataFrame(gpa_results)
    st.write("📈 **Semester-wise GPA Summary:**")
    st.dataframe(results_df, use_container_width=True)

    st.line_chart(results_df.set_index("Semester")["GPA"], use_container_width=True)
