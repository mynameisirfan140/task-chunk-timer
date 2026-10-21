# Task Chunk Timer

A web app that **auto‑breaks a task into bite‑size sub‑tasks** and runs a **Pomodoro timer** with a clear list for each work interval.  
It combines the classic Pomodoro technique with task decomposition, helping you focus on small, manageable pieces of work.

## Features
- **Auto‑break** a task into subtasks (manual definition only)  
- **Pomodoro timer** with configurable interval control  
- **Progress tracking** for each work interval  

## Architecture
- **Frontend**: React (Vite)  
- **Backend**: Python FastAPI  
- **Database**: PostgreSQL  
- **Tests**: Pytest (backend) & Jest (frontend)  

## Prerequisites
- Python 3.9+  
- Node.js 18+ (for frontend)  
- Docker (optional, for containerized setup)  

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/task-chunk-timer.git
cd task-chunk-timer
```

### 2. Create environment files
Copy the example files and fill in your values:

```bash
cp .env.example .env
# edit .env with your own values
```

### 3. Backend dependencies
Create a virtual environment and install Python packages:

```bash
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Database
Make sure PostgreSQL is running and the `DATABASE_URL` in `.env` points to it.  
Run the Alembic migration to create tables:

```bash
alembic upgrade head
```

### 5. Start the backend
```bash
uvicorn backend.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 6. Frontend setup
```bash
cd frontend
npm install
npm run dev
```
The React app runs on `http://localhost:5173` by default.

## Usage Examples

### Creating a task with subtasks
```bash
curl -X POST "http://127.0.0.1:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Write report",
        "total_duration": 1800,
        "subtasks": [
            {"title": "Outline sections", "duration": 600},
            {"title": "Write introduction", "duration": 600},
            {"title": "Write conclusion", "duration": 600}
        ]
      }'
```

### Starting a Pomodoro timer for a subtask
```bash
curl -X POST "http://127.0.0.1:8000/timers/start/" \
  -H "Content-Type: application/json" \
  -d '{"subtask_id": 3, "work_interval": 25, "break_interval": 5}'
```

### Checking progress
```bash
curl "http://127.0.0.1:8000/tasks/1"
```
Response includes the list of subtasks with their `completed_at` timestamps, letting you see how much work has been done.

## Built by

**Irfan N** — [@mynameisirfan93](https://www.instagram.com/mynameisirfan93/)

From **Tekzbyte**