"""
LinkedIn Manager Agent - Python Backend
Human-in-the-Loop AI Assistant powered by Gemini 2.5 Flash
"""

import os
import json
import secrets
import urllib.parse
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
CLIENT_ID       = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET   = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI    = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000/callback")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY")
SECRET_KEY      = os.getenv("SECRET_KEY", "dev-secret")
PORT            = int(os.getenv("PORT", 8000))  # Render sets PORT automatically

# Validate required environment variables
def validate_env():
    missing = []
    if not CLIENT_ID:
        missing.append("LINKEDIN_CLIENT_ID")
    if not CLIENT_SECRET:
        missing.append("LINKEDIN_CLIENT_SECRET")
    if not GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")
    if missing:
        print(f"❌ ERROR: Missing required environment variables: {', '.join(missing)}")
        print("   Create a .env file in the project root with these keys.")
        exit(1)

LINKEDIN_AUTH_URL  = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_API_BASE  = "https://api.linkedin.com/v2"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

# In-memory session store (use Redis/DB in production)
sessions = {}
pending_posts = {}  # posts awaiting human approval

# ── LinkedIn OAuth helpers ─────────────────────────────────────────────────────
def get_auth_url(state):
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": "openid profile email w_member_social"
    }
    return f"{LINKEDIN_AUTH_URL}?{urllib.parse.urlencode(params)}"

def exchange_code_for_token(code):
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }).encode()
    req = urllib.request.Request(LINKEDIN_TOKEN_URL, data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()}

def get_linkedin_profile(access_token):
    req = urllib.request.Request(
        f"{LINKEDIN_API_BASE}/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()}

def post_to_linkedin(access_token, author_urn, text):
    payload = json.dumps({
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }).encode()
    req = urllib.request.Request(
        f"{LINKEDIN_API_BASE}/ugcPosts",
        data=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
    )
    try:
        with urllib.request.urlopen(req) as r:
            return {"success": True, "status": r.status}
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()}

