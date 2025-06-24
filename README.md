# 🚂 LangGraph ID Processor

This project is a LangGraph-based conversational multi-agent workflow designed to collect, track, and parse guest ID documents for a reservation. It uses OpenAI's GPT-4o model to extract structured data from image-based ID documents and sends the final results via mock email.

## 📆 Features

* LangGraph multi-agent flow
* Tracks submission of 2 guest IDs per reservation
* Parses ID documents (PNG/JPG) using OpenAI Vision API
* Extracts:

  * First Name
  * Last Name
  * Date of Birth
  * Place of Birth
* Sends guest info to a mock email address
* Configurable via `.env`

## 🧐 Tech Stack

* Python
* LangGraph
* OpenAI (GPT-4o with Vision)
* `python-dotenv`

## 📁 Project Structure

```
langgraph-id-processor/
️|
├── agents.py              # OpenAI parsing and input detection
├── main.py                # LangGraph runtime and CLI simulation
├── reservation_mock.py    # Fake DB and mock email sender
├── state.py               # Shared ConversationState class
├── .env                   # Your secrets (not committed)
├── .env.example           # Template for env setup
├── requirements.txt
└── mock_ids/
    ├── id_1.png
    └── id_2.png
```

## ⚙️ Setup

### 1. Clone the Repo

```bash
git clone https://github.com/gerardo-peraltac/langgraph-id-processor.git
cd langgraph-id-processor
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` and fill in your own keys:

```bash
cp .env.example .env
```

`.env` should contain:

```
OPENAI_API_KEY=your-openai-key
EMAIL_TO=host@example.com
```

### 4. Run the Processor

```bash
python main.py
```

## 📝 Notes

* This project simulates file input via hardcoded mock ID images.
* Email sending is mocked with console output.
* OCR is skipped in favor of direct image-to-GPT-4o processing.

---

## 🔒 Security

Make sure `.env` is in your `.gitignore` and **never commit API keys**.

---

## 🧪 Example Output

```
Hi! Please upload ID documents for both guests (2 total).

[USER] ./mock_ids/id_1.png
Document received: ./mock_ids/id_1.png

[USER] ./mock_ids/id_2.png
Document received: ./mock_ids/id_2.png

[MOCK EMAIL SENT TO: host@example.com]
Guest 1:
  first_name: Jane
  last_name: Doe
  dob: 1985-06-15
  pob: Texas

Guest 2:
  first_name: John
  last_name: Smith
  dob: 1990-03-22
  pob: New York
```

---

## 📬 Contact

Created by [Gerardo Peralta](https://github.com/gerardo-peraltac) — feel free to fork and adapt.
