# 🤖 AWS Architect Assistant (Premium)

A state-of-the-art AI-powered assistant designed to help you prepare for the **AWS Solutions Architect Associate (SAA-C03) Exam**. 

Experience a seamless, hands-free cloud architecture learning environment with **Notion integration** and a premium **Neon Cyberpunk** interface.

---

## ✨ Key Features

### 🎨 Stunning Visual Experience
- **Neon Cyberpunk Glassmorphism**: High-end UI with glowing gradients and blurred glass panels.
- **Dynamic Themes**: Seamless toggle between sleek Neon Dark mode and crisp Pastel Light mode.

### 🎤 Advanced Interactivity
- **Hands-Free (Hot-Mic)**: The AI automatically listens for your next question immediately after it finishes speaking its response.
- **Real-Time Transcription**: Watch your voice transcribe into text live in the input field.
- **Smart Interruption**: Ask a new question at any time to immediately stop the current reading.
- **Full TTS (Text-to-Speech)**: Assistant answers are read aloud with high clarity.

### 📂 Productivity & Integration
- **Direct Notion Sync**: Every Q&A pair is automatically formatted and saved to your workspace for high-retention study.
- **Intelligent Sidebar**: Keep track of recent queries with full-text tooltips on hover.
- **One-Click Deletion**: Remove unwanted notes from Notion directly from the Sidebar.
- **One-Click Clear**: Instantly reset your current chat environment.

---

## 🛠️ Technology Stack

- **Frontend**: Vanilla JavaScript + Premium CSS3 Glassmorphism
- **Backend**: FastAPI (Python)
- **AI Engine**: OpenAI GPT-4o / GPT-3.5
- **Knowledge Base**: Notion API
- **Voice Engine**: Web Speech API (Recognition & Synthesis)

---

## 🚀 Quick Start (Local Setup)

1. **Prerequisites**:
   - Python 3.10+
   - OpenAI API Key
   - Notion API Key & Page ID

2. **Configuration**:
   Copy `.env.example` to `.env` and add your credentials:
   ```env
   OPENAI_API_KEY=your_key
   NOTION_API_KEY=your_key
   NOTION_PAGE_ID=your_page_id
   ```

3. **Run the App**:
   The easiest way to start both servers is using our automated scripts:
   
   **Windows (PowerShell/CMD):**
   ```cmd
   ./run_app.bat
   ```
   
   **Bash/Git Bash:**
   ```bash
   ./run_app.sh
   ```

---

## 🏗️ Architecture

- **`frontend/`**: contains `index.html` and the premium CSS logic.
- **`backend/`**: contains the FastAPI logic (`main.py`) and clients for OpenAI/Notion.
- **`run_app.bat`/`.sh`**: handle the environment activation and port management (Backend: 8000, Frontend: 3000).

---

## 📜 Git Workflow
The project follows a feature-branch workflow. All premium UI changes were developed in a `feature/ui-overhaul` branch and merged into `main` for production stability.

---

## Webapp image
<img width="1915" height="1062" alt="image" src="https://github.com/user-attachments/assets/4685f8eb-8d15-49fc-91d5-1af6bbe44809" />


## 🤝 Contributing
Contributions are welcome! Feel free to push issues or create pull requests for new exam preparation features.
