# AI Chat Backend API

A read-only Flask backend API for AI-powered chat functionality with Firebase Firestore and Groq LLM integration.

## Features

- ✅ Read-only Firebase access (no writes)
- ✅ Personalized AI responses based on user preferences
- ✅ Conversation history context (last 10 messages)
- ✅ Support for multiple chat sessions per user
- ✅ Groq API integration (Meta Llama 3.3 70B)
- ✅ CORS enabled for web/mobile access
- ✅ Comprehensive logging
- ✅ Error handling

## Architecture

**Backend Responsibilities:**
- Read user profile from Firebase
- Read user preferences from Firebase
- Read last 10 messages from chat session
- Build personalized AI prompt
- Call Groq LLM API
- Return AI response to frontend

**Frontend Responsibilities:**
- Write user data to Firebase
- Write messages to Firebase
- Update session metadata
- Display chat UI

## Firebase Schema

### Collections Used (Read-Only):

1. **users** - User profiles
   - `id`, `name`, `age`, `email`, etc.

2. **user_preferences** - Chat personalization
   - `user_id`, `conversation_tone`, `support_type`, `topics_to_avoid`, etc.

3. **messages** - Chat messages
   - `user_id`, `chat_session_id`, `message`, `type`, `timestamp`

4. **chat_sessions** - Conversation threads
   - `id`, `user_id`, `session_name`, `created_at`

## Installation

### 1. Create Virtual Environment

```bash
cd ammora_backend
python -m venv .venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
- Firebase credentials (from service account JSON)
- Groq API key

### 5. Run the Server

```bash
python app.py
```

Server will start at: `http://localhost:5001`

## API Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Chat Backend API",
  "version": "1.0.0"
}
```

### Chat Endpoint

```http
POST /api/chat
```

**Request Body:**
```json
{
  "user_id": "user123",
  "chat_session_id": "session456",
  "message": "Hello, how are you?"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "Hello! I'm doing great, thank you for asking...",
    "model": "llama-3.3-70b-versatile"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message description"
}
```

## Project Structure

```
ammora_backend/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── config/
│   └── firebase_config.py     # Firebase initialization
├── services/
│   ├── firebase_service.py    # Firebase read operations
│   ├── llm_service.py         # Groq API integration
│   └── prompt_builder.py      # AI prompt construction
└── README.md                  # This file
```

## Environment Variables

Required variables in `.env`:

```env
# Firebase
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com

# Groq
GROQ_API_KEY=your_groq_api_key_here

# Server
PORT=5001
```

## How It Works

1. **Frontend sends request** with `user_id`, `chat_session_id`, and `message`
2. **Backend reads** user profile from Firebase
3. **Backend reads** user preferences from Firebase
4. **Backend reads** last 10 messages from session
5. **Backend builds** personalized AI prompt
6. **Backend calls** Groq API with context
7. **Backend returns** AI response to frontend
8. **Frontend saves** both user message and AI response to Firebase

## Deployment

### Using Gunicorn (Production)

```bash
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Using Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
```

### Deploy to Cloud

- **Heroku**: `git push heroku main`
- **Railway**: Connect GitHub repo
- **Google Cloud Run**: `gcloud run deploy`
- **AWS Elastic Beanstalk**: `eb deploy`

## Testing

### Using curl

```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "chat_session_id": "session456",
    "message": "Hello!"
  }'
```

### Using Postman

1. Create new POST request
2. URL: `http://localhost:5001/api/chat`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "user_id": "your-user-id",
  "chat_session_id": "your-session-id",
  "message": "Test message"
}
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (missing parameters)
- `404` - Not Found (user doesn't exist)
- `500` - Server Error (Firebase/Groq API issues)

## Logging

The backend logs all operations to console:

```
📨 New chat request received
👤 User ID: user123
💬 Session ID: session456
📝 Message: Hello!
🔍 Fetching user data from Firebase...
✅ User data retrieved: John
🎨 Fetching user preferences...
✅ Preferences retrieved: Supportive Friend
📜 Fetching conversation history...
✅ Retrieved 5 messages from history
🤖 Building AI prompt...
✅ Prompt built successfully
🚀 Calling Groq API...
✅ AI response received (150 chars)
```

## Security Notes

- Backend only reads from Firebase (no write access)
- All writes handled by authenticated frontend
- Firebase security rules should restrict write access
- Consider adding API authentication for production

## License

MIT

## Support

For issues or questions, contact the development team.
