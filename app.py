# =============================================
# 🎓 Streamlit App: GPA & CGPA Calculator (Excel Only, Error-Free)
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
st.write("Upload your Excel marks file (.xlsx or .xls) to automatically calculate GPA and CGPA.")

# -----------------------------
# File Upload Section (Excel only)
# -----------------------------
st.sidebar.header("📂 Upload Your Excel File")
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx", "xls"])

# -----------------------------
# When user uploads a file
# -----------------------------
if uploaded_file is not None:
    try:
        # Try to import openpyxl (required for Excel reading)
        import openpyxl

        # Read Excel file safely
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        st.success("✅ Excel file uploaded successfully!")

        # -----------------------------
        # Display the uploaded data
        # -----------------------------
        st.subheader("📊 Uploaded Marks Data")
        st.dataframe(df)

        # -----------------------------
        # Check if required columns exist
        # -----------------------------
        required_cols = {"Semester", "Course", "Credit_Hours", "Grade_Point"}
        if not required_cols.issubset(df.columns):
            st.error("❌ Missing required columns. Please include: Semester, Course, Credit_Hours, and Grade_Point.")
            st.stop()

        # -----------------------------
        # Create Tabs
        # -----------------------------
        tab1, tab2, tab3 = st.tabs(["📘 GPA per Semester", "📗 CGPA Summary", "📙 Course Details"])

        # ==================================================
        # TAB 1: GPA PER SEMESTER
        # ==================================================
        with tab1:
            st.header("📘 GPA Calculation per Semester")

            # GPA = Sum(Grade_Point * Credit_Hours) / Sum(Credit_Hours)
            gpa_summary = (
                df.groupby("Semester")
                .apply(lambda x: (x["Grade_Point"] * x["Credit_Hours"]).sum() / x["Credit_Hours"].sum())
                .reset_index(name="GPA")
            )

            st.dataframe(gpa_summary.style.format({"GPA": "{:.2f}"}))
            st.bar_chart(gpa_summary.set_index("Semester"))

        # ==================================================
        # TAB 2: CGPA SUMMARY
        # ==================================================
        with tab2:
            st.header("📗 CGPA till 4th Semester")

            total_points = (df["Grade_Point"] * df["Credit_Hours"]).sum()
            total_credits = df["Credit_Hours"].sum()
            cgpa = total_points / total_credits

            st.metric(label="🎯 Cumulative Grade Point Average (CGPA)", value=round(cgpa, 2))

            # Line chart showing GPA trend by semester
            st.line_chart(gpa_summary.set_index("Semester"))

        # ==================================================
        # TAB 3: COURSE DETAILS
        # ==================================================
        with tab3:
            st.header("📙 Course Details")
            st.dataframe(df)
            st.write("**Total Courses:**", df["Course"].nunique())
            st.write("**Total Credit Hours:**", df["Credit_Hours"].sum())

    except ImportError:
        # Show user-friendly message if openpyxl is missing
        st.error("⚠️ Missing dependency: Please install 'openpyxl' using the command below:")
        st.code("pip install openpyxl")
        st.stop()

    except Exception as e:
        # Handle unexpected errors gracefully
        st.error(f"🚫 An unexpected error occurred: {e}")

# -----------------------------
# If no file uploaded yet
# -----------------------------
else:
    st.info("👆 Please upload your Excel file (.xlsx or .xls) to start calculating your GPA and CGPA.")
