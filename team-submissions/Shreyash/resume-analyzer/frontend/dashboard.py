import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils.parser import extract_text
from utils.analyzer import load_skills, extract_skills, get_required_skills
from utils.scorer import calculate_score, missing_skills
from utils.suggestions import generate_suggestions
from utils.resume_quality import project_score, experience_score, structure_score, skill_density_score
from utils.impact_analyzer import detect_achievements
from utils.bullet_analyzer import analyze_bullets
from utils.section_classifier import classify_sections
from utils.skill_gap import analyze_skill_gap
from utils.job_recommender import recommend_jobs


def run():

    st.set_page_config(
        page_title="AI Resume Analyzer",
        layout="centered",
        page_icon="📄"
    )

    st.markdown("""
<style>


.stApp{
background:
radial-gradient(circle at 20% 20%, #5b0f4a 0%, transparent 40%),
radial-gradient(circle at 80% 30%, #3c096c 0%, transparent 40%),
radial-gradient(circle at 50% 80%, #240046 0%, transparent 40%),
linear-gradient(180deg,#0d001a,#020006);
color:white;
}



.stButton>button{
background:linear-gradient(90deg,#800f2f,#7b2cbf);
border-radius:30px;
color:white;
font-weight:600;
border:none;
padding:0.6rem 1.4rem;
}



.stTextInput input {
background:#0a0016 !important;
border:1px solid rgba(255,255,255,0.2) !important;
border-radius:8px;
color:white !important;
}

label {
color:#e9d5ff !important;
font-weight:500;
}



[data-testid="stFileUploader"]{
background:rgba(0,0,0,0.35);
border-radius:14px;
border:1px solid rgba(255,255,255,0.2);
padding:1rem;
}

[data-testid="stFileUploaderDropzone"]{
background:rgba(0,0,0,0.35);
border:2px dashed rgba(255,255,255,0.25);
}


.stProgress > div > div > div {
background:linear-gradient(90deg,#9d4edd,#7b2cbf);
}



.skill-chip{
display:inline-block;
padding:8px 14px;
margin:6px;
background:linear-gradient(90deg,#7b2cbf,#9d4edd);
border-radius:30px;
font-size:14px;
transition:all 0.25s ease;
box-shadow:0 0 8px rgba(157,78,221,0.6);
}

.skill-chip:hover{
transform: translateY(-6px) scale(1.08);
box-shadow:0 0 20px rgba(200,120,255,1);
}



.analysis-box{
border:1px solid rgba(255,255,255,0.15);
border-radius:14px;
padding:20px;
margin-top:20px;
background:rgba(0,0,0,0.35);
backdrop-filter: blur(10px);
box-shadow:0 0 25px rgba(140,80,255,0.3);
}



.analysis-header{
font-size:20px;
font-weight:600;
padding:10px 15px;
margin-bottom:15px;
border-radius:8px;

background:linear-gradient(
90deg,
#d4d4d4,
#f5f5f5,
#bcbcbc,
#ffffff,
#d4d4d4
);

color:black;
letter-spacing:1px;
}



.analysis-table{
width:100%;
border-collapse:collapse;
}

.analysis-table td{
border:1px solid rgba(255,255,255,0.2);
padding:8px;
}



.tech-bullet{
color:#c77dff;
font-weight:600;
margin-right:8px;
}

[data-testid="stSelectbox"]{
display:none;
}
                
[data-testid="stFileUploaderFile"] p {
color:#f3e8ff !important;
}

[data-testid="stFileUploaderDropzone"] p {
color:#f3e8ff !important;
}
                
[data-testid="stFileUploader"] div,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p {
color: #ffffff !important;
}

[data-testid="stFileUploaderFile"] {
color: #ffffff !important;
}

[data-testid="stFileUploaderDropzone"] {
color: #ffffff !important;
}

[data-testid="stFileUploader"] button {
    color: #000000 !important;
    background: #ffffff !important;
}
h1 svg {
fill: #ffffff !important;
}   

.section-card{
border:1px solid rgba(255,255,255,0.15);
border-radius:14px;
padding:18px;
background:rgba(0,0,0,0.35);
box-shadow:0 0 20px rgba(140,80,255,0.25);
margin-top:15px;
height:100%;
display:flex;
flex-direction:column;
}

.section-header{
font-size:18px;
font-weight:600;
padding:8px 12px;
margin-bottom:12px;
border-radius:6px;

background:linear-gradient(
90deg,
#cfcfcf,
#f2f2f2,
#cfcfcf
);

color:black;
}

.stat-ball{
display:inline-block;
width:80px;
height:80px;
border-radius:50%;
background:linear-gradient(145deg,#7b2cbf,#9d4edd);
color:white;
font-size:22px;
font-weight:bold;
text-align:center;
line-height:80px;
margin:10px;
box-shadow:0 0 18px rgba(157,78,221,0.7);
}

.stat-label{
text-align:center;
font-size:12px;
margin-top:4px;
color:#e0e0e0;
}    

/* Galaxy title box */

.hero-box{
position:relative;
padding:30px 20px;
border-radius:18px;
margin-bottom:25px;
text-align:center;

background:
radial-gradient(circle at 20% 30%, rgba(255,255,255,0.15) 2px, transparent 3px),
radial-gradient(circle at 70% 20%, rgba(255,255,255,0.2) 1px, transparent 3px),
radial-gradient(circle at 40% 80%, rgba(255,255,255,0.15) 2px, transparent 4px),
linear-gradient(135deg,#240046,#5a189a,#3c096c);

box-shadow:
0 0 30px rgba(157,78,221,0.6),
inset 0 0 20px rgba(255,255,255,0.08);

border:2px solid rgba(255,255,255,0.25);
}

/* shiny metallic title */

.hero-title{
font-size:42px;
font-weight:800;

background:linear-gradient(
90deg,
#dcdcdc,
#ffffff,
#bfbfbf,
#ffffff,
#dcdcdc
);

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;

letter-spacing:1px;
}

/* subtitle */

.hero-subtitle{
color:#d0cde1;
font-size:16px;
margin-top:8px;
}

/* shine animation */

.hero-box:before{
content:"";
position:absolute;
top:0;
left:-75%;
width:50%;
height:100%;
background:linear-gradient(
120deg,
transparent,
rgba(255,255,255,0.3),
transparent
);
transform:skewX(-20deg);
animation:shine 6s infinite;
}

@keyframes shine{
0%{left:-75%;}
100%{left:130%;}
}

/* Streamlit top header color fix */

header[data-testid="stHeader"]{
background: linear-gradient(180deg,#240046,#3c096c);
}

div[data-testid="stToolbar"]{
background: linear-gradient(180deg,#240046,#3c096c);
}

header{
box-shadow:none;
}

</style>
""", unsafe_allow_html=True)

    st.markdown(
    """
    <div class="hero-box">

    <div class="hero-title">
    AI Resume Analyzer
    </div>

    <div class="hero-subtitle">
    Upload your resume and get AI powered ATS analysis, skill gap insights,
    and career recommendations.
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload Resume(s) (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files and len(uploaded_files) > 15:
        st.error("Maximum 15 resumes allowed.")
        st.stop()

    job_role = st.text_input("Enter Target Job Role")

    analyze = st.button("Analyze Resume")

    skills = load_skills("data/skills.json")

    if analyze and uploaded_files and job_role:

        all_scores = []
        resume_names = []
        resume_results = []

        for uploaded_file in uploaded_files:

            text = extract_text(uploaded_file)

            found_skills = extract_skills(text, skills)
            required_skills = get_required_skills(job_role)

            skill_score = calculate_score(found_skills, required_skills)

            proj_score = project_score(text)
            exp_score = experience_score(text)
            struct_score = structure_score(text)
            density_score = skill_density_score(text, found_skills)

            impact_score, achievement_count = detect_achievements(text)
            bullet_score, bullet_count = analyze_bullets(text)
            sections_detected = classify_sections(text)

            score = (
                0.35 * skill_score +
                0.15 * proj_score +
                0.15 * exp_score +
                0.10 * struct_score +
                0.10 * density_score +
                0.10 * impact_score +
                0.05 * bullet_score
            )

            all_scores.append(score)
            resume_names.append(uploaded_file.name)

            missing = missing_skills(found_skills, required_skills)

            matched_skills, gap_skills, match_count, total_required = analyze_skill_gap(found_skills, required_skills)

            recommended_jobs = recommend_jobs(found_skills)

            suggestions = generate_suggestions(found_skills, missing, text)

            resume_results.append({
                "text": text,
                "score": score,
                "found_skills": found_skills,
                "missing": missing,
                "matched_skills": matched_skills,
                "gap_skills": gap_skills,
                "match_count": match_count,
                "total_required": total_required,
                "recommended_jobs": recommended_jobs,
                "suggestions": suggestions,
                "achievement_count": achievement_count,
                "bullet_count": bullet_count,
                "sections_detected": sections_detected,
                "skill_score": skill_score,
                "proj_score": proj_score,
                "exp_score": exp_score,
                "struct_score": struct_score,
                "density_score": density_score,
                "impact_score": impact_score,
                "bullet_score": bullet_score
            })

        if len(resume_names) > 1:

            st.subheader("Resume Comparison")

            fig, ax = plt.subplots(figsize=(8,4))

            x = np.arange(len(resume_names))

            bars = ax.bar(
                x,
                all_scores,
                color="#9d4edd"
            )

            ax.set_xticks(x)
            ax.set_xticklabels(resume_names, rotation=20)

            ax.set_ylabel("ATS Score")
            ax.set_ylim(0,100)

            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2,
                    height + 1,
                    f"{height:.1f}",
                    ha="center",
                    va="bottom"
                )

            plt.tight_layout()
            st.pyplot(fig)

        if len(resume_names) > 1:
            best_index = np.argmax(all_scores)
            best_resume = resume_names[best_index]
            best_score = all_scores[best_index]

            st.success(f"🏆 Best Resume: **{best_resume}** (Score: {round(best_score,2)}%)")

        st.session_state["resume_results"] = resume_results
        st.session_state["resume_names"] = resume_names

        if len(st.session_state["resume_names"]) == 1:
            selected_resume = st.session_state["resume_names"][0]
        else:
            selected_resume = st.selectbox(
            "Select resume to inspect",
            st.session_state["resume_names"],
            key="resume_selector"
        )

        idx = st.session_state["resume_names"].index(selected_resume)
        data = st.session_state["resume_results"][idx]

        score = data["score"]

        st.markdown("## ATS Score")
        st.progress(int(max(min(score, 100), 0)))
        st.markdown(f"### {round(score,2)} %")

        st.subheader("Resume vs Industry Benchmark")

        labels = [
            "Skill Match",
            "Projects",
            "Experience",
            "Structure",
            "Density",
            "Impact",
            "Bullets"
        ]

        user_scores = [
            data["skill_score"],
            data["proj_score"],
            data["exp_score"],
            data["struct_score"],
            data["density_score"],
            data["impact_score"],
            data["bullet_score"]
        ]

        industry_scores = [
            65,
            60,
            55,
            70,
            60,
            50,
            55
        ]

        x = np.arange(len(labels))
        width = 0.38

        fig, ax = plt.subplots(figsize=(8,4))

        bars1 = ax.bar(x - width/2, user_scores, width, label="Your Resume", color="#c77dff")
        bars2 = ax.bar(x + width/2, industry_scores, width, label="Industry Average", color="#7b2cbf")

        ax.set_ylabel("Score")
        ax.set_ylim(0,100)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=20)
        ax.legend()

        plt.tight_layout()
        st.pyplot(fig)

        coverage = min(len(data["found_skills"]) / max(len(get_required_skills(job_role)), 1), 1)

        st.subheader("Skill Coverage")
        st.progress(int(coverage * 100))
        st.write(str(round(coverage * 100, 2)) + " % role skill coverage")

        st.subheader("Detected Skills")

        skill_html = ""
        for s in sorted(data["found_skills"]):
            skill_html += f'<span class="skill-chip">{s}</span>'

        st.markdown(skill_html, unsafe_allow_html=True)

        st.subheader("Missing Skills")

        missing_html = ""
        for s in data["missing"]:
            missing_html += f'<span class="skill-chip">{s}</span>'

        st.markdown(missing_html, unsafe_allow_html=True)

        st.subheader("AI Skill Gap Analysis")

        st.write("Matched Skills:", data["match_count"], "/", data["total_required"])

        if len(data["gap_skills"]) > 0:
            for s in data["gap_skills"]:
                st.markdown(f'<span class="tech-bullet">⚙</span>{s}', unsafe_allow_html=True)
        else:
            st.write("Your resume already covers the required skill set.")

        st.subheader("AI Career Recommendations")

        if len(data["recommended_jobs"]) > 0:
            for job in data["recommended_jobs"]:
                st.markdown(f'<span class="tech-bullet">🚀</span>{job}', unsafe_allow_html=True)
        else:
            st.write("Not enough skill signals detected to recommend roles.")

        st.subheader("Analysis Visualizations")

        colA, colB = st.columns(2)

        with colA:
            labels = ["Matched Skills", "Missing Skills"]
            values = [len(data["matched_skills"]), len(data["missing"])]
            fig, ax = plt.subplots()
            ax.bar(labels, values)
            st.pyplot(fig)

        with colB:
            labels = ["Skill","Projects","Experience","Structure","Density","Impact","Bullets"]
            values = [
                data["skill_score"],
                data["proj_score"],
                data["exp_score"],
                data["struct_score"],
                data["density_score"],
                data["impact_score"],
                data["bullet_score"]
            ]
            values.append(values[0])
            angles = np.linspace(0, 2*np.pi, len(values), endpoint=False).tolist()

            fig = plt.figure(figsize=(3,3))
            ax = plt.subplot(111, polar=True)
            ax.plot(angles, values)
            ax.fill(angles, values, alpha=0.25)
            ax.set_ylim(0,100)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)

            st.pyplot(fig)

        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:

            detect_html = """
            <div class="section-card" style="height:100%">
            <div class="section-header">
            Resume Section Detection
            </div>
            """

            for sec in data["sections_detected"]:

                if data["sections_detected"][sec]:
                    detect_html += f"✓ {sec.capitalize()}<br>"
                else:
                    detect_html += f"✗ {sec.capitalize()}<br>"

            detect_html += "</div>"

            st.markdown(detect_html, unsafe_allow_html=True)

        with col2:

            word_count = len(data["text"].split())

            stats_html = f"""
            <div class="section-card" style="height:100%">

            <div class="section-header">
            Resume Statistics
            </div>

            <div style="
                display:grid;
                grid-template-columns:1fr 1fr;
                gap:10px;
                justify-items:center;
                align-items:center;
            ">

            <div>
            <div class="stat-ball">{data["achievement_count"]}</div>
            <div class="stat-label">Achievements</div>
            </div>

            <div>
            <div class="stat-ball">{data["bullet_count"]}</div>
            <div class="stat-label">Bullets</div>
            </div>

            <div>
            <div class="stat-ball">{len(data["found_skills"])}</div>
            <div class="stat-label">Skills</div>
            </div>

            <div>
            <div class="stat-ball">{len(data["missing"])}</div>
            <div class="stat-label">Missing</div>
            </div>

            </div>
            </div>
            """

            st.markdown(stats_html, unsafe_allow_html=True)



        suggest_html = """
        <div class="section-card">

        <div class="section-header">
        Resume Suggestions
        </div>
        """

        if len(data["suggestions"]) > 0:

            for s in data["suggestions"]:
                suggest_html += f"🧠 {s}<br><br>"

        else:
            suggest_html += "No suggestions detected."

        suggest_html += "</div>"

        st.markdown(suggest_html, unsafe_allow_html=True)
