# LangGraph ID Processor

This project implements a conversational multi-agent system using **LangGraph** to collect and process guest ID documents for a 2-person reservation.

## ✅ Features
- Requests and tracks ID submissions for 2 guests
- Reminds user if documents are missing
- Parses key information (name, DOB, POB) from uploaded ID image using OpenAI
- Submits collected data to a simulated email endpoint

## 🗂️ Project Structure
```
langgraph_id_processor/
├── main.py               # LangGraph bot logic and flow
├── agents.py             # LLM-based parsing functions
├── config.py             # Constants and OpenAI key
├── reservation_mock.py   # Fake reservation and email logic
├── state.py              # State class tracking docs and data
├── mock_ids/             # Folder for fake ID image files
├── README.md             # Project overview
└── .gitignore            # Excludes venv, temp files and mock IDs
```

## 🛠️ Requirements
- Python 3.9+
- OpenAI SDK
- LangGraph

Install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## 🔐 Setup
Create a `.env` or manually configure `OPENAI_API_KEY` in `config.py`.

## 🚀 Run
```bash
python main.py
```

## 📩 Output
You’ll see messages prompting for document uploads and the final guest data printed as a mock email.

## 📌 Note
For image parsing, you can extend `parse_id_document_with_llm()` to perform OCR with Tesseract or Google Vision and feed the text to OpenAI.
