# multi-agent-ai-system
A multi-agent AI system that classifies and routes PDF, JSON, or Email inputs.
# 🧠 Multi-Agent AI Classifier System

This project is a lightweight, demo AI system that:

- Accepts input in JSON, Email (text), or plain text format
- Classifies input type and intent (like RFQ, Invoice, Complaint)
- Routes to correct agent (Email Agent or JSON Agent)
- Maintains a shared memory log for context and traceability

## 🚀 How to Run

You can deploy this app using **[Streamlit Cloud](https://streamlit.io/cloud)**:

1. Upload this repo to GitHub
2. Deploy with Streamlit
3. Main file: `app.py`

## 📂 Agents Involved

- **Classifier Agent**: Detects format and intent
- **JSON Agent**: Extracts from structured JSON
- **Email Agent**: Extracts sender and subject info
- **Shared Memory**: Stores logs in session state

## 🛠 Tech Stack

- Python
- Streamlit
- Google Colab (for development)
- GitHub (for deployment)

## 🧪 Sample Inputs

Try input like:

```json
{
  "invoice_id": "12345",
  "amount": 2500,
  "date": "2025-05-01"
}
