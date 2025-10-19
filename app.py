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
The app will automatically calculate **subject-wise GPA**, **semester GPA**, **semester CGPA**, and your **overall CGPA** in the same table.
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
    data = [{"Course": f"Course {i}", "Marks": 0.0, "Credit Hours": 3.0, "Subject GPA": 0.0} for i in range(1, 7)]
    df = pd.DataFrame(data)
    
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        hide_index=True,
        key=f"sem_{sem_num}"
    )
    
    # Automatically calculate Subject GPA
    edited_df["Subject GPA"] = edited_df["Marks"].apply(marks_to_gpa)
    
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

    for sem_idx, (sem_name, sem_data) in enumerate(semesters.items(), start=1):
        # Weighted points
        sem_data["Weighted Points"] = sem_data["Subject GPA"] * sem_data["Credit Hours"]

        # Semester GPA
        sem_weighted = sem_data["Weighted Points"].sum()
        sem_credits = sem_data["Credit Hours"].sum()
        sem_gpa = sem_weighted / sem_credits if sem_credits > 0 else 0

        # Cumulative CGPA
        cumulative_points += sem_weighted
        cumulative_credits += sem_credits
        sem_cgpa = cumulative_points / cumulative_credits if cumulative_credits > 0 else 0

        # Add semester GPA, CGPA, and overall CGPA to bottom of table
        summary_row = pd.DataFrame({
            "Course": ["---"],
            "Marks": ["---"],
            "Credit Hours": ["---"],
            "Subject GPA": ["---"],
            "Weighted Points": ["---"],
        })
        sem_data = pd.concat([sem_data, summary_row], ignore_index=True)
        sem_data.loc[sem_data.index[-1], "Course"] = f"Semester GPA: {round(sem_gpa,2)}, Semester CGPA: {round(sem_cgpa,2)}, Overall CGPA: {round(cumulative_points/cumulative_credits,2)}"

        # Display the table
        st.markdown(f"### 📚 {sem_name} Summary")
        st.dataframe(sem_data, use_container_width=True)
