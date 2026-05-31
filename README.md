# 🔍 IncidentLens AI

An AI-powered data pipeline incident analyser and Confluence runbook generator.

Built by [Alekhya Bhupati](https://linkedin.com/in/alekhyabhupati) — Senior Data Engineer with experience in financial services data pipelines.

## 🔗 Live App
👉 [incidentlens-ai.streamlit.app](https://incidentlens-ai.streamlit.app)

## 💡 What It Does
Paste a pipeline incident — error log, environment, what you've already tried — and get back:

- 🔍 Root cause diagnosis with confidence level
- 🛠️ Fix steps in priority order
- ⚠️ Prevention recommendations
- 📋 Ready-to-paste Confluence runbook entry
- 💬 Follow-up chat to ask questions about your incident

## 🛠️ Built With
- Python
- Streamlit
- Anthropic Claude API (claude-haiku-4-5)

## 🚀 Run Locally
```bash
git clone https://github.com/AlekhyaBhupati/incidentlens-ai.git
cd incidentlens-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
ANTHROPIC_API_KEY=your-key-here

Then run:
```bash
streamlit run app.py
```
## 👩‍💻 Author
Alekhya Bhupati — [LinkedIn](https://linkedin.com/in/alekhyabhupati) | [GitHub](https://github.com/AlekhyaBhupati)

