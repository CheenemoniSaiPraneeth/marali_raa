# Elite Execution Tracker

A personal habit + weight tracking dashboard deployable on Render.

## Files
- `app.py` — Flask backend (serves API + static files)
- `static/index.html` — Full frontend (charts, habits, weight)
- `requirements.txt` — Python deps
- `render.yaml` — Render config
- `data.json` — Auto-created on first save (your data lives here)

## Customizing Habits
Open `static/index.html` and find the `HABITS` array near the top of the `<script>` tag.
Add/remove entries like: `{ id: 'myhabit', label: 'My Habit' }`
Then add a matching checkbox in the sidebar HTML above.

## Deploy on Render (Free Tier)

1. Push this folder to a GitHub repo
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Settings:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add a **Disk** (so data persists):
   - Render Dashboard → your service → Disks → Add Disk
   - Mount Path: `/opt/render/project/src`
   - Size: 1 GB (free)
6. Deploy!

## Local Run
```bash
pip install flask gunicorn
python app.py
# Open http://localhost:5000
```
