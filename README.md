# ExamEcho
ExamEcho is your AI-powered study companion that makes exam preparation effortless. Ask any question by typing or speaking, get a clear and concise answer echoed back to you in real time, and have every Q&A automatically saved to Notion — building your personal knowledge base as you study. Whether you're tackling certifications, competitive exams, or university finals, ExamEcho ensures every answer you hear is one you can always come back to.
# AWS Question Answerer 🤖

I made it for my AWS, we can make this as any exam notes taker
A web app that answers AWS Solutions Architect questions using **OpenAI** and automatically syncs every Q&A to **Notion**.

## Features ✨

- 🎤 **Voice input** — ask questions by speaking
- ⌨️ **Text input** — type questions manually
- 🧠 **OpenAI-powered** — AWS exam-style tutor responses
- 📝 **Notion sync** — automatically append answers to your page
- 🔊 **Text-to-speech** — answers read aloud in-browser
- ⚡ **Live health status** — checks OpenAI + Notion connectivity

---

## Prerequisites

- **Python 3.9+**
- **OpenAI API key**
- **Notion integration token** and **Notion page ID**

---

## Quick Start

### 1. Activate the Python environment
If the included `myenv` already exists:

```powershell
myenv\Scripts\Activate.ps1
```

Or create a fresh environment:

```powershell
python -m venv myenv
myenv\Scripts\Activate.ps1
```

### 2. Install backend dependencies

```powershell
cd backend
pip install -r requirements.txt
```

### 3. Copy environment template

```powershell
copy ..\.env.example ..\.env
```

Then edit `.env` and fill in your credentials:

```env
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-3.5-turbo
NOTION_API_KEY=ntn-your-notion-key
NOTION_PAGE_ID=your-notion-page-id
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=true
```

### 4. Start the backend

```powershell
cd backend
python main.py
```

The backend will start on `http://0.0.0.0:8000`.

### 5. Open the frontend

Open `frontend/index.html` in your browser.

Alternatively, serve it locally from the project root:

```powershell
python -m http.server 5500 --directory frontend
```

Then open:

```text
http://localhost:5500
```

---

## How to Use

1. Confirm the health status in the UI
2. Ask an AWS question by typing or speaking
3. Wait for the assistant answer
4. Verify the Q&A entry in your Notion page

---

## Model Recommendation

Use `gpt-3.5-turbo` for fast AWS question answering.

To switch models, update `OPENAI_MODEL` in `.env` and restart the backend.

---

## Troubleshooting

### OpenAI fails
- Confirm `OPENAI_API_KEY` is correct
- Use the OpenAI secret key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Restart the backend after editing `.env`

### Notion sync fails
- Confirm `NOTION_API_KEY` is valid
- Confirm the integration is shared with the target page
- Confirm `NOTION_PAGE_ID` is correct
- Run `python backend/test_notion.py`

### Microphone or speech issues
- Use Chrome, Edge, Firefox, or Safari
- Allow microphone access in the browser
- The Web Speech API is required for voice input

---

## Project Structure

```text
OpenaiChat to Notion app/
├── backend/
│   ├── main.py
│   ├── openai_client.py
│   ├── notion_client.py
│   ├── requirements.txt
│   └── test_notion.py
├── frontend/
│   └── index.html
├── .env
├── .env.example
└── README.md
```

---

## Architecture

```
[Browser UI] → [FastAPI Backend] → [OpenAI API]
                              ↘ [Notion API]
```

### Request flow
1. User sends a question from the frontend
2. Backend calls OpenAI for an AWS answer
3. Backend writes the Q&A pair to Notion
4. Frontend displays and speaks the answer

---

## API Endpoints

### `POST /ask`
Send a question and receive an answer with Notion sync.

**Request body:**

```json
{
  "question": "What is AWS S3?"
}
```

**Response:**

```json
{
  "question": "What is AWS S3?",
  "answer": "AWS S3 is...",
  "added_to_notion": true,
  "message": "Done ✓ Added to Notion"
}
```

### `GET /health`
Check service connectivity.

**Response:**

```json
{
  "status": "ok",
  "openai": "connected",
  "notion": "connected"
}
```

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI secret key | `sk-abc123...` |
| `OPENAI_MODEL` | Model to use | `gpt-3.5-turbo` |
| `NOTION_API_KEY` | Notion integration token | `ntn_abc123...` |
| `NOTION_PAGE_ID` | Notion page ID | `3333c1cd-5e9c-...` |
| `SERVER_HOST` | Backend host | `0.0.0.0` |
| `SERVER_PORT` | Backend port | `8000` |

---

## Notes

- Do not commit `.env`
- The app is tuned for AWS Solutions Architect exam style questions
- The frontend communicates with the backend at `http://localhost:8000`
  
---

## Questions or Issues?

- First check the Troubleshooting section
- Run `python backend/test_notion.py` for Notion diagnostics
- Confirm your `.env` values are correct

Webapp Images
<img width="1910" height="983" alt="image" src="https://github.com/user-attachments/assets/69bb4e2a-bce1-4e9e-88d3-5bf322d200cd" />

Enjoy! 🎉
