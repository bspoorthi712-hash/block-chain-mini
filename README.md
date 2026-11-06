# Mini Blockchain Project

A beginner-friendly blockchain demonstration built with Python and Flask.

## Features
- Create blocks and store transactions
- Link blocks using SHA-256 hashes
- Mine blocks using a simple Proof of Work algorithm
- Validate the blockchain
- Access functionality through REST API endpoints

## Requirements
- Python 3.10 or newer
- pip

## Run locally

```bash
# Optional: create and activate a virtual environment
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Project home page |
| GET | `/chain` | View the blockchain |
| POST | `/transactions/new` | Add a transaction |
| POST | `/mine` | Mine a block |
| GET | `/valid` | Check blockchain integrity |

### Add a transaction

Send a POST request to `http://127.0.0.1:5000/transactions/new`
with JSON body:

```json
{
  "sender": "Alice",
  "receiver": "Bob",
  "amount": 100
}
```

Then send a POST request to `http://127.0.0.1:5000/mine`.

Check the chain at `http://127.0.0.1:5000/chain` and validate it at
`http://127.0.0.1:5000/valid`.

## GitHub

Create a new GitHub repository, then upload these project files. Alternatively:

```bash
git init
git add .
git commit -m "Add mini blockchain project"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## Educational note

This is a local educational prototype. It is not a decentralized network,
does not implement digital signatures or peer-to-peer consensus, and is not
suitable for real money or production use.
