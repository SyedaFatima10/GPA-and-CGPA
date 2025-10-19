# ================================================================
# 🎓 Streamlit App: GPA & CGPA Calculator for Statistics Program
# ================================================================

import streamlit as st
import pandas as pd

# -------------------------
# Streamlit Page Settings
# -------------------------
st.set_page_config(page_title="Statistics GPA & CGPA Calculator", page_icon="📊", layout="wide")

st.title("🎓 GPA & CGPA Calculator for Statistics Program")
st.write("Each semester has 6 courses — 2 Humanities (2 credits each) and 4 Major courses (3 credits each).")

# -------------------------
# Helper Function: Grade Conversion
# -------------------------
def grade_from_marks(marks):
    """Convert marks (0–100) to letter grade and grade points."""
    if marks >= 85:
        return "A+", 4.00
    elif marks >= 80:
        return "A", 3.70
    elif marks >= 75:
        return "B+", 3.30
    elif marks >= 70:
        return "B", 3.00
    elif marks >= 65:
        return "B-", 2.70
    elif marks >= 60:
        return "C+", 2.30
    elif marks >= 55:
        return "C", 2.00
    elif marks >= 50:
        return "D", 1.70
    else:
        return "F", 0.00

# -------------------------
# Predefined Courses by Semester
# -------------------------
semester_courses = {
    1: [
        ("ENG101", "Functional English (Humanities)", 2),
        ("ISL101", "Islamic Studies (Humanities)", 2),
        ("STAT101", "Introduction to Statistics", 3),
        ("STAT102", "Statistical Methods I", 3),
        ("MATH101", "Calculus I", 3),
        ("COMP101", "Computer Applications in Statistics", 3),
    ],
    2: [
        ("ENG102", "Communication Skills (Humanities)", 2),
        ("PAK101", "Pakistan Studies (Humanities)", 2),
        ("STAT201", "Probability & Distribution Theory", 3),
        ("STAT202", "Statistical Inference I", 3),
        ("MATH102", "Linear Algebra", 3),
        ("STAT203", "Applied Statistics I", 3),
    ],
    3: [
        ("ENG201", "Technical Writing (Humanities)", 2),
        ("ECO101", "Principles of Economics (Humanities)", 2),
        ("STAT301", "Regression Analysis", 3),
        ("STAT302", "Sampling Techniques", 3),
        ("STAT303", "Design of Experiments", 3),
        ("STAT304", "Time Series Analysis", 3),
    ],
    4: [
        ("PSY101", "Introduction to Psychology (Humanities)", 2),
        ("SOC101", "Sociology (Humanities)", 2),
        ("STAT401", "Multivariate Analysis", 3),
        ("STAT402", "Statistical Inference II", 3),
        ("STAT403", "Nonparametric Methods", 3),
        ("STAT404", "Applied Statistics II", 3),
    ]
}

# -------------------------
# Tabs for 4 Semesters
# -------------------------
tabs = st.tabs(["📘 Semester 1", "📗 Semester 2", "📙 Semester 3", "📕 Semester 4"])
semester_data = {}
semester_gpas = []

# -------------------------
# Input Marks and GPA per Semester
# -------------------------
for sem_index, tab in enumerate(tabs, start=1):
    with tab:
        st.header(f"Semester {sem_index} Courses")

        course_list = semester_courses[sem_index]
        course_data = []

        for code, title, credit in course_list:
            marks = st.number_input(f"{code} - {title} | Credit Hours: {credit}",
                                    min_value=0, max_value=100, key=f"marks_{sem_index}_{code}")
            grade, gp = grade_from_marks(marks)
            course_data.append({
                "Semester": sem_index,
                "Course Code": code,
                "Course Title": title,
                "Credit Hours": credit,
                "Marks": marks,
                "Letter Grade": grade,
                "Grade Points": gp
            })

        df = pd.DataFrame(course_data)
        semester_data[sem_index] = df

        # GPA Calculation
        df["Total Points"] = df["Credit Hours"] * df["Grade Points"]
        total_points = df["Total Points"].sum()
        total_credits = df["Credit Hours"].sum()
        gpa = round(total_points / total_credits, 2)
        semester_gpas.append(gpa)

        st.success(f"📊 GPA for Semester {sem_index}: **{gpa}**")
        st.dataframe(df[["Course Code", "Course Title", "Credit Hours", "Marks", "Letter Grade", "Grade Points"]],
                     use_container_width=True)

# -------------------------
# Dynamic CGPA Calculation
# -------------------------
st.divider()
st.header("🎯 Overall CGPA Calculation")

all_semesters = pd.concat(semester_data.values(), ignore_index=True)
if not all_semesters.empty:
    all_semesters["Total Points"] = all_semesters["Credit Hours"] * all_semesters["Grade Points"]
    total_points = all_semesters["Total Points"].sum()
    total_credits = all_semesters["Credit Hours"].sum()
    cgpa = round(total_points / total_credits, 2)

    st.success(f"🎓 **Overall CGPA till 4th Semester: {cgpa}**")

    gpa_summary = pd.DataFrame({
        "Semester": [1, 2, 3, 4],
        "GPA": semester_gpas
    })

    st.subheader("📈 GPA Summary by Semester")
    st.dataframe(gpa_summary, use_container_width=True)
    st.line_chart(gpa_summary.set_index("Semester"))

    st.subheader("📚 Full Course Details")
    st.dataframe(all_semesters[["Semester", "Course Code", "Course Title", "Credit Hours",
                                "Marks", "Letter Grade", "Grade Points"]],
                 use_container_width=True)
else:
    st.warning("Please enter marks for at least one semester to calculate CGPA.")
