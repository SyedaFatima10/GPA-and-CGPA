# ===============================
# 📘 Streamlit App: GPA & CGPA Calculator
# ===============================

import streamlit as st
import pandas as pd

# ===============================
# 🎯 App Title and Description
# ===============================
st.set_page_config(page_title="GPA & CGPA Calculator", layout="wide")
st.title("🎓 GPA and CGPA Calculator (Till 4th Semester)")
st.write("Upload your marks file to calculate your GPA and CGPA automatically.")

# ===============================
# 📂 File Upload Section
# ===============================
uploaded_file = st.file_uploader("Upload your Marks File (CSV or Excel)", type=["csv", "xlsx"])

# ===============================
# 📑 Instructions for the user
# ===============================
st.info("""
**File Format Example:**

| Semester | Course | Credit_Hours | Grade |
|-----------|---------|---------------|--------|
| 1 | Programming | 3 | A |
| 1 | Math | 3 | B+ |
| 2 | Physics | 4 | A- |
| 3 | Data Science | 3 | B |
| 4 | AI | 3 | A |

Grades accepted: A, A-, B+, B, B-, C+, C, C-, D+, D, F
""")

# ===============================
# 🧮 Grade to GPA Conversion Function
# ===============================
def grade_to_points(grade):
    grade_scale = {
        "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "F": 0.0
    }
    return grade_scale.get(grade.upper(), 0.0)

# ===============================
# 📊 Process Data if File Uploaded
# ===============================
if uploaded_file is not None:
    # Read file (detect CSV or Excel)
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Ensure proper column names
    df.columns = df.columns.str.strip().str.title()

    # Validate required columns
    required_columns = {"Semester", "Course", "Credit_Hours", "Grade"}
    if not required_columns.issubset(df.columns):
        st.error("❌ Missing required columns! Please include: Semester, Course, Credit_Hours, Grade")
    else:
        # Convert Grades to Points
        df["Grade_Points"] = df["Grade"].apply(grade_to_points)
        df["Quality_Points"] = df["Grade_Points"] * df["Credit_Hours"]

        # ===============================
        # 🧾 Separate Tabs for Each Section
        # ===============================
        tab1, tab2, tab3 = st.tabs(["📘 Semester GPA", "📈 Cumulative CGPA", "📄 Course Summary"])

        # ===============================
        # 📘 TAB 1: GPA per Semester
        # ===============================
        with tab1:
            st.subheader("📘 GPA per Semester")
            gpa_per_sem = (
                df.groupby("Semester")
                .apply(lambda x: round(x["Quality_Points"].sum() / x["Credit_Hours"].sum(), 2))
                .reset_index(name="GPA")
            )
            st.dataframe(gpa_per_sem, use_container_width=True)
            st.bar_chart(gpa_per_sem.set_index("Semester"))

        # ===============================
        # 📈 TAB 2: Cumulative CGPA till 4th Semester
        # ===============================
        with tab2:
            st.subheader("📈 CGPA Calculation (Till 4th Semester)")

            total_quality_points = df["Quality_Points"].sum()
            total_credit_hours = df["Credit_Hours"].sum()

            cgpa = round(total_quality_points / total_credit_hours, 2)

            st.metric(label="🎓 Cumulative CGPA", value=cgpa)

            # Optional line chart for GPA trend
            st.line_chart(gpa_per_sem.set_index("Semester"))

        # ===============================
        # 📄 TAB 3: Course Summary
        # ===============================
        with tab3:
            st.subheader("📄 Detailed Course Summary")
            st.dataframe(df, use_container_width=True)
            total_courses = df["Course"].nunique()
            total_credits = df["Credit_Hours"].sum()

            st.write(f"**Total Courses:** {total_courses}")
            st.write(f"**Total Credit Hours:** {total_credits}")
            st.write(f"**CGPA (again for reference):** {cgpa}")

else:
    st.warning("📤 Please upload your marks file to begin.")
