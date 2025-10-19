import streamlit as st
import pandas as pd

# ------------------------- #
# Streamlit Page Settings
# ------------------------- #
st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓", layout="wide")

# ------------------------- #
# Title Section
# ------------------------- #
st.title("🎓 GPA & CGPA Calculator (Up to 4th Semester)")
st.markdown("""
Welcome to the **4-Semester GPA & CGPA Calculator**!  
Enter your **marks (out of 100)** and **credit hours** for each course below.  
The app will automatically calculate **subject-wise GPA**, **semester GPA**, **semester CGPA**, and your **overall CGPA**.
""")

# ------------------------- #
# Grade Conversion Function
# ------------------------- #
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

# ------------------------- #
# Semester Input Function
# ------------------------- #
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

# ------------------------- #
# Collect Semester Data
# ------------------------- #
semesters = {f"Semester {i}": semester_input(i) for i in range(1, 5)}

# ------------------------- #
# GPA & CGPA Calculation
# ------------------------- #
if st.button("🚀 Calculate GPA and CGPA"):
    cumulative_points = 0
    cumulative_credits = 0
    semester_gpas = []

    for sem_name, sem_data in semesters.items():
        # Calculate subject-wise GPA (used internally)
        sem_data["Subject GPA"] = sem_data["Marks"].apply(marks_to_gpa)
        sem_data["Weighted Points"] = sem_data["Subject GPA"] * sem_data["Credit Hours"]

        # Semester GPA
        sem_weighted = sem_data["Weighted Points"].sum()
        sem_credits = sem_data["Credit Hours"].sum()
        sem_gpa = sem_weighted / sem_credits if sem_credits > 0 else 0

        # Cumulative CGPA
        cumulative_points += sem_weighted
        cumulative_credits += sem_credits
        sem_cgpa = cumulative_points / cumulative_credits if cumulative_credits > 0 else 0

        # Save semester GPA for line chart
        semester_gpas.append((sem_name, round(sem_gpa, 2)))

        st.success(f"**GPA for {sem_name}: {round(sem_gpa,2)} | Semester CGPA: {round(sem_cgpa,2)}**")

    # Overall CGPA
    overall_cgpa = cumulative_points / cumulative_credits if cumulative_credits > 0 else 0
    st.markdown("---")
    st.success(f"📊 **Overall CGPA (1st–4th Semester): {overall_cgpa:.2f}**")

    # Optional: Line chart for semester GPAs
    chart_df = pd.DataFrame(semester_gpas, columns=["Semester", "GPA"]).set_index("Semester")
    st.line_chart(chart_df, use_container_width=True)
