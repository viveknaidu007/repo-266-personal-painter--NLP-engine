# repo-266-personal-painter--NLP-engine

---

```markdown

A web application featuring a chat-based painting generator and a natural language search engine for images/collections.

- **Personal Painter**: Chat with the AI about emotions/themes to generate hyperpersonalized painting prompts and 3 image options using Gemini LLM.
- **Search Engine**: Search existing images/collections by describing them in natural language, ranked by keyword convergence.

Built with FastAPI (backend) and React + Vite (frontend).

## Project Structure
```
personal-painter/
├── backend/         # FastAPI backend
│   ├── app/        # Core app logic
│   ├── .env        # Environment variables (Gemini API key)
│   └── requirements.txt
├── frontend/        # React + Vite frontend
│   ├── src/        # React components and styles
│   └── package.json
└── README.md
```

## Prerequisites
- Python 3.8+
- Node.js 18+
- Gemini API key (add to `backend/.env`)

## Setup

### Backend
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` file in `backend/`:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
5. Run the backend:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the frontend:
   ```bash
   npm run dev
   ```
4. Open `http://localhost:5173` in your browser.

**Note**: Start the backend before the frontend to avoid proxy errors.

## Usage

### Personal Painter
- **Chat**: Enter messages (e.g., "I feel regret over a lost friend") in the chat window.
- **Output**: See a generated prompt and 3 simulated image IDs.
- **Reset**: Click "Reset" to clear the conversation.

### Search Engine
- **Search**: Type a query (e.g., "someone on a mountain with the Milky Way").
- **Toggle**: Switch between "Individual Images" (20 results) and "Collections" (5 results).
- **Output**: View ranked results based on keyword convergence.

## API Endpoints
- **Chat**: `POST /api/chat` - Send a message, get a prompt and images.
- **Reset Chat**: `GET /api/chat/reset-chat` - Clear conversation.
- **Search**: `POST /api/search` - Query images/collections.

## Notes
- **Image Generation**: Simulated. Replace with a real API (e.g., Stable Diffusion) in `backend/app/services/painter.py`.
- **Data**: Simulated in `backend/app/data/images.json`. Use a database for production.
- **LLM**: Uses Gemini. Swap with an open-source model (e.g., Hugging Face) if needed.

## Troubleshooting
- **ECONNREFUSED**: Ensure backend is running on `http://localhost:8000` before starting frontend.
- **Port Conflict**: Change port in `uvicorn` command and update `vite.config.js` proxy if needed.

```

---
