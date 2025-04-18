import streamlit as st
import pandas as pd
import json
import google.generativeai as genai
from bs4 import BeautifulSoup
import requests
import re
from dotenv import load_dotenv
import os

# Load the API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

if "job_desc" not in st.session_state:
    st.session_state.job_desc = ""
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "raw_json" not in st.session_state:
    st.session_state.raw_json = ""
if "selected_query" not in st.session_state:
    st.session_state.selected_query = ""

st.markdown("""
    <style>
    .stButton>button {
        background-color: #005B96;
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #003F6C;
    }
    .stDataFrame {
        border: 1px solid #E5E7EB;
        border-radius: 5px;
    }
    h1, h2, h3 {
        color: #005B96;
    }
    .stTextInput>label, .stSelectbox>label, .stRadio>label {
        color: #374151;
        font-weight: 500;
    }
    .css-1aumxhk {  /* Adjust table header width */
        max-width: 100%;
    }
    .css-1d8v9i5 {  /* Ensure table fits content */
        overflow-x: auto;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_catalog_data():
    try:
        return pd.read_csv("catalog.csv")
    except Exception as e:
        st.error(f"CSV you asked for could not be found or is Unreadable: {e}")
        return pd.DataFrame()

def json_extraction(response_text):
    try:
        match = re.search(r'\[\s*{.*?}\s*]', response_text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return []

def get_assessment_recommendation(query):
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = (
        "You are a helpful assistant. Based on the following job description, recommend up to 10 relevant SHL assessments.\n\n"
        f"{query.strip()}\n\n"
        "Your response MUST be a valid JSON list. Each object in the list should have the following six keys:\n"
        "- Assessment Name\n"
        "- URL (must link to SHL’s catalog)\n"
        "- Remote Testing Support (Yes/No)\n"
        "- Adaptive/IRT Support (Yes/No)\n"
        "- Duration\n"
        "- Test Type\n\n"
        "Respond ONLY in valid JSON format like this:\n"
        '[{"Assessment Name": "...", "URL": "...", "Remote Testing Support": "Yes", '
        '"Adaptive/IRT Support": "No", "Duration": "30 mins", "Test Type": "Cognitive"}]'
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Gemini API for SHL has Failed: {e}. Try specifying skills or duration clearly.")
        return []

def extract_raw_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text(separator='\n', strip=True)
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return {
            "text": page_text,
            "links": links
        }
    except Exception as e:
        return {"error": str(e)}

def fetch_description(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        st.error(f"Sorry we were unable to fetch job description from url: {url}: {e}")
        return ""

st.markdown("""
    <div style='display: flex; align-items: center;'>
        <img src='https://www.shl.com/assets/header-graphics/SHL-logo-colour-update.svg' style='height: 50px; margin-right: 10px;'>
        <h1 style='margin: 0;'>Assessment Recommendation System</h1>
    </div>
""", unsafe_allow_html=True)

sample_queries = [
    "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes .",
    "Looking to hire mid-level professionals who are proficient in Python, SQL and Java Script. Need an assessment package that can test all skills with max duration of 60 minutes. ",
    "I am hiring for an analyst and wants applications to screen using Cognitive and personality tests, what options are available within 45 mins.."
]

input_type = st.radio("Select input type:", ["Job Description Text", "Job Description URL"], key="input_type_radio", horizontal=True)

if input_type == "Job Description URL":
    default_query = ""
else:
    default_query = st.session_state.get("selected_query", "")

job_desc = st.selectbox(
    "Select a sample query or enter your own:",
    [""] + sample_queries,
    format_func=lambda x: "Custom input" if x == "" else x[:50] + "...",
    key="sample_query",
    index=0 if input_type == "Job Description URL" else sample_queries.index(default_query) + 1 if default_query in sample_queries else 0
)

if input_type == "Job Description Text":
    if not job_desc:
        job_desc = st.text_area("Paste the job description here:", height=150, key="text_input", value=st.session_state.job_desc)
else:
    job_url = st.text_input("Enter the job description URL:", key="url_input", help="E.g., https://example.com/job")
    if job_url and re.match(r'^https?://[^\s/$.?#].[^\s]*$', job_url):
        scraped = extract_raw_data(job_url)
        if "error" not in scraped:
            job_desc = scraped["text"]
            st.success("URL content fetched successfully!")
        else:
            st.markdown(f'<div class="error-alert">Failed to fetch URL: {scraped["error"]}</div>', unsafe_allow_html=True)
            job_desc = ""
    elif job_url:
        st.markdown('<div class="error-alert">Invalid URL format. Use http:// or https://</div>', unsafe_allow_html=True)
        job_desc = ""

st.session_state.job_desc = job_desc
st.session_state.selected_query = job_desc if job_desc in sample_queries else ""

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Recommend Assessments") and job_desc.strip():
        with st.spinner("Fetching SHL assessment recommendations..."):
            raw_json = get_assessment_recommendation(job_desc)
            st.session_state.raw_json = raw_json
            st.session_state.recommendations = json_extraction(raw_json)
with col2:
    if st.button("Reset"):
        st.session_state.job_desc = ""
        st.session_state.selected_query = ""
        st.session_state.recommendations = []
        st.session_state.raw_json = ""
        st.rerun()

if st.session_state.recommendations:
    st.subheader("📄 Raw JSON Response")
    st.code(st.session_state.raw_json, language="json")

    required_keys = {
        "Assessment Name", "URL", "Remote Testing Support",
        "Adaptive/IRT Support", "Duration", "Test Type"
    }

    valid_recs = [rec for rec in st.session_state.recommendations if required_keys.issubset(rec.keys())]
    
    if valid_recs:
        st.subheader("Filter Recommendations")
        test_types = set()
        for rec in valid_recs:
            if isinstance(rec["Test Type"], str):
                test_types.add(rec["Test Type"])
            elif isinstance(rec["Test Type"], list):
                test_types.update(rec["Test Type"])
        selected_test_types = st.multiselect("Filter by Test Type:", sorted(test_types), key="test_type_filter")
        max_duration = st.slider("Max Duration (minutes):", 0, 120, 60, key="duration_filter")

        filtered_recs = valid_recs
        if selected_test_types:
            filtered_recs = [
                rec for rec in filtered_recs
                if any(t in (rec["Test Type"] if isinstance(rec["Test Type"], list) else [rec["Test Type"]]) for t in selected_test_types)
            ]
        filtered_recs = [
            rec for rec in filtered_recs
            if (
                isinstance(rec["Duration"], str) and
                re.search(r'\d+', rec["Duration"]) and
                int(re.search(r'\d+', rec["Duration"]).group()) <= max_duration
            )
        ]

        if filtered_recs:
            st.subheader("📋 Recommended SHL Assessments")
            df = pd.DataFrame(filtered_recs)
            # Configure URL column as a clickable link
            st.dataframe(
                df,
                column_config={
                    "Assessment Name": st.column_config.TextColumn("Assessment Name", width="medium"),
                    "URL": st.column_config.LinkColumn("URL", width="large"),
                    "Remote Testing Support": st.column_config.TextColumn("Remote Testing Support", width="small"),
                    "Adaptive/IRT Support": st.column_config.TextColumn("Adaptive/IRT Support", width="small"),
                    "Duration": st.column_config.TextColumn("Duration", width="small"),
                    "Test Type": st.column_config.TextColumn("Test Type", width="medium")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.warning("No assessments match the selected filters. Try adjusting the test types or duration.")
    else:
        st.warning("Recommendations received, but they are missing required fields. Please refine your input.")
elif st.session_state.raw_json:
    st.error("❌ Sorry we Could not parse valid JSON from Gemini. Try refining your job description.")

st.divider()
st.subheader("🧪 Test: SHL Product Catalog Scraping")

if st.button("Scrape SHL Product Catalog"):
    url = "https://www.shl.com/solutions/products/product-catalog/"
    scraped = extract_raw_data(url)
    if "error" in scraped:
        st.error(f"Scraping failed: {scraped['error']}")
    else:
        with st.expander("📄 Extracted Page Text"):
            st.text_area("Raw Page Text", scraped["text"][:3000])  
        with st.expander("🔗 Extracted Links"):
            st.write(scraped["links"])

st.markdown("""
    <div style="text-align: center; color: #9CA3AF; margin-top: 2rem; margin-bottom: 1rem;">
        <p>Powered by Streamlit & Gemini API</p>
        <p><a href="https://www.shl.com/solutions/products/product-catalog/" style="color: #60A5FA;">SHL Catalog</a></p>
        <p><a href="https://github.com/Swayamgupta07/GenAI---SHL-Assessment-Recommendation-System" style="color: #60A5FA;">View Code</a></p>
    </div>
""", unsafe_allow_html=True)