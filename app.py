import streamlit as st
import pandas as pd

st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓", layout="wide")

st.title("🎓 GPA & CGPA Calculator (Up to 4th Semester)")
# Grade Conversion Functions
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

def gpa_to_grade(gpa):
    if gpa == 4.00:
        return "A+"
    elif gpa >= 3.70:
        return "A"
    elif gpa >= 3.30:
        return "A-"
    elif gpa >= 3.00:
        return "B+"
    elif gpa >= 2.70:
        return "B"
    elif gpa >= 2.30:
        return "B-"
    elif gpa >= 2.00:
        return "C+"
    elif gpa >= 1.70:
        return "C"
    elif gpa >= 1.00:
        return "D"
    else:
        return "F"
# Semester Input Function
def semester_input(sem_num):
    st.subheader(f"📘 Semester {sem_num}")
    data = [{"Course": f"Course {i}", "Marks": 0.0, "Credit Hours": 3.0} for i in range(1, 7)]
    df = pd.DataFrame(data)
    
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        hide_index=True,
        key=f"sem_{sem_num}"
    )
    
    return edited_df
# Collect Semester Data
semesters = {f"Semester {i}": semester_input(i) for i in range(1, 5)}
# GPA & CGPA Calculation

if st.button("🚀 Calculate GPA and CGPA"):
    cumulative_points = 0
    cumulative_credits = 0
    semester_gpas = []

    for sem_name, sem_data in semesters.items():
        # Subject-wise GPA and Grade
        sem_data["Subject GPA"] = sem_data["Marks"].apply(marks_to_gpa)
        sem_data["Grade"] = sem_data["Subject GPA"].apply(gpa_to_grade)
        sem_data["Weighted Points"] = sem_data["Subject GPA"] * sem_data["Credit Hours"]

        # Semester GPA
        sem_weighted = sem_data["Weighted Points"].sum()
        sem_credits = sem_data["Credit Hours"].sum()
        sem_gpa = sem_weighted / sem_credits if sem_credits > 0 else 0

        # Cumulative CGPA
        cumulative_points += sem_weighted
        cumulative_credits += sem_credits
        sem_cgpa = cumulative_points / cumulative_credits if cumulative_credits > 0 else 0

        # Display results with Grade first
        st.markdown(f"### 📚 {sem_name} Results")
        st.dataframe(
            sem_data[["Course", "Marks", "Credit Hours", "Grade", "Subject GPA"]],
            use_container_width=True
        )
        st.success(f"**GPA for {sem_name}: {round(sem_gpa,2)} | Semester CGPA: {round(sem_cgpa,2)}**")

        semester_gpas.append((sem_name, round(sem_gpa, 2)))

    # Overall CGPA
    overall_cgpa = cumulative_points / cumulative_credits if cumulative_credits > 0 else 0
    overall_grade = gpa_to_grade(overall_cgpa)
    st.markdown("---")
    st.success(f"📊 **Overall CGPA (1st–4th Semester): {overall_cgpa:.2f} | Grade: {overall_grade}**")

    # Line chart for semester GPAs
    chart_df = pd.DataFrame(semester_gpas, columns=["Semester", "GPA"]).set_index("Semester")
    st.line_chart(chart_df, use_container_width=True)
