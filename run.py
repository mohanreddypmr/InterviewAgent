import streamlit as st

# Sample JSON data
import json

# Load your actual json_data here
json_data = json.load(open("tt.json"))

st.set_page_config(page_title="AI Engineer Resume", layout="wide")
st.title("📄 AI Engineer Resume")

# === Work Experience ===
if "work_experience" in json_data:
    st.subheader("💼 Work Experience")
    for exp in json_data["work_experience"]:
        with st.container():
            st.markdown(f"### **{exp.get('Title', 'N/A')}** at **{exp.get('Company', 'N/A')}**")
            st.markdown(f"*{exp.get('Duration', 'N/A')}*")
            for resp in exp.get("Responsibilities", []):
                st.markdown(f"- {resp}")
            for proj in exp.get("Projects", []):
                with st.expander(f"📌 {proj.get('title', 'Project')}"):
                    st.markdown(proj.get("description", ""))
                    techs = proj.get("technologies", [])
                    if techs:
                        st.markdown("**Technologies:** " + ", ".join(f"`{tech}`" for tech in techs))

# === Personal Projects ===
if "projects" in json_data:
    st.subheader("🧠 Personal Projects")
    for proj in json_data["projects"]:
        with st.expander(f"📍 {proj.get('title', 'Project')}"):
            st.markdown(proj.get("description", ""))
            techs = proj.get("technologies", [])
            if techs:
                st.markdown("**Technologies:** " + ", ".join(f"`{tech}`" for tech in techs))

# === Skills ===
if "skills" in json_data:
    st.subheader("🛠 Skills")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Technical Skills**")
        for skill in json_data["skills"].get("technical_skills", []):
            st.markdown(f"- {skill}")
    with col2:
        st.markdown("**Soft Skills**")
        for skill in json_data["skills"].get("soft_skills", []):
            st.markdown(f"- {skill}")
    with col3:
        st.markdown("**Languages & Tools**")
        for lang in json_data["skills"].get("languages", []):
            st.markdown(f"- {lang}")
        for tool in json_data["skills"].get("tools_and_platforms", []):
            st.markdown(f"- {tool}")

# === Education ===
if "education" in json_data:
    st.subheader("🎓 Education")
    for edu in json_data["education"]:
        st.markdown(f"**{edu.get('institution', 'N/A')}**")
        st.markdown(f"*{edu.get('degree', '')} ({edu.get('year', '')})*")
        st.markdown("---")

# === Publications & Research ===
if "publications_research" in json_data:
    st.subheader("📚 Publications & Research")
    for pub in json_data["publications_research"]:
        with st.expander(f"🔖 {pub.get('title', 'Untitled')}"):
            st.markdown(f"**Authors:** {', '.join(pub.get('authors', []))}")
            st.markdown(f"**Published In:** {pub.get('publication_venue', 'N/A')} ({pub.get('year', '')})")
            st.markdown(f"**Description:** {pub.get('description', '')}")
            if "doi_or_link" in pub:
                st.markdown(f"[DOI / Link]({pub['doi_or_link']})")

# === Footer ===
st.markdown("---")
st.markdown("📌 *This resume was rendered using Streamlit.*")
