import streamlit as st
import pandas as pd

# ------------------------- #
# Streamlit Page Settings
# ------------------------- #
st.set_page_config(
    page_title="GPA & CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# ------------------------- #
# Title Section
# ------------------------- #
st.title("🎓 GPA & CGPA Calculator (Up to 4th Semester)")
st.markdown("""
Welcome! Enter your **marks (out of 100)** and **credit hours** for each course.  
The app calculates **subject-wise GPA**, **semester GPA**, **semester CGPA**, and **overall CGPA** automatically.
""")

# ------------------------- #
# Grade Conversion Function
# ------------------------- #
def marks_to_gpa(marks):
    if marks >= 85: return 4.00
    elif marks >= 80: return 3.70
    elif marks >= 75: return 3.30
    elif marks >= 70: return 3.00
    elif marks >= 65: return 2.70
    elif marks >= 61: return 2.30
    elif marks >= 58: return 2.00
    elif marks >= 55: return 1.70
    elif marks >= 50: return 1.00
    else: return 0.00

# ------------------------- #
# Semester Input Function
# ------------------------- #
def semester_input(sem_num):
    st.subheader(f"📘 Semester {sem_num}")
    # Initial table with 6 courses
    df = pd.DataFrame({
        "Course": [f"Course {i}" for i in range(1, 7)],
        "Marks": [0.0]*6,
        "Credit Hours": [3.0]*6,
        "Subject GPA": [0.0]*6
    })
    
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        hide_index=True,
        key=f"sem_{sem_num}"
    )
    
    # Calculate Subject GPA
    edited_df["Subject GPA"] = edited_df["Marks"].apply(marks_to_gpa)
    return edited_df

# ------------------------- #
# Collect Data for 4 Semesters
# ------------------------- #
semesters = {f"Semester {i}": semester_input(i) for i in range(1, 5)}

# ------------------------- #
# GPA & CGPA Calculation
# ------------------------- #
if st.button("🚀 Calculate GPA and CGPA"):
    cumulative_points = 0
    cumulative_credits = 0
    semester_summary = []

    for sem_name, sem_data in semesters.items():
        sem_data["Weighted Points"] = sem_data["Subject GPA"] * sem_data["Credit Hours"]
        sem_gpa = sem_data["Weighted Points"].sum() / sem_data["Credit Hours"].sum()
        
        cumulative_points += sem_data["Weighted Points"].sum()
        cumulative_credits += sem_data["Credit Hours"].sum()
        sem_cgpa = cumulative_points / cumulative_credits
        
        # Save semester summary
        semester_summary.append({
            "Semester": sem_name,
            "Semester GPA": round(sem_gpa, 2),
            "Semester CGPA": round(sem_cgpa, 2)
        })
        
        # Show table with subject GPA
        st.markdown(f"### 📚 {sem_name} Details")
        st.dataframe(sem_data[["Course", "Marks", "Credit Hours", "Subject GPA"]], use_container_width=True)
        st.success(f"GPA: {sem_gpa:.2f} | Semester CGPA: {sem_cgpa:.2f}")

    # Overall CGPA
    overall_cgpa = cumulative_points / cumulative_credits

    st.markdown("---")
    st.header("🎯 Final Results")
    results_df = pd.DataFrame(semester_summary)
    st.dataframe(results_df, use_container_width=True)
    st.success(f"📊 **Overall CGPA (1st–4th Semester): {overall_cgpa:.2f}**")
    st.line_chart(results_df.set_index("Semester")["Semester GPA"], use_container_width=True)
