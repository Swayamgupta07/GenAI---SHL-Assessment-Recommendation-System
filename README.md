
# 📘 SHL Assessment Recommender

🧠 **SHL Assessment Recommender (Generative AI Task)**  
A smart, AI-driven SHL Assessment Recommender System built using Streamlit and Google Gemini Pro. This tool enables hiring managers to input job descriptions or queries in natural language and receive personalized SHL assessment recommendations within seconds.

## 🚀 Project Overview
Hiring managers often face challenges in selecting the right SHL assessments for specific job roles. This project leverages Google’s Gemini Pro model to:

- Accept natural language input or job description URLs.
- Return up to 10 relevant assessments from SHL’s catalog.
- Display key attributes like remote support, duration, and test type.
- Provide a filterable table and raw JSON output for debugging.
- Offer a FastAPI-powered backend with `/health` and `/recommend` endpoints.

## 🖼️ Demo
🌐 **Live App**: [https://genai-shl-assessment-recommendation.streamlit.app](https://genai-shl-assessment-recommendation.streamlit.app)  
🔗 **GitHub**: [https://github.com/Swayamgupta07/GenAI---SHL-Assessment-Recommendation-System](https://github.com/Swayamgupta07/GenAI---SHL-Assessment-Recommendation-System)  
🔌 **API Endpoint**: [https://genai-shl-assessment-recommendation-ylim.onrender.com](https://genai-shl-assessment-recommendation-ylim.onrender.com)

*(Note: Update the Live App URL after deploying to Streamlit Cloud.)*

## 💻 Features
- ✅ Accepts job description input (text or URL).
- ✅ Integrates with Google Gemini Pro for intelligent recommendations.
- ✅ Displays results in a clean, filterable table.
- ✅ Provides raw JSON output for debugging.
- ✅ Includes a FastAPI backend with `/health` and `/recommend` endpoints.
- ✅ Fully deployable on Streamlit Cloud and Render.

## 📊 Example Input
**Query**:  
"Looking to hire mid-level professionals who are proficient in Python, SQL, and JavaScript. Need an assessment package that can test all skills with a max duration of 60 minutes."

## 🧾 Output Format
Each recommendation includes:  
```json
{
  "Assessment Name": "Java Programming Test",
  "URL": "https://www.shl.com/...",
  "Remote Testing Support": "Yes",
  "Adaptive/IRT Support": "No",
  "Duration": "45 mins",
  "Test Type": ["Coding", "Problem Solving"]
}
```

## 📦 Tech Stack

| Layer            | Technology                          |
|-------------------|-------------------------------------|
| 🧠 AI Engine      | Google Gemini Pro (google-generativeai) |
| 🎨 UI             | Streamlit                           |
| 🌐 API            | FastAPI                             |
| 🧰 Utilities      | BeautifulSoup, Requests, dotenv     |
| 📁 Hosting        | Streamlit Cloud + Render            |

## 🔐 Environment Variables
Create a `.env` file with your Gemini API key:  
```ini
GEMINI_API_KEY=your_actual_api_key_here
```

## 🛠️ Installation & Setup
1. **Clone the repository**:  
   ```bash
   git clone https://github.com/Swayamgupta07/GenAI---SHL-Assessment-Recommendation-System.git
   cd GenAI---SHL-Assessment-Recommendation-System
   ```
2. **Install dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Streamlit app**:  
   ```bash
   streamlit run app.py
   ```
4. **Run the FastAPI backend**:  
   ```bash
   uvicorn api:app --reload
   ```

## 🧪 API Documentation
### Health Check
- **Endpoint**: `GET /health`  
- **Response**:  
  ```json
  { "status": "healthy" }
  ```

### Recommendations
- **Endpoint**: `POST /recommend`  
- **Request Body**:  
  ```json
  {
    "query": "Hiring for a Python developer..."
  }
  ```
- **Response**:  
  ```json
  {
    "recommended_assessments": [
      {
        "Assessment_Name": "Python Skills Test",
        "URL": "https://www.shl.com/...",
        "Remote_Testing_Support": "Yes",
        "Adaptive_IRT_Support": "No",
        "Duration": 45,
        "Test_Type": ["Coding", "Problem Solving"]
      }
    ]
  }
  ```

## 🧠 Evaluation Metrics
Evaluate your recommendation system using:  
- **Mean Recall@K**: Measures the proportion of relevant items retrieved.  
- **MAP@K (Mean Average Precision)**: Assesses relevance and ranking quality of recommendations.

## ✍️ Author
- 👤 **Swayam Gupta**  
- 🔗 [GitHub](https://github.com/Swayamgupta07)  
- 📧 [swayam@example.com](mailto:swayam@example.com) *(Replace with your email)*

## 📃 License
This project is licensed under the [MIT License](LICENSE).

## 🙌 Acknowledgements
- Google Gemini API  
- SHL Product Catalog  
- Streamlit Community  
- Render for API hosting

## 📝 Notes
1. **API Endpoint**: The endpoint `https://genai-shl-assessment-recommendation-ylim.onrender.com` is used. Ensure it is correct and accessible.
2. **Live App URL**: Replace the placeholder `https://genai-shl-assessment-recommendation.streamlit.app` with your actual Streamlit Cloud deployment URL after deployment.
3. **Requirements.txt**: The current `requirements.txt` lacks version pins. Update it for reproducibility:  
   ```
   streamlit==1.24.0
   pandas==2.0.3
   requests==2.31.0
   beautifulsoup4==4.12.2
   google-generativeai==0.3.2
   python-dotenv==1.0.0
   fastapi==0.68.0
   uvicorn==0.15.0
   ```
4. **Code Consistency**: Ensure `app.py` and `api.py` align with the latest versions, including fixes (e.g., PyArrow error handling).
5. **Deployment**: Test and update URLs after deploying to Streamlit Cloud and Render.

## 🚀 Next Steps
- Copy this markdown into your `README.md`.
- Commit and push changes:  
  ```bash
  git add README.md
  git commit -m "Beautify and update README with new details"
  git push origin main
  ```
- Deploy the app to Streamlit Cloud and API to Render, then update the Live App URL.
- Test the app and API, and report any issues for further adjustments.
```

### Improvements Made
1. **Formatting**: Fixed inconsistent markdown syntax (e.g., tables, code blocks, headings) and ensured proper indentation.
2. **Structure**: Reorganized sections for better flow (e.g., moved "Notes" to the end, completed the "License" section).
3. **Consistency**: Aligned the content with your provided `app.py`, `api.py`, and `requirements.txt`, including the new API endpoint.
4. **Clarity**: Added bullet points for features and next steps, and completed incomplete sections (e.g., "Acknowledgements").
5. **Professionalism**: Enhanced readability with consistent styling and added a "Next Steps" section for guidance.

### Next Steps
- Copy the above content into your `README.md` file.
- Update the `requirements.txt` with the suggested versioned dependencies.
- Follow the commit and push instructions.
- Deploy and test the app/API, then update the Live App URL.
- Let me know if you need further refinements or help with deployment!

This version is now polished and ready for use. Let me know how it works or if you’d like additional changes!
