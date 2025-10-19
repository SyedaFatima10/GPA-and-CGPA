# =============================================
# 🎓 Streamlit App: GPA & CGPA Calculator (1st–4th Semester)
# =============================================

import streamlit as st
import pandas as pd

# -------------------------
# Streamlit Page Settings
# -------------------------
st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓", layout="wide")

st.title("🎓 GPA & CGPA Calculator (1st – 4th Semester)")
st.write("Enter your course details for each semester to calculate your GPA and overall CGPA.")

# -------------------------
# Helper Function: Grade Conversion
# -------------------------
def grade_from_marks(marks):
    if marks >= 85:
        return "A+", 4.00
    elif marks >= 80:
        return "A-", 3.66
    elif marks >= 75:
        return "B+", 3.33
    elif marks >= 70:
        return "B", 3.00
    elif marks >= 65:
        return "B-", 2.66
    elif marks >= 60:
        return "C+", 2.33
    elif marks >= 55:
        return "C", 2.00
    elif marks >= 50:
        return "D", 1.66
    else:
        return "F", 0.00

# -------------------------
# Tabs for Semesters
# -------------------------
tabs = st.tabs(["📘 Semester 1", "📗 Semester 2", "📙 Semester 3", "📕 Semester 4"])
semester_data = {}
semester_gpas = []

# -------------------------
# Loop for each semester
# -------------------------
for sem_index, tab in enumerate(tabs, start=1):
    with tab:
        st.header(f"Semester {sem_index} Details")

        n = st.number_input(f"How many courses did you take in Semester {sem_index}?",
                            min_value=1, max_value=10, value=6, key=f"num_{sem_index}")

        course_data = []
        for i in range(1, n + 1):
            st.subheader(f"Course {i}")
            course_code = st.text_input(f"Course Code (e.g., CSC{sem_index}0{i})", key=f"code_{sem_index}_{i}")
            course_name = st.text_input(f"Course Title", key=f"name_{sem_index}_{i}")
            credit = st.number_input(f"Credit Hours", min_value=1, max_value=4, key=f"credit_{sem_index}_{i}")
            marks = st.number_input(f"Marks (0–100)", min_value=0, max_value=100, key=f"marks_{sem_index}_{i}")

            grade, gp = grade_from_marks(marks)
            course_data.append({
                "Semester": sem_index,
                "Course No": course_code,
                "Course Title": course_name,
                "Credit": credit,
                "Marks": marks,
                "L.G.": grade,
                "G.P.": gp
            })

        df = pd.DataFrame(course_data)
        semester_data[sem_index] = df

        if st.button(f"Calculate GPA (Semester {sem_index})", key=f"calc_{sem_index}"):
            if not df.empty:
                df["Total Points"] = df["Credit"] * df["G.P."]
                total_credits = df["Credit"].sum()
                total_points = df["Total Points"].sum()
                gpa = round(total_points / total_credits, 2)
                semester_gpas.append((sem_index, gpa))
                st.success(f"📊 GPA for Semester {sem_index}: {gpa}")
                st.dataframe(df[["Course No", "Course Title", "Credit", "Marks", "L.G.", "G.P."]],
                             use_container_width=True)
            else:
                st.warning("Please fill in your course details first!")

# -------------------------
# Final CGPA Calculation
# -------------------------
if st.button("🎯 Calculate Overall CGPA"):
    all_semesters = pd.concat(semester_data.values(), ignore_index=True)
    if not all_semesters.empty:
        all_semesters["Total Points"] = all_semesters["Credit"] * all_semesters["G.P."]
        total_points = all_semesters["Total Points"].sum()
        total_credits = all_semesters["Credit"].sum()
        cgpa = round(total_points / total_credits, 2)

        # GPA per semester
        gpa_summary = (
            all_semesters.groupby("Semester")
            .apply(lambda x: round((x["Total Points"].sum() / x["Credit"].sum()), 2))
            .reset_index(name="GPA")
        )

        st.success(f"🎓 **Overall CGPA till 4th Semester: {cgpa}**")

        st.write("### 📊 GPA per Semester")
        st.dataframe(gpa_summary, use_container_width=True)

        st.write("### 📚 Complete Course Summary")
        st.dataframe(all_semesters[["Semester", "Course No", "Course Title", "Credit", "Marks", "L.G.", "G.P."]],
                     use_container_width=True)
    else:
        st.warning("Please enter data for at least one semester!")
