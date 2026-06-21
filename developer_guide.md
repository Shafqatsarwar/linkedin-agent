# LinkedIn Manager Agent — Complete Developer Guide
`python app.py`
## ⚡ QUICK START (5 minutes to posting)

### Step 1: Prerequisites
```bash
# Check Python version (3.8+)
python --version

# Verify dependencies installed
pip list | findstr python-dotenv
```
```bash
cd D:\Panaverse\linkedin-agent
python app.py
```
### Setup (Windows & Mac/Linux)

```bash
# Clone repository
git clone https://github.com/Shafqatsarwar/linkedin-agent.git
cd linkedin-agent

# Install dependencies
pip install -r requirements.txt

# Verify environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ All set!') if all(os.getenv(k) for k in ['LINKEDIN_CLIENT_ID','LINKEDIN_CLIENT_SECRET','GEMINI_API_KEY']) else print('❌ Missing env vars')"

# Run the agent
python app.py
```
### Step 2: Use It
- Open: http://localhost:8000
- Click **"Continue with LinkedIn"**
- Approve permissions
- Enter a topic → AI drafts → You approve → **Posted! 🚀**

---

### Step 3: Get Gemini API Key
1. Go to: https://ai.google.dev
2. Click **"Get API Key"** → **"Create API Key"**
3. Copy the key

### Step 4: Create .env file
```dotenv
LINKEDIN_CLIENT_ID=your_id_here
LINKEDIN_CLIENT_SECRET=your_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8000/callback
GEMINI_API_KEY=your_gemini_key_here
SECRET_KEY=your-random-secret-key
PORT=8000
```
### Step 5: Configure LinkedIn OAuth
1. Go to: https://www.linkedin.com/developers/apps
2. Select your app
3. Click **Auth** tab
4. Add to **Authorized redirect URLs**: `http://localhost:8000/callback`
5. Copy `LINKEDIN_CLIENT_ID` and `LINKEDIN_CLIENT_SECRET`

### ✅ What's Verified & Working

| Component | Status | Test Result |
|-----------|--------|-------------|
| Environment Variables | ✅ | All credentials loaded from `.env` |
| Python Syntax | ✅ | `app.py` compiles without errors |
| Server Startup | ✅ | Runs on `http://localhost:8000` |
| OAuth Flow | ✅ | Correctly redirects to LinkedIn OAuth |
| Gemini Integration | ✅ | API key loaded and ready |
| Frontend Dashboard | ✅ | Beautiful UI renders correctly |
| Error Handling | ✅ | Validates missing env vars at startup |
| CORS Security | ✅ | Properly configured origin restrictions |

### Project Structure
```
linkedin-agent/
├── app.py                    # Python backend (OAuth + LinkedIn API + Gemini)
├── index.html                # Dashboard UI (vanilla JS)
├── requirements.txt          # Dependencies
├── render.yaml               # Cloud deployment config
├── .env                      # Your secrets (in .gitignore)
├── .env.example              # Template for setup
├── developer_guide.md        # Full documentation
├── post-copy.md              # Ready-to-post content
└── project_visual.html       # Architecture visualization
```


**Output when running:**
```
╔══════════════════════════════════════════════╗
║     LinkedIn Manager Agent is running!       ║
║                                              ║
║  Open: http://localhost:8000                 ║
║  Login with your LinkedIn account            ║
║  Press Ctrl+C to stop                        ║
╚══════════════════════════════════════════════╝
```

Open browser to: `http://localhost:8000`

### Workflow: Topic → Draft → Approve → Published ✅

1. **Login** → Click "Continue with LinkedIn" → Grant permissions
2. **Draft** → Enter topic → Gemini generates post
3. **Review** → Edit if needed → Click buttons to regenerate
4. **Approve** → One-click publish → **Goes live on LinkedIn!**

---

### Common Commands (Quick Reference)