# ── Gemini AI helpers ──────────────────────────────────────────────────────────
def gemini_draft_post(topic, tone="professional", user_name=""):
    system = f"""You are an expert LinkedIn content strategist writing on behalf of {user_name}, 
an Agentic AI Developer specialized in automation for SMEs.

Write LinkedIn posts that are:
- Authentic and human, not corporate
- Start with a strong hook (not "I am excited to share")
- Use short paragraphs and line breaks for readability  
- Include 3-5 relevant hashtags at the end
- Between 150-300 words
- Tone: {tone}

Return ONLY the post text, nothing else."""

    payload = json.dumps({
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": f"Write a LinkedIn post about: {topic}"}]}]
    }).encode()
    req = urllib.request.Request(GEMINI_URL, data=payload,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error generating post: {str(e)}"

def gemini_improve_profile(section, current_text, user_name=""):
    system = f"""You are a LinkedIn profile optimisation expert improving the profile of {user_name},
an Agentic AI Developer specialized in automation for SMEs.

Rewrite the given {section} to be:
- Clear, compelling and keyword-rich
- Focused on value delivered to clients
- Professional but human
- Optimised for LinkedIn search

Return ONLY the improved text, nothing else."""

    payload = json.dumps({
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": f"Improve this LinkedIn {section}:\n\n{current_text}"}]}]
    }).encode()
    req = urllib.request.Request(GEMINI_URL, data=payload,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {str(e)}"

# ── HTTP Request Handler ───────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"  {args[0]} {args[1]} {args[2]}")

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000").split(",")
        origin = self.headers.get("Origin", "http://localhost:8000")
        allowed_origin = origin if origin in allowed_origins else allowed_origins[0]
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", allowed_origin)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html, status=200):
        body = html.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path, content_type):
        try:
            with open(path, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)
        except FileNotFoundError:
            self.send_json({"error": "File not found"}, 404)

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def get_session(self):
        cookie = self.headers.get("Cookie", "")
        for part in cookie.split(";"):
            part = part.strip()
            if part.startswith("session="):
                sid = part[8:]
                return sessions.get(sid), sid
        return None, None

    def do_OPTIONS(self):
        self.send_json({})

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        # Serve frontend
        if path == "/" or path == "/index.html":
            self.send_file("index.html", "text/html")

        # LinkedIn OAuth login
        elif path == "/login":
            state = secrets.token_urlsafe(16)
            sessions[f"state_{state}"] = True
            url = get_auth_url(state)
            self.send_response(302)
            self.send_header("Location", url)
            self.end_headers()

        # OAuth callback
        elif path == "/callback":
            code = params.get("code", [None])[0]
            state = params.get("state", [None])[0]
            error = params.get("error", [None])[0]

            if error:
                self.send_html(f"<h2>Auth error: {error}</h2>")
                return

            token_data = exchange_code_for_token(code)
            if "error" in token_data:
                self.send_html(f"<h2>Token error: {token_data['error']}</h2>")
                return

            access_token = token_data.get("access_token")
            profile = get_linkedin_profile(access_token)

            sid = secrets.token_urlsafe(32)
            sessions[sid] = {
                "access_token": access_token,
                "profile": profile,
                "author_urn": f"urn:li:person:{profile.get('sub', '')}"
            }

            self.send_response(302)
            self.send_header("Location", "/")
            self.send_header("Set-Cookie", f"session={sid}; Path=/; HttpOnly")
            self.end_headers()

        # Get current user session
        elif path == "/api/me":
            session, _ = self.get_session()
            if not session:
                self.send_json({"authenticated": False})
            else:
                p = session["profile"]
                self.send_json({
                    "authenticated": True,
                    "name": p.get("name", ""),
                    "email": p.get("email", ""),
                    "picture": p.get("picture", ""),
                    "sub": p.get("sub", "")
                })

        # Get pending posts awaiting approval
        elif path == "/api/pending":
            session, _ = self.get_session()
            if not session:
                self.send_json({"error": "Not authenticated"}, 401)
                return
            user_id = session["profile"].get("sub")
            user_pending = {k: v for k, v in pending_posts.items()
                          if v.get("user_id") == user_id}
            self.send_json({"posts": list(user_pending.values())})

        # Logout
        elif path == "/logout":
            _, sid = self.get_session()
            if sid and sid in sessions:
                del sessions[sid]
            self.send_response(302)
            self.send_header("Location", "/")
            self.send_header("Set-Cookie", "session=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT")
            self.end_headers()

        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        session, _ = self.get_session()

        if not session and path != "/api/draft":
            self.send_json({"error": "Not authenticated"}, 401)
            return

        # Draft a post with Gemini (human reviews before posting)
        if path == "/api/draft":
            if not session:
                self.send_json({"error": "Not authenticated"}, 401)
                return
            body = self.read_body()
            topic = body.get("topic", "")
            tone = body.get("tone", "professional")
            if not topic:
                self.send_json({"error": "Topic required"}, 400)
                return

            user_name = session["profile"].get("name", "")
            draft = gemini_draft_post(topic, tone, user_name)

            post_id = secrets.token_urlsafe(8)
            pending_posts[post_id] = {
                "id": post_id,
                "topic": topic,
                "draft": draft,
                "tone": tone,
                "status": "pending",
                "user_id": session["profile"].get("sub")
            }
            self.send_json({"post_id": post_id, "draft": draft})

        # Approve & publish post to LinkedIn
        elif path == "/api/approve":
            body = self.read_body()
            post_id = body.get("post_id")
            final_text = body.get("text", "")

            if post_id not in pending_posts:
                self.send_json({"error": "Post not found"}, 404)
                return

            result = post_to_linkedin(
                session["access_token"],
                session["author_urn"],
                final_text
            )

            if "error" in result:
                self.send_json({"error": result["error"]}, 400)
            else:
                pending_posts[post_id]["status"] = "published"
                self.send_json({"success": True, "message": "Post published to LinkedIn!"})

        # Reject/delete a pending post
        elif path == "/api/reject":
            body = self.read_body()
            post_id = body.get("post_id")
            if post_id in pending_posts:
                del pending_posts[post_id]
            self.send_json({"success": True})

        # Regenerate a post draft
        elif path == "/api/regenerate":
            body = self.read_body()
            post_id = body.get("post_id")
            if post_id not in pending_posts:
                self.send_json({"error": "Post not found"}, 404)
                return
            post = pending_posts[post_id]
            user_name = session["profile"].get("name", "")
            new_draft = gemini_draft_post(post["topic"], post.get("tone", "professional"), user_name)
            pending_posts[post_id]["draft"] = new_draft
            self.send_json({"draft": new_draft})

        # Improve profile section with Gemini
        elif path == "/api/improve-profile":
            body = self.read_body()
            section = body.get("section", "headline")
            current_text = body.get("text", "")
            if not current_text:
                self.send_json({"error": "Text required"}, 400)
                return
            user_name = session["profile"].get("name", "")
            improved = gemini_improve_profile(section, current_text, user_name)
            self.send_json({"improved": improved})

        else:
            self.send_json({"error": "Not found"}, 404)


# ── Start server ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    validate_env()  # Check all required env vars before starting
    port = PORT
    print(f"""
╔══════════════════════════════════════════════╗
║     LinkedIn Manager Agent is running!       ║
║                                              ║
║  Open: http://localhost:{port}                 ║
║  Login with your LinkedIn account            ║
║  Press Ctrl+C to stop                        ║
╚══════════════════════════════════════════════╝
    """)
    server = HTTPServer(("", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped gracefully.")
        print("\n  Server stopped.")
