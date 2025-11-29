# PrepMate-AI Backend

FastAPI backend for AI-powered interview preparation platform.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Run the server**:
   ```bash
   python main.py
   ```
   Or with uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### Health Check
- `GET /health` - Basic health check
- `GET /health/ready` - Readiness check

### Interview
- `POST /api/interview/start` - Start a new interview session
- `POST /api/interview/answer` - Submit an answer and get feedback
- `GET /api/interview/summary/{session_id}` - Get interview summary

## Project Structure

```
backend/
├── main.py                     # FastAPI entrypoint
├── config.py                   # Environment & settings
├── requirements.txt
├── routers/                    # API endpoints
│   ├── interview.py
│   └── health.py
├── chains/                     # LangChain implementations
│   ├── question_chain.py
│   ├── feedback_chain.py
│   └── prompts/
├── core/                       # Business logic
│   ├── interview_manager.py
│   └── utils.py
└── models/                     # Data models
```

## Environment Variables

See `.env.example` for required configuration.