```bash
# 🚀 Run the agent
python app.py

# ✓ Check syntax before running
python -m py_compile app.py && echo "✓ Syntax OK"

# 📋 Verify all credentials loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); [print(f'{k}: {\"✓\" if os.getenv(k) else \"✗\"}') for k in ['LINKEDIN_CLIENT_ID','LINKEDIN_CLIENT_SECRET','GEMINI_API_KEY']]"

# 🔍 View git configuration
git config user.name
git config user.email

# 🔧 Set git identity (first time setup)
git config --global user.name "Shafqatsarwar"
git config --global user.email "khansarwar1@hotmail.com"

# 📤 Push to GitHub
git add .
git commit -m "LinkedIn Manager Agent - production ready"
git push -u origin main

# ⛔ Kill running server (Windows)
taskkill /IM python.exe /F

# ⛔ Kill port 8000 if busy (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# 📱 Check if server is running
curl http://localhost:8000/api/me
```

### ✅ Production Checklist

- [x] Python 3.8+ installed
- [x] Dependencies installed (`pip install -r requirements.txt`)
- [x] `.env` file configured with all 4 keys
- [x] OAuth redirect URI added to LinkedIn app settings
- [x] Server starts without errors (`python app.py`)
- [x] Frontend loads at `http://localhost:8000`
- [x] OAuth flow works (redirects to LinkedIn)
- [x] Gemini API key validated

### Deployment to Render (Optional - Free Cloud Hosting)

```bash
# 1. Push to GitHub
git push -u origin main

# 2. Go to render.com → New Web Service → Connect GitHub repo

# 3. Render automatically reads render.yaml:
#    - Runtime: Python 3
#    - Build: pip install -r requirements.txt
#    - Start: python app.py

# 4. Add environment variables in Render dashboard:
#    - LINKEDIN_CLIENT_ID
#    - LINKEDIN_CLIENT_SECRET
#    - GEMINI_API_KEY
#    - LINKEDIN_REDIRECT_URI=https://your-app.onrender.com/callback

# 5. Update LinkedIn app settings:
#    - Add new Redirect URI: https://your-app.onrender.com/callback
#    - Update LINKEDIN_REDIRECT_URI in Render env vars
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

---

## Publishing to GitHub (Share Your Work)

```bash
# Initialize git if not already done
git init

# staging all files
git add app.py index.html requirements.txt render.yaml .gitignore .env.example

# Commit with meaningful message
git commit -m "LinkedIn Manager Agent - Production ready with OAuth + Gemini"

# Set main branch
git branch -M main

# Add remote (if not already added)
git remote add origin https://github.com/Shafqatsarwar/linkedin-agent.git

# Push to GitHub
git push -u origin main
```

**Note:** `.env` is automatically excluded by `.gitignore`—never commit secrets!

---

## API Endpoints Reference

| Method | Endpoint | Authentication | Purpose |
|--------|----------|-----------------|---------|
| GET | `/` | None | Dashboard UI |
| GET | `/login` | None | Start OAuth flow |
| GET | `/callback` | None | OAuth return endpoint |
| GET | `/api/me` | Session (Cookie) | Get current user |
| GET | `/api/pending` | Session | Get pending posts |
| POST | `/api/draft` | Session | Generate AI draft |
| POST | `/api/approve` | Session | Publish to LinkedIn |
| POST | `/api/reject` | Session | Discard draft |
| POST | `/api/regenerate` | Session | Regenerate variant |
| POST | `/api/improve-profile` | Session | Enhance profile section |
| GET | `/logout` | Session | Clear session |

---

## Troubleshooting Guide

### Problem: ModuleNotFoundError: dotenv
**Solution:** Install python-dotenv
```bash
pip install python-dotenv
```

### Problem: Port 8000 is already in use
**Solution (Windows):**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Solution (Mac/Linux):**
```bash
lsof -ti:8000 | xargs kill -9
```

### Problem: "redirect_uri does not match"
**Solution:** Check LinkedIn Developer settings
1. Go to: https://www.linkedin.com/developers/apps
2. Click your app
3. Click **Auth** tab
4. Verify Redirect URI: `http://localhost:8000/callback` (for local)
5. Make sure it matches your `.env` LINKEDIN_REDIRECT_URI

### Problem: Gemini API returns 403 Forbidden
**Solution:** Check Gemini API key
1. Go to: https://ai.google.dev
2. Verify the API key is valid
3. Check that it's enabled for "Generative Language API"
4. Update `.env` with new key if expired

