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

        # Expected column names after cleaning
        required_cols = {"semester", "course", "credithours", "gradepoint"}

        # Try alternate spellings
        rename_map = {}
        for col in df.columns:
            if "credit" in col:
                rename_map[col] = "credithours"
            elif "grade" in col and "point" in col:
                rename_map[col] = "gradepoint"
        df = df.rename(columns=rename_map)

        # Validate columns
        if not {"semester", "credithours", "gradepoint"}.issubset(df.columns):
            st.error("❌ Missing required columns. Your Excel must have columns for Semester, CreditHours, and GradePoint.")
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
        # Calculate CGPA (Cumulative)
        # -----------------------------
        total_points = (df["gradepoint"] * df["credithours"]).sum()
        total_credits = df["credithours"].sum()
        cgpa = total_points / total_credits

        # -----------------------------
        # Create Tabs
        # -----------------------------
        tab1, tab2, tab3 = st.tabs(["📘 GPA per Semester", "📗 CGPA Summary", "📙 Course Details"])

        # ==================================================
        # TAB 1: GPA PER SEMESTER
        # ==================================================
        with tab1:
            st.header("📘 GPA Calculation per Semester")
            st.dataframe(gpa_summary.style.format({"GPA": "{:.2f}"}))
            st.bar_chart(gpa_summary.set_index("semester"))

        # ==================================================
        # TAB 2: CGPA SUMMARY
        # ==================================================
        with tab2:
            st.header("📗 CGPA till 4th Semester")
            st.metric(label="🎯 Cumulative Grade Point Average (CGPA)", value=round(cgpa, 2))
            st.line_chart(gpa_summary.set_index("semester"))

        # ==================================================
        # TAB 3: COURSE DETAILS
        # ==================================================
        with tab3:
            st.header("📙 Course Details")
            st.dataframe(df)
            st.write("**Total Courses:**", df["course"].nunique())
            st.write("**Total Credit Hours:**", df["credithours"].sum())

    except ImportError:
        st.error("⚠️ Missing dependency: Please install 'openpyxl' using this command:")
        st.code("pip install openpyxl")
        st.stop()

    except Exception as e:
        st.error(f"🚫 An unexpected error occurred: {e}")

# -----------------------------
# If no file uploaded yet
# -----------------------------
else:
    st.info("👆 Please upload your Excel file (.xlsx or .xls) to start calculating your GPA and CGPA.")
