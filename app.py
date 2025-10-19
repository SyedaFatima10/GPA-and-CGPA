import streamlit as st
import pandas as pd

# ------------------------- #
# Streamlit Page Settings
# ------------------------- #
st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓", layout="centered")

st.title("🎓 GPA & CGPA Calculator (1st Semester)")
st.write("Enter your first semester course details below to calculate your GPA and CGPA.")

# ------------------------- #
# Helper Function: Grade Conversion
# ------------------------- #
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


# ------------------------- #
# Tabs
# ------------------------- #
tab1, tab2 = st.tabs(["📘 GPA & CGPA Calculator", "📚 Courses Entered"])

# ------------------------- #
# Tab 1: GPA / CGPA Calculation
# ------------------------- #
with tab1:
    st.header("Enter Course Details")

    n = st.number_input("How many courses did you take in 1st semester?", min_value=1, max_value=10, value=6)

    course_data = []

    for i in range(1, n + 1):
        st.subheader(f"Course {i}")
        course_code = st.text_input(f"Course Code (e.g., CSC101)", key=f"code_{i}")
        course_name = st.text_input(f"Course Title", key=f"name_{i}")
        credit = st.number_input(f"Credit Hours", min_value=1, max_value=4, key=f"credit_{i}")
        marks = st.number_input(f"Marks (0–100)", min_value=0, max_value=100, key=f"marks_{i}")

        grade, gp = grade_from_marks(marks)
        course_data.append({
            "Course No": course_code,
            "Course Title": course_name,
            "Credit": credit,
            "Marks": marks,
            "L.G.": grade,
            "G.P.": gp
        })

    df = pd.DataFrame(course_data)

    if st.button("Calculate GPA & CGPA"):
        if not df.empty:
            df["Total Points"] = df["Credit"] * df["G.P."]
            total_credits = df["Credit"].sum()
            total_points = df["Total Points"].sum()
            gpa = round(total_points / total_credits, 2)
            cgpa = gpa  # First semester => CGPA = GPA

            st.success(f"📊 **GPA (1st Semester): {gpa}**")
            st.success(f"🎓 **CGPA (Cumulative): {cgpa}**")

            st.write("### Semester Summary")
            st.dataframe(df[["Course No", "Course Title", "Credit", "Marks", "L.G.", "G.P."]],
                         use_container_width=True)
        else:
            st.warning("Please fill in your course details first!")

# ------------------------- #
# Tab 2: Courses Entered
# ------------------------- #
with tab2:
    st.header("Courses Entered This Session")
    if "df" in locals() and not df.empty:
        st.dataframe(df[["Course No", "Course Title", "Credit", "Marks", "L.G.", "G.P."]],
                     use_container_width=True)
    else:
        st.info("No courses entered yet. Please go to the first tab to input your data.")
