
📘 README.md – SHL Assessment Recommender
markdown
Copy
Edit
# 🧠 SHL Assessment Recommender (Generative AI Task)

A smart, AI-driven SHL Assessment Recommender System built using Streamlit and Gemini Pro. This tool allows hiring managers to input job descriptions or queries in natural language and receive personalized SHL assessment recommendations within seconds.

---

## 🚀 Project Overview

Hiring managers often struggle to find the right SHL assessments for specific job roles. This project solves that problem using Google’s Gemini Pro model by:

- Accepting **natural language input** or **job description URL**
- Returning up to **10 relevant assessments** from SHL’s catalog
- Displaying essential attributes like remote support, duration, and test type

---

## 🖼️ Demo

🌐 Live App: [https://your-app-name.streamlit.app](#)  
🔗 GitHub: [https://github.com/Swayamgupta07/GenAI---SHL-Assessment-Recommendation-System](https://github.com/Swayamgupta07/GenAI---SHL-Assessment-Recommendation-System)  
🔌 API Endpoint: [https://your-api-host.com/recommend](#)

> Replace the URLs above after deployment.

---

## 💻 Features

✅ Accepts job description (as text or URL)  
✅ Integrates with Google Gemini Pro for intelligent recommendations  
✅ Validates and displays results in a clean, filterable table  
✅ Shows full JSON output for debugging  
✅ FastAPI-powered backend with health & recommendation endpoints  
✅ Fully deployable on Streamlit Cloud

---

## 📊 Example Input

```text
Looking to hire mid-level professionals who are proficient in Python, SQL, and JavaScript. Need an assessment package that can test all skills with a max duration of 60 minutes.
🧾 Output Format
Each recommendation includes:

json
Copy
Edit
{
  "Assessment Name": "Java Programming Test",
  "URL": "https://www.shl.com/...",
  "Remote Testing Support": "Yes",
  "Adaptive/IRT Support": "No",
  "Duration": "45 mins",
  "Test Type": ["Coding", "Problem Solving"]
}
📦 Tech Stack

Layer	Technology
🧠 AI Engine	Google Gemini Pro via google-generativeai
🎨 UI	Streamlit
🌐 API	FastAPI
🧰 Utilities	BeautifulSoup, Requests, dotenv
📁 Hosting	Streamlit Cloud + GitHub
🔐 Environment Variables
Create a .env file with your Gemini API key:

ini
Copy
Edit
GEMINI_API_KEY=your_actual_api_key_here
🛠️ Installation & Setup
Clone the repo:

bash
Copy
Edit
git clone https://github.com/Swayamgupta07/GenAI---SHL-Assessment-Recommendation-System.git
cd GenAI---SHL-Assessment-Recommendation-System
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run Streamlit app:

bash
Copy
Edit
streamlit run app.py
Run FastAPI (API):

bash
Copy
Edit
uvicorn api:app --reload
🧪 API Documentation
Health Check:

http
Copy
Edit
GET /health
Response: { "status": "healthy" }
Recommendations:

http
Copy
Edit
POST /recommend
{
  "query": "Hiring for a Python developer..."
}
Response:
{
  "recommended_assessments": [...]
}
🧠 Evaluation Metrics
Your recommendation system can be evaluated using:

Mean Recall@K

MAP@K (Mean Average Precision)

These measure relevance and ranking quality of your recommendations.

✍️ Author
👤 Swayam Gupta
🔗 GitHub
📧 swayam@example.com (replace with your email)

📃 License
This project is licensed under the MIT License.

🙌 Acknowledgements
Google Gemini API

SHL Product Catalog

Streamlit Community
