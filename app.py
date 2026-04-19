from flask import Flask, jsonify, request, send_from_directory
import json
import os
import base64
import urllib.request
import urllib.error

app = Flask(__name__, static_folder='static')

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_REPO  = os.environ.get('GITHUB_REPO', '')
DATA_PATH    = os.environ.get('DATA_PATH', 'data/habit_data.json')


def github_get():
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return {"entries": []}, None
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATA_PATH}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            meta = json.loads(resp.read())
            sha = meta['sha']
            raw = base64.b64decode(meta['content']).decode('utf-8').strip()
            # Handle empty file
            if not raw:
                return {"entries": []}, sha
            try:
                return json.loads(raw), sha
            except json.JSONDecodeError:
                return {"entries": []}, sha
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"entries": []}, None
        raise


def github_put(data, sha=None):
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATA_PATH}"
    content = base64.b64encode(json.dumps(data, indent=2).encode()).decode()
    payload = {"message": "update tracker data", "content": content}
    if sha:
        payload["sha"] = sha
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, method='PUT', headers={
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    })
    with urllib.request.urlopen(req) as resp:
        resp.read()


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/entries', methods=['GET'])
def get_entries():
    try:
        data, _ = github_get()
        return jsonify(data.get('entries', []))
    except Exception as e:
        return jsonify([]), 200


@app.route('/api/entries', methods=['POST'])
def save_entry():
    try:
        data, sha = github_get()
        entry = request.json
        entries = data.get('entries', [])
        idx = next((i for i, e in enumerate(entries) if e['date'] == entry['date']), None)
        if idx is not None:
            entries[idx] = entry
        else:
            entries.append(entry)
        entries.sort(key=lambda x: x['date'])
        data['entries'] = entries
        github_put(data, sha)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
