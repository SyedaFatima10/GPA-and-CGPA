import streamlit as st
import pandas as pd

# ------------------------- #
# Streamlit Page Settings
# ------------------------- #
st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓", layout="wide")

# ------------------------- #
# Title Section
# ------------------------- #
st.title("🎓 GPA & CGPA Calculator till 4th Semester")
st.markdown("""
Welcome to the **4-Semester GPA & CGPA Calculator**!  
Enter your **marks (out of 100)** and **credit hours** for each course below.  
The app will automatically calculate **subject-wise GPA**, **semester GPAs**, and your **overall CGPA**.
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
    gpa_results = []
    total_weighted_points = 0
    total_credits = 0

    for sem_name, sem_data in semesters.items():
        # Add subject-wise GPA
        sem_data["Subject GPA"] = sem_data["Marks"].apply(marks_to_gpa)
        sem_data["Weighted Points"] = sem_data["Subject GPA"] * sem_data["Credit Hours"]

        sem_weighted = sem_data["Weighted Points"].sum()
        sem_credits = sem_data["Credit Hours"].sum()
        sem_gpa = sem_weighted / sem_credits if sem_credits > 0 else 0
        gpa_results.append({"Semester": sem_name, "GPA": round(sem_gpa, 2)})

        total_weighted_points += sem_weighted
        total_credits += sem_credits

        # Show subject-wise GPA table
        st.markdown(f"### 📚 {sem_name} Summary")
        st.dataframe(
            sem_data[["Course", "Marks", "Credit Hours", "Subject GPA"]],
            use_container_width=True
        )
        st.success(f"**GPA for {sem_name}: {round(sem_gpa, 2)}**")

    # Overall CGPA
    cgpa = total_weighted_points / total_credits if total_credits > 0 else 0

    # ------------------------- #
    # Display Results
    # ------------------------- #
    st.markdown("---")
    st.header("🎯 Final Results")

    st.success(f"📊 **Overall CGPA (1st–4th Semester): {cgpa:.2f}**")

    results_df = pd.DataFrame(gpa_results)
    st.write("📈 **Semester-wise GPA Summary:**")
    st.dataframe(results_df, use_container_width=True)

    st.line_chart(results_df.set_index("Semester")["GPA"], use_container_width=True)
