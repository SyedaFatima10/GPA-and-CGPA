# =============================================
# 🎓 Streamlit App: GPA & CGPA Calculator (Excel + Manual Input)
# =============================================

import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="GPA & CGPA Calculator", layout="wide")

# -----------------------------
# App Header
# -----------------------------
st.title("🎓 GPA & CGPA Calculator till 4th Semester")
st.write("You can either upload your Excel marks file or input marks manually.")

# =============================
# SIDEBAR: File Upload
# =============================
st.sidebar.header("📂 Upload Your Excel File")
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx", "xls"])

# -----------------------------
# Function: GPA Calculation (Manual)
# -----------------------------
def calculate_gpa(marks):
    """Assuming GPA scale out of 4"""
    gpa_list = []
    for mark in marks:
        if mark >= 85:
            gpa_list.append(4.0)
        elif mark >= 80:
            gpa_list.append(3.7)
        elif mark >= 75:
            gpa_list.append(3.3)
        elif mark >= 70:
            gpa_list.append(3.0)
        elif mark >= 65:
            gpa_list.append(2.7)
        elif mark >= 60:
            gpa_list.append(2.3)
        elif mark >= 55:
            gpa_list.append(2.0)
        elif mark >= 50:
            gpa_list.append(1.7)
        elif mark >= 45:
            gpa_list.append(1.0)
        else:
            gpa_list.append(0.0)
    return round(sum(gpa_list)/len(gpa_list), 2)

# =============================
# IF EXCEL FILE IS UPLOADED
# =============================
if uploaded_file is not None:
    try:
        import openpyxl  # Required for Excel reading

        # Read Excel file
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.success("✅ Excel file uploaded successfully!")

        # -----------------------------
        # Display Uploaded Data
        # -----------------------------
        st.subheader("📊 Uploaded Marks Data")
        st.dataframe(df)

        # -----------------------------
        # Normalize Column Names
        # -----------------------------
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        rename_map = {}
        for col in df.columns:
            if "credit" in col:
                rename_map[col] = "credithours"
            elif "grade" in col and "point" in col:
                rename_map[col] = "gradepoint"
        df = df.rename(columns=rename_map)

        # Validate required columns
        if not {"semester", "credithours", "gradepoint"}.issubset(df.columns):
            st.error("❌ Missing required columns. Excel must have Semester, CreditHours, and GradePoint.")
            st.stop()

        # -----------------------------
        # Calculate GPA per Semester
        # -----------------------------
        gpa_summary = (
            df.groupby("semester")
            .apply(lambda x: (x["gradepoint"] * x["credithours"]).sum() / x["credithours"].sum())
            .reset_index(name="GPA")
        )

        # -----------------------------
        # Calculate CGPA
        # -----------------------------
        total_points = (df["gradepoint"] * df["credithours"]).sum()
        total_credits = df["credithours"].sum()
        cgpa = total_points / total_credits

        # -----------------------------
        # Create Tabs
        # -----------------------------
        tab1, tab2, tab3 = st.tabs(["📘 GPA per Semester", "📗 CGPA Summary", "📙 Course Details"])

        # TAB 1
        with tab1:
            st.header("📘 GPA per Semester")
            st.dataframe(gpa_summary.style.format({"GPA": "{:.2f}"}))
            st.bar_chart(gpa_summary.set_index("semester"))

        # TAB 2
        with tab2:
            st.header("📗 CGPA till 4th Semester")
            st.metric(label="🎯 CGPA", value=round(cgpa, 2))
            st.line_chart(gpa_summary.set_index("semester"))

        # TAB 3
        with tab3:
            st.header("📙 Course Details")
            st.dataframe(df)
            st.write("**Total Courses:**", df["course"].nunique())
            st.write("**Total Credit Hours:**", df["credithours"].sum())

    except ImportError:
        st.error("⚠️ Install 'openpyxl' using: pip install openpyxl")
        st.stop()
    except Exception as e:
        st.error(f"🚫 An unexpected error occurred: {e}")

# =============================
# MANUAL GPA & CGPA CALCULATOR
# =============================
st.sidebar.header("✏️ Or Input Marks Manually")
manual_calc = st.sidebar.checkbox("Enable Manual GPA Calculator")

if manual_calc:
    st.header("✏️ Manual GPA & CGPA Calculator")

    # Create tabs for semesters
    semesters = st.tabs(["Semester 1", "Semester 2", "Semester 3", "Semester 4"])
    semester_gpas = []

    for i, tab in enumerate(semesters):
        with tab:
            st.subheader(f"Semester {i+1}")
            num_courses = st.number_input(f"Number of courses in Semester {i+1}", min_value=1, step=1, key=f"num_{i}")
            marks = []
            for j in range(int(num_courses)):
                mark = st.number_input(f"Marks for Course {j+1} (0-100)", min_value=0, max_value=100, key=f"{i}_{j}")
                marks.append(mark)

            if st.button(f"Calculate GPA Semester {i+1}", key=f"btn_{i}"):
                gpa = calculate_gpa(marks)
                semester_gpas.append(gpa)
                st.success(f"GPA for Semester {i+1}: {gpa}")

    # Calculate CGPA after all semesters
    if len(semester_gpas) == 4:
        cgpa_manual = round(sum(semester_gpas)/4, 2)
        st.balloons()
        st.header(f"🎉 Your CGPA till 4th Semester: {cgpa_manual}")

# -----------------------------
# If no file uploaded
# -----------------------------
if uploaded_file is None and not manual_calc:
    st.info("👆 Upload Excel file or enable manual calculator to start.")