### Problem: OAuth login fails silently
**Solution:** Check browser console
1. Open DevTools (F12)
2. Go to **Console** tab
3. Look for error messages
4. Common causes:
   - `.env` file not loaded (restart server)
   - Invalid Client ID/Secret
   - Redirect URI mismatch

### Problem: "Cannot read properties of null (reading 'textContent')"
**Solution:** This is LinkedIn's JavaScript error, not ours. Clear browser cache and try again.

---

## File Descriptions

| File | Purpose |
|------|---------|
| **app.py** | Main backend server - handles OAuth, API, Gemini calls |
| **index.html** | Dashboard UI - forms, buttons, real-time updates |
| **requirements.txt** | Pip dependencies (just python-dotenv) |
| **render.yaml** | Cloud deployment config for Render.com |
| **.env** | Your secrets - NEVER commit this |
| **.env.example** | Template showing what variables to set |
| **.gitignore** | Excludes .env and common Python files |
| **developer_guide.md** | This file - full documentation |
| **post-copy.md** | Ready-to-use post text versions |
| **project_visual.html** | Beautiful visualization of architecture |

---

## Tech Stack Breakdown

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3 HTTP server | Lightweight, no external dependencies |
| **Authentication** | LinkedIn OAuth 2.0 | Secure, user-approved access |
| **AI Engine** | Google Gemini 2.5 Flash | Fast, accurate content generation |
| **Frontend** | Vanilla HTML/CSS/JS | No build step, runs anywhere |
| **Storage** | In-memory sessions | Stateless (session lost on restart) |
| **Deployment** | Render (optional) | Free tier, auto-deploys from GitHub |

---

## Performance & Optimization Tips

1. **Faster Gemini responses:** Keep topics concise (< 100 chars)
2. **Better drafts:** Include tone preference (professional, casual, humorous)
3. **Local testing:** Use `python app.py` first before deploying
4. **Batch operations:** Draft multiple posts, then approve one-by-one
5. **Caching:** Gemini responses are NOT cached (each call costs quota)

---

## Next Steps & Future Enhancements

### Immediate (This Week)
- ✅ Post inaugural article to LinkedIn (Version 1 text ready)
- ✅ Gather feedback from first users
- ✅ Monitor Gemini quota usage
- [ ] Create video walkthrough

### Short-term (This Month)
- [ ] Add post scheduling (publish at optimal times)
- [ ] Batch upload multiple topics
- [ ] Analytics dashboard (track post performance)
- [ ] Rate limiting to prevent API abuse

### Medium-term (This Quarter)
- [ ] LinkedIn profile auto-optimizer (headline, about, experience)
- [ ] Multi-account support
- [ ] Tone/style customization templates
- [ ] Export analytics reports to email
- [ ] Integration with other social platforms (Twitter, Medium)

### Long-term (Vision)
- [ ] Machine learning for personal writing style matching
- [ ] Sentiment analysis on LinkedIn comments
- [ ] Competitor content analysis
- [ ] AI-powered hashtag recommendations
- [ ] Mobile app (iOS/Android)
- [ ] Team collaboration (shared drafts, approvals)

---

## Contributing & Feedback

Have an idea? Found a bug? Want to contribute?

1. **Open an Issue:** https://github.com/Shafqatsarwar/linkedin-agent/issues
2. **Submit a PR:** Fork → Branch → Commit → Push → PR
3. **Provide Feedback:** What would make this more useful?

---

## License & Credits

**Built by:** [@Shafqatsarwar](https://github.com/Shafqatsarwar) — Agentic AI Developer  
**AI Engine:** Google Gemini 2.5 Flash  
**OAuth:** LinkedIn OAuth 2.0  
**Deployment:** Render.com  

**Open Source:** MIT License — Use freely, attribute appreciated.

---

## Quick Links

- 🔗 **GitHub:** https://github.com/Shafqatsarwar/linkedin-agent
- 📄 **LinkedIn:** https://www.linkedin.com/in/shafqatsarwar
- 🚀 **Live App:** http://localhost:8000 (run `python app.py`)
- 📚 **Documentation:** This file
- 💡 **Post Copy:** See `post-copy.md`
- 🎨 **Project Visualization:** See `project_visual.html`

---

**Questions? Issues? Ideas?** Open an issue on GitHub or connect on LinkedIn!

Last Updated: June 19, 2026
