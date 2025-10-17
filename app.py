# =============================================
# 🎓 Streamlit App: GPA & CGPA Calculator till 4th Semester
# =============================================

# Importing required libraries
import streamlit as st
import pandas as pd

# -----------------------------
# App Title and Description
# -----------------------------
st.set_page_config(page_title="GPA & CGPA Calculator", layout="wide")
st.title("🎓 GPA & CGPA Calculator till 4th Semester")
st.write("Upload your marks file to automatically calculate GPA and CGPA for up to 4 semesters.")

# -----------------------------
# File Upload Section
# -----------------------------
st.sidebar.header("📂 Upload Your Marks File")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

# -----------------------------
# If user uploads a file
# -----------------------------
if uploaded_file is not None:

    # Detect file type and read accordingly
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully!")

    # Display the uploaded data
    st.subheader("📊 Uploaded Marks Data")
    st.dataframe(df)

    # -----------------------------
    # Expected Columns in the Data
    # -----------------------------
    st.markdown("""
    **Your file should include the following columns:**
    - `Semester` (1–4)
    - `Course` (Course name)
    - `Credit_Hours`
    - `Grade_Point` (4.0 scale)
    """)

    # Check if required columns exist
    required_columns = {"Semester", "Course", "Credit_Hours", "Grade_Point"}
    if not required_columns.issubset(df.columns):
        st.error("❌ The uploaded file must contain the columns: Semester, Course, Credit_Hours, and Grade_Point.")
    else:
        # -----------------------------
        # Tabs for separate sections
        # -----------------------------
        tab1, tab2, tab3 = st.tabs(["📘 GPA per Semester", "📗 CGPA Summary", "📙 Course Details"])

        # =============================
        # TAB 1: GPA per Semester
        # =============================
        with tab1:
            st.header("📘 GPA Calculation for Each Semester")

            # Calculate GPA for each semester
            gpa_summary = (
                df.groupby("Semester")
                .apply(lambda x: (x["Grade_Point"] * x["Credit_Hours"]).sum() / x["Credit_Hours"].sum())
                .reset_index(name="GPA")
            )

            st.dataframe(gpa_summary)

            # Display bar chart
            st.bar_chart(gpa_summary.set_index("Semester"))

        # =============================
        # TAB 2: CGPA Summary
        # =============================
        with tab2:
            st.header("📗 CGPA till 4th Semester")

            # Calculate cumulative totals
            total_points = (df["Grade_Point"] * df["Credit_Hours"]).sum()
            total_credits = df["Credit_Hours"].sum()

            cgpa = total_points / total_credits

            st.metric(label="🎯 Cumulative Grade Point Average (CGPA)", value=round(cgpa, 2))

            # Display cumulative GPA trend
            cumulative_data = (
                df.groupby("Semester")
                .apply(lambda x: (x["Grade_Point"] * x["Credit_Hours"]).sum() / x["Credit_Hours"].sum())
                .cumsum() / (df["Semester"].unique().size)
            ).reset_index(name="Cumulative GPA")

            st.line_chart(cumulative_data.set_index("Semester"))

        # =============================
        # TAB 3: Course Details
        # =============================
        with tab3:
            st.header("📙 All Course Details")
            st.dataframe(df)

            st.write("Total Courses:", df["Course"].nunique())
            st.write("Total Credit Hours:", df["Credit_Hours"].sum())

else:
    # Display message if no file uploaded
    st.info("👆 Please upload your marks file to start calculating your GPA and CGPA.")
