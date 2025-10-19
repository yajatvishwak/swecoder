# Swecoder 🚀

A spaced-repetition system for tracking and revisiting LeetCode problems. Keep your coding skills sharp by systematically reviewing problems at optimal intervals.

> ⚠️ **Work in Progress** - This project is under active development

## Features

- 📊 **Activity Heatmap** - Visual tracking of your daily problem-solving activity
- 🔄 **Spaced Repetition** - Smart revision scheduling based on difficulty and time intervals
- 📝 **Code Submission Tracking** - Store and track all your solutions
- 🎯 **Daily Revision Queue** - See which problems need review today
- 🔐 **User Authentication** - Secure signup/login with JWT tokens
- 📈 **Progress Tracking** - Monitor attempts and solve dates for all problems

## Tech Stack

**Backend:** FastAPI, SQLModel, SQLAlchemy, SQLite  
**Frontend:** SvelteKit, TailwindCSS, DaisyUI

## Setup

### Backend

```bash
cd backend

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload
```

API will be available at `http://127.0.0.1:8000`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

App will be available at `http://localhost:5173`

## How It Works

1. **Submit Solutions** - After solving a LeetCode problem, submit your code and the problem slug
2. **Smart Scheduling** - The system schedules revisions using spaced repetition (stage-based intervals)
3. **Daily Revisions** - Check your dashboard for problems due today
4. **Track Progress** - View your activity heatmap and solved questions history
5. **Rate Difficulty** - When revisiting, rate how difficult it was to adjust future intervals

## Environment Variables

Create a `.env` file in the backend directory:

```
APP_NAME=Swecoder
DEBUG=True
SQLITE_DB_FILE=./app.db
SECRET_KEY=your-secret-key-here
```

## API Endpoints

- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/submissions` - Submit a problem solution
- `GET /api/v1/revisions` - Get today's revision queue
- `GET /api/v1/activity` - Get activity heatmap data

---

Built with ❤️ for consistent coding practice

