# GitHub Repository Analyzer

A command-line tool that gives you an instant breakdown of any public GitHub repository — languages, file count, largest files, and dependencies. Built in Python.

---

## What it does

Point it at any GitHub repo and get a structured report in seconds

## How it works

The tool makes a series of calls to the GitHub REST API:

| API Endpoint | What we use it for |
|---|---|
| `/repos/{owner}/{repo}` | Basic repo info |
| `/repos/{owner}/{repo}/languages` | Language breakdown |
| `/repos/{owner}/{repo}/git/trees/HEAD?recursive=1` | Full file tree |
| `raw.githubusercontent.com/...` | Reading dependency files |

Dependency detection currently supports:
- **JavaScript/Node** → `package.json`
- **Python** → `requirements.txt`, `Pipfile`
- **Go** → `go.mod`
- **Java** → `pom.xml`

---

## Project structure

```
github-analyzer/
├── analyzer.py       # Main script
├── .env              # Your GitHub token (never committed)
├── .gitignore        # Keeps .env out of version control
└── README.md
```

---

## Requirements

- Python 3.7+
- A free GitHub account + personal access token
- `requests` and `python-dotenv` libraries

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/github-analyzer.git
cd github-analyzer
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install requests python-dotenv
```

**4. Add your GitHub token**

Create a `.env` file in the root of the project:
```
GITHUB_TOKEN=your_token_here
```

To get a free token: GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic) → Generate new token. Only the `public_repo` scope is needed.

---

## Usage

```bash
python analyzer.py <github-repo-url>
```
---

