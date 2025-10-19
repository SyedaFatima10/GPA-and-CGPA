import streamlit as st
import pandas as pd

# ------------------------- #
# Streamlit Page Settings
# ------------------------- #
st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓", layout="centered")

# ------------------------- #
# Custom Page Styling
# ------------------------- #
st.markdown(
    """
    <style>
    body {
        background-color: #f0f4f8;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1a237e;
        text-align: center;
        font-weight: bold;
    }
    h2 {
        color: #0d47a1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎓 GPA & CGPA Calculator (1st–4th Semester)")
st.write("Enter course details for each semester to calculate GPA and CGPA.")

# ------------------------- #
# Helper Function: Grade Conversion
# ------------------------- #
def grade_from_marks(marks):
    if marks >= 85:
        return "A+", 4.00
    elif marks >= 80:
        return "A", 3.66
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
# Semester Tabs
# ------------------------- #
tabs = st.tabs(["📘 Semester 1", "📗 Semester 2", "📙 Semester 3", "📕 Semester 4", "📊 Summary"])

semester_data = {}
semester_gpa = []

for i in range(4):
    with tabs[i]:
        st.header(f"Semester {i+1} Details")

        n = st.number_input(f"Number of courses in Semester {i+1}", min_value=1, max_value=10, value=6, key=f"num_{i}")
        course_data = []

        for j in range(1, n + 1):
            st.subheader(f"Course {j}")
            code = st.text_input("Course Code", key=f"code_{i}_{j}")
            name = st.text_input("Course Title", key=f"name_{i}_{j}")
            credit = st.number_input("Credit Hours", min_value=1, max_value=4, key=f"credit_{i}_{j}")
            marks = st.number_input("Marks (0–100)", min_value=0, max_value=100, key=f"marks_{i}_{j}")

            grade, gp = grade_from_marks(marks)
            course_data.append({
                "Course No": code,
                "Course Title": name,
                "Credit": credit,
                "Marks": marks,
                "L.G.": grade,
                "G.P.": gp
            })

        df = pd.DataFrame(course_data)
        semester_data[f"Semester_{i+1}"] = df

        if not df.empty and df["Credit"].sum() > 0:
            df["Total Points"] = df["Credit"] * df["G.P."]
            gpa = round(df["Total Points"].sum() / df["Credit"].sum(), 2)
            semester_gpa.append(gpa)

            st.success(f"📊 GPA for Semester {i+1}: **{gpa}**")

            # Neat Table
            st.dataframe(df.style.set_table_styles(
                [{
                    'selector': 'thead th',
                    'props': [('background-color', '#1e88e5'), ('color', 'white')]
                },
                {
                    'selector': 'tbody td',
                    'props': [('background-color', '#e3f2fd')]
                }]
            ), use_container_width=True)
        else:
            st.info("Please enter complete course details.")

# ------------------------- #
# Summary Tab: CGPA Display
# ------------------------- #
with tabs[4]:
    st.header("📊 Overall GPA & CGPA Summary")

    if semester_gpa:
        summary_df = pd.DataFrame({
            "Semester": [f"Semester {i+1}" for i in range(len(semester_gpa))],
            "GPA": semester_gpa
        })
        cgpa = round(sum(semester_gpa) / len(semester_gpa), 2)

        st.success(f"🎯 **Cumulative CGPA (1st–4th Semester): {cgpa}**")
        st.dataframe(summary_df.style.set_table_styles(
            [{
                'selector': 'thead th',
                'props': [('background-color', '#1565c0'), ('color', 'white')]
            },
            {
                'selector': 'tbody td',
                'props': [('background-color', '#bbdefb')]
            }]
        ), use_container_width=True)

        st.line_chart(summary_df.set_index("Semester")["GPA"], use_container_width=True)
    else:
        st.info("Please calculate GPA for each semester first.")
