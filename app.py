import streamlit as st
import pandas as pd
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from analyzer import analyze_careers
from roadmap import get_roadmap
from skill_gap import get_skill_gap
from ml_model import predict_career


st.set_page_config(
    page_title="AI Student Career Analyzer",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🎓 AI Student Career & Skill Analyzer")

st.write(
    "Analyze your technical skills, discover suitable career paths, "
    "identify skill gaps, and get an AI-powered career prediction."
)

st.divider()


# =========================================================
# STUDENT INFORMATION
# =========================================================

st.header("👤 Student Information")

col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("Enter your name")

with col2:
    education = st.selectbox(
        "Select your education",
        [
            "B.Tech",
            "B.E",
            "B.Sc",
            "BCA",
            "MCA",
            "Other"
        ]
    )

with col3:
    branch = st.selectbox(
        "Select your branch",
        [
            "Computer Science Engineering",
            "Information Technology",
            "Electronics and Communication",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Other"
        ]
    )


st.divider()


# =========================================================
# SKILLS
# =========================================================

st.header("💻 Select Your Technical Skills")

available_skills = [
    "Python",
    "Java",
    "C",
    "OOP",
    "DSA",
    "SQL",
    "Git",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Pandas",
    "NumPy",
    "Statistics",
    "Excel",
    "Data Visualization",
    "Machine Learning",
    "Scikit-learn",
    "APIs"
]

student_skills = st.multiselect(
    "Choose the skills you currently have",
    available_skills
)


st.divider()


# =========================================================
# PDF REPORT FUNCTION
# =========================================================

def create_pdf_report(
    name,
    education,
    branch,
    student_skills,
    best_career,
    results,
    roadmap,
    predicted_career,
    ml_probabilities
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    story = []

    story.append(
        Paragraph(
            "AI Student Career & Skill Analyzer",
            title_style
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Student Name:</b> {name}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Education:</b> {education}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Branch:</b> {branch}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Technical Skills:</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            ", ".join(student_skills),
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Rule-Based Best Career:</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"{best_career['career']} - "
            f"{best_career['score']}% Match",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>AI/ML Predicted Career:</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"{predicted_career}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>ML Career Probabilities:</b>",
            styles["Heading2"]
        )
    )

    for career, probability in ml_probabilities.items():

        story.append(
            Paragraph(
                f"{career}: {probability}%",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Skills You Have:</b>",
            styles["Heading2"]
        )
    )

    if best_career["matched_skills"]:

        story.append(
            Paragraph(
                ", ".join(
                    best_career["matched_skills"]
                ),
                styles["Normal"]
            )
        )

    else:

        story.append(
            Paragraph(
                "No matching skills",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Skills You Need to Learn:</b>",
            styles["Heading2"]
        )
    )

    if best_career["missing_skills"]:

        story.append(
            Paragraph(
                ", ".join(
                    best_career["missing_skills"]
                ),
                styles["Normal"]
            )
        )

    else:

        story.append(
            Paragraph(
                "You have all the required skills.",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Career Recommendations:</b>",
            styles["Heading2"]
        )
    )

    for result in results:

        story.append(
            Paragraph(
                f"{result['career']} - "
                f"{result['score']}% Match",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Learning Roadmap:</b>",
            styles["Heading2"]
        )
    )

    for number, step in enumerate(
        roadmap,
        start=1
    ):

        story.append(
            Paragraph(
                f"Step {number}: {step}",
                styles["Normal"]
            )
        )

    document.build(story)

    buffer.seek(0)

    return buffer


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🔍 Analyze My Career",
    type="primary"
):

    if not name:

        st.warning(
            "Please enter your name."
        )

    elif not student_skills:

        st.warning(
            "Please select at least one skill."
        )

    else:

        # Rule-based analysis
        results = analyze_careers(
            student_skills
        )

        best_career = results[0]

        # ML prediction
        predicted_career, ml_probabilities = predict_career(
            student_skills
        )

        st.success(
            f"Analysis completed for {name}! 🎉"
        )


        # =================================================
        # DASHBOARD
        # =================================================

        st.header(
            "📊 Student Career Dashboard"
        )

        total_possible_skills = len(
            available_skills
        )

        skill_score = round(
            (
                len(student_skills)
                / total_possible_skills
            ) * 100,
            2
        )

        skills_to_learn = len(
            best_career["missing_skills"]
        )

        best_match = best_career["score"]

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "💻 Skills Selected",
                len(student_skills)
            )

        with col2:

            st.metric(
                "📈 Overall Skill Score",
                f"{skill_score}%"
            )

        with col3:

            st.metric(
                "🏆 Best Career Match",
                f"{best_match}%"
            )

        with col4:

            st.metric(
                "📚 Skills to Learn",
                skills_to_learn
            )


        st.divider()


        # =================================================
        # AI/ML PREDICTION
        # =================================================

        st.header(
            "🧠 AI/ML Career Prediction"
        )

        st.success(
            f"🤖 Predicted Career: {predicted_career}"
        )

        predicted_probability = ml_probabilities[
            predicted_career
        ]

        st.write(
            f"**ML Confidence: "
            f"{predicted_probability}%**"
        )

        st.progress(
            int(predicted_probability)
        )


        st.subheader(
            "📊 Career Prediction Probabilities"
        )

        ml_chart_data = pd.DataFrame({
            "Career": list(
                ml_probabilities.keys()
            ),
            "Probability": list(
                ml_probabilities.values()
            )
        })

        st.bar_chart(
            ml_chart_data.set_index(
                "Career"
            )
        )


        st.divider()


        # =================================================
        # BEST CAREER
        # =================================================

        st.header(
            "🏆 Best Career Recommendation"
        )

        st.success(
            f"{best_career['career']} — "
            f"{best_match}% Match"
        )

        st.write(
            f"Your current skills have a "
            f"**{best_match}% match** with this career."
        )

        st.progress(
            int(best_match)
        )


        st.divider()


        # =================================================
        # CAREER MATCH CHART
        # =================================================

        st.header(
            "📈 Career Match Overview"
        )

        chart_data = pd.DataFrame({
            "Career": [
                result["career"]
                for result in results
            ],
            "Match": [
                result["score"]
                for result in results
            ]
        })

        st.bar_chart(
            chart_data.set_index(
                "Career"
            )
        )


        st.divider()


        # =================================================
        # AI SKILL GAP
        # =================================================

        st.header(
            "🤖 AI Skill Gap Analysis"
        )

        skill_gap = get_skill_gap(
            best_career
        )

        for item in skill_gap:

            st.write(
                f"📌 {item}"
            )


        st.divider()


        # =================================================
        # DETAILED SKILLS
        # =================================================

        st.header(
            "🔎 Detailed Skill Analysis"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "✅ Skills You Have"
            )

            if best_career["matched_skills"]:

                for skill in best_career[
                    "matched_skills"
                ]:

                    st.write(
                        f"✅ {skill}"
                    )

            else:

                st.write(
                    "No matching skills yet."
                )


        with col2:

            st.subheader(
                "📚 Skills You Need"
            )

            if best_career["missing_skills"]:

                for skill in best_career[
                    "missing_skills"
                ]:

                    st.write(
                        f"📚 {skill}"
                    )

            else:

                st.success(
                    "You have all the required skills!"
                )


        st.divider()


        # =================================================
        # CAREER RECOMMENDATIONS
        # =================================================

        st.header(
            "🎯 Career Recommendations"
        )

        for index, result in enumerate(
            results
        ):

            st.subheader(
                f"{index + 1}. "
                f"{result['career']}"
            )

            st.progress(
                int(result["score"])
            )

            st.write(
                f"**Career Match: "
                f"{result['score']}%**"
            )

            if result["matched_skills"]:

                st.write(
                    "**✅ Matching Skills:** "
                    + ", ".join(
                        result["matched_skills"]
                    )
                )

            else:

                st.write(
                    "**✅ Matching Skills:** None"
                )

            if result["missing_skills"]:

                st.write(
                    "**📚 Skills to Learn:** "
                    + ", ".join(
                        result["missing_skills"]
                    )
                )

            else:

                st.success(
                    "🎉 You already have all "
                    "required skills!"
                )

            with st.expander(
                "📚 View Learning Roadmap"
            ):

                roadmap = get_roadmap(
                    result["career"]
                )

                for step_number, step in enumerate(
                    roadmap,
                    start=1
                ):

                    st.write(
                        f"**Step {step_number}:** "
                        f"{step}"
                    )

            st.divider()


        # =================================================
        # PERFORMANCE SUMMARY
        # =================================================

        st.header(
            "📊 Performance Summary"
        )

        if skill_score >= 75:

            st.success(
                "🌟 Excellent! You have developed "
                "a strong technical skill base."
            )

        elif skill_score >= 50:

            st.info(
                "👍 Good progress! Continue learning "
                "new technical skills."
            )

        else:

            st.warning(
                "🚀 You are at the beginning of "
                "your journey. Follow the roadmap "
                "and build projects."
            )


        # =================================================
        # CAREER ADVICE
        # =================================================

        st.header(
            "💡 Career Advice"
        )

        if best_match >= 80:

            st.success(
                f"You are strongly aligned with the "
                f"{best_career['career']} career path. "
                "Focus on projects, advanced concepts, "
                "and interview preparation."
            )

        elif best_match >= 50:

            st.info(
                f"You have a good foundation for "
                f"{best_career['career']}. "
                "Work on the missing skills and "
                "build practical projects."
            )

        else:

            st.warning(
                f"You need to develop more skills for "
                f"{best_career['career']}. "
                "Follow the learning roadmap step by step."
            )


        st.divider()


        # =================================================
        # DOWNLOAD PDF REPORT
        # =================================================

        st.header(
            "📄 Career Report"
        )

        st.write(
            "Download your complete career analysis "
            "as a PDF report."
        )

        best_roadmap = get_roadmap(
            best_career["career"]
        )

        pdf_file = create_pdf_report(
            name,
            education,
            branch,
            student_skills,
            best_career,
            results,
            best_roadmap,
            predicted_career,
            ml_probabilities
        )

        st.download_button(
            label="📥 Download Career Report",
            data=pdf_file,
            file_name="career_analysis_report.pdf",
            mime="application/pdf"
        )


        st.divider()

        st.caption(
            "🎓 AI Student Career & Skill Analyzer | "
            "AI/ML Powered Career Guidance"
        )