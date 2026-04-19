# Elite Execution Tracker

Habit + weight tracking dashboard. Free on Render. Data stored in GitHub (no paid disk needed).

## How data is stored
Every time you hit "Save Daily Progress", the app writes `data.json` directly to your GitHub repo via the GitHub API. Free, persistent, survives redeployments.

---

## Deploy on Render — Step by Step

### Step 1 — Push this folder to GitHub
- Go to github.com → New repository → name it `elite-tracker`
- Upload all files from this zip into it and commit

### Step 2 — Create a GitHub Personal Access Token
- GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
- Generate new token → check the `repo` scope → copy it

### Step 3 — Deploy on Render
- render.com → New → Web Service → connect your `elite-tracker` repo
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Click Create Web Service

### Step 4 — Add Environment Variables in Render
- Your service → Environment tab → Add:
  - `GITHUB_TOKEN` = your token from Step 2
  - `GITHUB_REPO`  = e.g. `CheenemoniSaiPraneeth/elite-tracker`
- Save Changes — Render redeploys automatically

### Step 5 — Done!
Open your Render URL, save a day. Check GitHub — `data.json` appears there.

---

## Customize Habits
In `static/index.html`:
1. Add to HABITS array: `{ id: 'myhabit', label: 'My_Habit' }`
2. Add checkbox in sidebar HTML: `<div class="habit-item"><input type="checkbox" id="myhabit"><label for="myhabit">My Habit</label></div>`
3. Push to GitHub — Render auto-redeploys

## Local Run
```
pip install flask
export GITHUB_TOKEN=your_token
export GITHUB_REPO=yourname/elite-tracker
python app.py
```
