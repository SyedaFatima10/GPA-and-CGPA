import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓", layout="wide")

st.title("🎓 GPA & CGPA Calculator till 4th Semester")
st.markdown("""
Enter your **marks (out of 100)** and **credit hours**.  
This app calculates **subject-wise GPA**, **semester GPA**, **semester CGPA**, and **overall CGPA** in the same table.
""")

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

def semester_input(sem_num):
    st.subheader(f"📘 Semester {sem_num}")
    data = [{"Course": f"Course {i}", "Marks": 0.0, "Credit Hours": 3.0} for i in range(1, 7)]
    df = pd.DataFrame(data)
    
    edited_df = st.data_editor(df, use_container_width=True, num_rows="fixed", hide_index=True, key=f"sem_{sem_num}")
    edited_df["Subject GPA"] = edited_df["Marks"].apply(marks_to_gpa)
    return edited_df

# Collect semester data
semesters = {f"Semester {i}": semester_input(i) for i in range(1, 5)}

# GPA & CGPA Calculation
if st.button("🚀 Calculate GPA and CGPA"):
    cumulative_points = 0
    cumulative_credits = 0

    for sem_name, sem_data in semesters.items():
        sem_data["Weighted Points"] = sem_data["Subject GPA"] * sem_data["Credit Hours"]

        sem_weighted = sem_data["Weighted Points"].sum()
        sem_credits = sem_data["Credit Hours"].sum()
        sem_gpa = sem_weighted / sem_credits if sem_credits > 0 else 0

        cumulative_points += sem_weighted
        cumulative_credits += sem_credits
        sem_cgpa = cumulative_points / cumulative_credits if cumulative_credits > 0 else 0

        # Add extra rows as consistent types
        extra_rows = pd.DataFrame({
            "Course": ["Semester GPA", "Semester CGPA"],
            "Marks": [None, None],
            "Credit Hours": [None, None],
            "Subject GPA": [round(sem_gpa,2), round(sem_cgpa,2)]
        })

        display_df = pd.concat([sem_data, extra_rows], ignore_index=True)
        st.markdown(f"### 📚 {sem_name} Summary")
        st.dataframe(display_df, use_container_width=True)

    overall_cgpa = cumulative_points / cumulative_credits if cumulative_credits > 0 else 0
    st.success(f"📊 **Overall CGPA (1st–4th Semester): {overall_cgpa:.2f}**")
