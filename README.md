# Automated Multi-Platform Posting System

A FastAPI REST service that validates short promotional messages containing a single Call-To-Action (CTA) URL and publishes them concurrently across 5 third-party platforms with independent fault tolerance.

## Integrated Platforms
1. **Telegraph (pi.telegra.ph)**: Publishes instant public articles (auto-provisions an anonymous token if TELEGRAPH_ACCESS_TOKEN is omitted).
2. **dpaste (dpaste.org/api/)**: Publishes public text snippets via REST API.
3. **Dev.to (dev.to/api/articles)**: Publishes public posts via Forem API (DEVTO_API_KEY).
4. **GitHub Gists (pi.github.com/gists)**: Creates public Markdown gists (GITHUB_TOKEN).
5. **Bluesky (sky.social/xrpc)**: Publishes public posts with rich-text link facets via AT Protocol (BLUESKY_HANDLE, BLUESKY_APP_PASSWORD).

## Project Structure
\\\	ext
automated-posting/
+-- app/
¦   +-- main.py
¦   +-- schemas.py
¦   +-- config.py
¦   +-- platforms/
¦   ¦   +-- base.py
¦   ¦   +-- telegraph.py
¦   ¦   +-- dpaste.py
¦   ¦   +-- devto.py
¦   ¦   +-- github_gist.py
¦   ¦   +-- bluesky.py
¦   +-- services/
¦       +-- posting_service.py
+-- tests/
¦   +-- test_posting.py
+-- .env.example
+-- requirements.txt
+-- README.md
\\\

## Setup & Local Execution

1. **Create and activate virtual environment:**
   \\\ash
   python -m venv venv
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # Linux/macOS:
   source venv/bin/activate
   \\\

2. **Install dependencies:**
   \\\ash
   pip install -r requirements.txt
   \\\

3. **Configure environment variables:**
   \\\ash
   cp .env.example .env
   \\\
   Fill in your API credentials in .env (never commit .env to GitHub).

4. **Start the server on port 4000:**
   \\\ash
   uvicorn app.main:app --host 0.0.0.0 --port 4000
   \\\

5. **Open interactive Swagger UI:**
   Navigate to http://localhost:4000/docs

## Sample API Request & Response

### Request (POST http://localhost:4000/posting)
\\\json
{
  "message": "Check out our latest business platform and grow your online visibility. https://example.com"
}
\\\

### Response (200 OK)
\\\json
{
  "success": true,
  "results": [
    {
      "platform": "Telegraph",
      "status": "success",
      "posted_url": "https://telegra.ph/Check-out-our-latest-business-platform-11-16",
      "public_access": true,
      "date": "2026-11-16",
      "time": "17:15:22",
      "error": null
    },
    {
      "platform": "dpaste",
      "status": "success",
      "posted_url": "https://dpaste.org/AbCdE",
      "public_access": true,
      "date": "2026-11-16",
      "time": "17:15:22",
      "error": null
    }
  ]
}
\\\

## Running Tests
\\\ash
pytest -v
\\\
"@

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v






Set-Content -Path "README.md" -Value @"
# Automated Multi-Platform Posting System

FastAPI REST service that validates messages containing a single CTA URL and publishes them concurrently across 5 third-party platforms (Telegraph, dpaste, Dev.to, GitHub Gists, Bluesky) with independent fault tolerance.

## Setup & Execution

1. Create and activate virtual environment:
   python -m venv venv
   .\venv\Scripts\Activate.ps1

2. Install dependencies:
   pip install -r requirements.txt

3. Configure environment variables:
   cp .env.example .env

4. Run server on port 4000:
   uvicorn app.main:app --host 0.0.0.0 --port 4000

5. Open Swagger UI:
   http://localhost:4000/docs

## Run Tests
   pytest -v
