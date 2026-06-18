# LinkedIn Manager Agent — Developer Guide (2 Versions)

You have **two separate working versions** of this agent. Use whichever fits the moment.

| | Laptop version | Claude.ai version |
|---|---|---|
| Where it runs | Your computer (`python3 app.py`) | Inside Claude.ai chat as an artifact |
| AI engine | Gemini 2.5 Flash (your own quota) | Gemini 2.5 Flash (called directly, still your quota) |
| Auto-publish to LinkedIn | ✅ Yes — real OAuth + API | ❌ No — copy/paste manually |
| LinkedIn login | ✅ Yes | ❌ No |
| Profile improver | ✅ Yes | ❌ No |
| Needs install | Python 3 | Nothing — just open Claude.ai |
| Best for | Daily real publishing | Quick drafts on the go, testing ideas |

---

## VERSION 1 — Laptop (full features, auto-publish)

### Files
```
linkedin-agent/
├── app.py               # Python backend — OAuth + LinkedIn API + Gemini
├── index.html           # Dashboard UI
├── requirements.txt     # Just python-dotenv
├── render.yaml          # Optional — for free cloud hosting later
├── .env                 # Your secrets (never committed)
└── .gitignore           # Excludes .env
```

### Setup

```bash
git clone https://github.com/Shafqatsarwar/linkedin.git
cd linkedin
pip install -r requirements.txt
python3 app.py
```

Open: `http://localhost:8000` → Login with LinkedIn → Draft → Approve → Published.

### Pre-flight test (run before first use)

```bash
python3 -c "
from dotenv import load_dotenv; import os; load_dotenv()
keys = ['LINKEDIN_CLIENT_ID','LINKEDIN_CLIENT_SECRET','GEMINI_API_KEY','LINKEDIN_REDIRECT_URI']
[print('PASS' if os.getenv(k) else 'FAIL', k) for k in keys]
"
```

All should print `PASS`.

### Test results (already verified)

```
PASS   Environment Variables
PASS   app.py Syntax
PASS   PORT env support
PASS   All files present
ALL PASS
```

### Optional — deploy to Render later (always-on URL, still free)

```bash
# 1. Push to GitHub first (see below)
# 2. Go to render.com → New Web Service → connect your repo
# 3. Render reads render.yaml automatically
# 4. Add your env vars in Render dashboard (Client ID, Secret, Gemini key)
# 5. Add the new Render URL + /callback to your LinkedIn app's redirect URIs
```

---

## VERSION 2 — Claude.ai artifact (no install, draft-only)

### How to use it

1. Open any conversation with Claude
2. Ask: *"Build me the LinkedIn post drafter artifact with Gemini"*
3. The widget renders inline in chat
4. Click **Generate draft** → review → edit → click **Approve** (copies to clipboard)
5. Paste manually into LinkedIn and publish

### Why this version can't auto-publish

Claude.ai's sandbox can make simple outbound API calls (like to Gemini),
but cannot hold a persistent OAuth session with LinkedIn or run a background
server. That's why drafting works but publishing is manual copy-paste here.

### When to use which

- **Quick idea while chatting with Claude** → use the Claude artifact, copy-paste the result
- **Daily real publishing workflow** → use the laptop version, fully automated approve→publish

---

## Full Command Reference (Laptop version)

```bash
# Setup
git clone https://github.com/Shafqatsarwar/linkedin.git
cd linkedin
pip install -r requirements.txt

# Run
python3 app.py

# Test syntax
python3 -m py_compile app.py && echo "Syntax OK"

# Test env vars
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); [print('PASS' if os.getenv(k) else 'FAIL', k) for k in ['LINKEDIN_CLIENT_ID','LINKEDIN_CLIENT_SECRET','GEMINI_API_KEY']]"

# Kill server if port busy (Mac/Linux)
lsof -ti:8000 | xargs kill -9

# Kill server if port busy (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## Publishing to GitHub

```bash
git init
git add app.py index.html requirements.txt render.yaml .gitignore developer_guide.md
git commit -m "LinkedIn Manager Agent — laptop + Claude versions"
git branch -M main
git remote add origin https://github.com/Shafqatsarwar/linkedin.git
git push -u origin main
```

> `.env` stays local — excluded by `.gitignore`, never pushed.

---

## API Endpoints (Laptop version only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| GET | `/login` | Start LinkedIn OAuth |
| GET | `/callback` | OAuth callback |
| GET | `/api/me` | Current user |
| GET | `/api/pending` | Pending posts |
| POST | `/api/draft` | Generate draft (Gemini) |
| POST | `/api/approve` | Publish to LinkedIn |
| POST | `/api/reject` | Discard draft |
| POST | `/api/regenerate` | New draft |
| POST | `/api/improve-profile` | Improve profile section |
| GET | `/logout` | Log out |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: dotenv` | `pip install python-dotenv` |
| Port 8000 busy | `lsof -ti:8000 \| xargs kill -9` |
| LinkedIn login fails | Check `.env` Client ID/Secret |
| `redirect_uri mismatch` | Add exact URI in LinkedIn app → Auth tab |
| Claude artifact: Gemini error | Check API key still valid at aistudio.google.com |
| Want both running at once | They're independent — run laptop locally AND use Claude artifact in chat, no conflict |

---

## Tech Stack

| Layer | Laptop version | Claude version |
|-------|-----------------|------------------|
| Backend | Python 3 stdlib | None (Claude sandbox) |
| AI | Gemini 2.5 Flash | Gemini 2.5 Flash |
| Auth | LinkedIn OAuth 2.0 | None |
| Frontend | Vanilla HTML/CSS/JS | Inline SVG + HTML widget |
| Publishing | Direct API | Manual copy-paste |

---

*Built by [@Shafqatsarwar](https://github.com/Shafqatsarwar) — Agentic AI Developer*
