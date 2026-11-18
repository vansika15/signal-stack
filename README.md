# Signal Stack – Autonomous Competitive & Market Intelligence Platform
*EDXSO AI Engineer Intern Assignment 1 – Full Production Delivery*

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue.svg)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC.svg)](https://tailwindcss.com/)
[![Tests](https://img.shields.io/badge/Tests-12%20Gates%20Passed%20(100%25)-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

Signal Stack is an autonomous, end-to-end competitive and market intelligence application engineered for strategy directors, product managers, and executive leadership. It continuously crawls permitted public sources, ingests internal operational telemetry, analyzes competitive developments, ranks them using an **explainable 6-factor multi-criteria scoring algorithm**, and synthesizes an executive **10-Section Monday Morning Intelligence Brief** with automated action item tracking.

---

## Key Features

- **Primary Showcase: MeetUniversity (`meetuniversity.com`):** Configured with **20 approved public sources**, 8 competitors (Direct, Indirect, Emerging), 40 verified intelligence records (28 Live Crawled Evidence + 12 Seeded Demo Baseline), completed 10-question adaptive interview, and executive Monday Brief with 32KB PDF export.
- **Multi-Company Demonstrations & Strict Isolation:** Seamlessly switch between **MeetUniversity** (EdTech / Higher Education Matching), **Stripe** (FinTech / Payments Infrastructure; 6 sources, 6 competitors, 11 intelligence items [7 live crawled]), and **Datadog** (Cloud Observability & Security SaaS; 5 sources, 6 competitors, 11 intelligence items [7 live crawled]). 100% multi-tenant data isolation with zero cross-contamination.
- **The Four Signal Stack Pillars:**
  1. *Customer Intelligence:* Student & buyer intent, application friction, loan bottlenecks, drop-offs, and churn sentiment.
  2. *Competitor Intelligence:* ApplyBoard, LeverageEdu, IDP, Adyen, Dynatrace; competitor pricing, agent commission wars, financing bundles.
  3. *Market Intelligence:* IRCC Canada visa caps, UK Graduate Visa Route, Australia Subclass 500 funds proof, foreign exchange fluctuations.
  4. *Internal Intelligence:* Admissions counselor call logs, 48-hour manual document verification backlogs, virtual matchmaking conversion yields. (Clearly labeled: internal telemetry status explicitly reported as connected vs disconnected).
- **Explainable 6-Factor Multi-Criteria Ranking:** Transparent mathematical weighting (Relevance 25%, Impact 25%, Urgency 20%, Credibility 15%, Recency 10%, Novelty 5%) with an interactive modal breakdown for every signal.
- **Adaptive 10-Question Diagnostic Interview:** Dynamic executive interrogation with real-time progress steps, ground-truth answer capture, contextual follow-ups, and strategic takeaways.
- **Real Public-Source Web Crawler:** Complies with `robots.txt`, detects content modifications via SHA-256 hashing, prevents duplicate noise, extracts direct evidence citations, and monitors source health (including HTTP 403 Forbidden handling).
- **Monday Morning Intelligence Brief:** Synthesizes all 10 mandatory executive sections, tracks weekly action items with live checkboxes, and generates downloadable ReportLab PDFs.
- **Autonomous Schedulers:** Built-in APScheduler managing weekly brief generation, monthly source-health audits, and periodic crawl sweeps.
- **Dual-Engine AI Architecture:** Native integration with **Google Gemini 1.5 Flash** with an offline heuristic reasoning engine for instant fallback.

---

## Architecture Overview

```
+-----------------------------------------------------------------------------------+
|                        REACT + VITE + TAILWIND FRONTEND                           |
|  - Overview Dashboard   - Company Profile & Context   - 10-Question AI Interview  |
|  - 4-Pillar Signal Stack- Source Manager (20 Feeds)   - Real-Time Intelligence    |
|  - Monday Brief (10 Sec)- Internal Telemetry Ingest   - Settings & Schedulers     |
+----------------------------------------+------------------------------------------+
                                         | REST APIs
                                         v
+-----------------------------------------------------------------------------------+
|                            FASTAPI BACKEND SERVICES                               |
|  - AI Service (Gemini 1.5 Flash / Fallback) - Crawler Service (robots.txt + SHA256)|
|  - Explainable 6-Factor Ranking Engine       - ReportLab PDF Generator            |
|  - APScheduler Automation Engine             - SQLAlchemy ORM Data Layer          |
+-----------------------------------------------------------------------------------+
```

---

## Quickstart Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.11 & 3.13)
- Node.js 18+ (Tested on Node.js v24.16.0)
- npm / pnpm

### 1. Clone & Setup Backend
```bash
# Clone the repository
git clone <your-repo-url>
cd signal-stack

# Setup Python virtual environment
cd backend
python -m venv venv

# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Run backend automated tests
pytest tests -v
```

### 2. Setup Frontend
```bash
cd ../frontend
npm install

# Build production bundle
npm run build
```

### 3. Run the Application
You can run the full application in one of two ways:

#### Option A: Unified Full-Stack Server (Recommended)
Since the FastAPI backend automatically mounts the built frontend:
```bash
cd backend
python run_backend.py
```
Open **`http://localhost:8000`** in your browser. Both the complete SaaS UI and REST APIs will be live!

#### Option B: Independent Vite Dev Server
```bash
# Terminal 1: Backend
cd backend
python run_backend.py

# Terminal 2: Frontend Dev Server
cd frontend
npm run dev
```
Open **`http://localhost:5173`** (proxies `/api` requests to `http://localhost:8000`).

---

## Environment Variables Configuration

Copy `.env.example` to `backend/.env`:
```bash
cp .env.example backend/.env
```

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite:///./signal_stack.db` | PostgreSQL-compatible SQLite database |
| `GEMINI_API_KEY` | `""` | Google Gemini 1.5 Flash API Key (Optional; fallback engine active if blank) |
| `SCHEDULER_ENABLED` | `true` | Enables autonomous background jobs |
| `SCHEDULER_TIMEZONE` | `"UTC"` | Timezone for cron schedules |
| `CRAWL_INTERVAL_HOURS`| `24` | Hours between background crawler sweeps |

---

## Verification & Test Results

Run the verification test suite:
```bash
cd backend
pytest tests -v
python tests/run_tests_direct.py
```

### Output:
```
=================================================================
RUNNING SIGNAL STACK COMPREHENSIVE 12-GATE VERIFICATION SUITE
=================================================================
✔ [1/12] Database initialization and seed completed.
✔ [2/12] Mandatory company demonstrations verified: ['meetuniversity', 'stripe', 'datadog']
✔ [3/12] MeetUniversity public sources verified: 20 sources with documented relevance explanations.
✔ [4/12] Four Signal Stack categories present with 40 intelligence records.
✔ [5/12] Explainable 6-factor ranking mechanism verified across all intelligence items.
✔ [6/12] 10-Question adaptive interview with dynamic follow-ups verified.
✔ [7/12] MeetUniversity Monday Brief verified: all 10 sections populated with 3 action items & strict provenance (28 live / 12 demo).
✔ [8/12] MeetUniversity Executive PDF Brief verified (32729 bytes).
✔ [9/12] Stripe demonstration verified: 6 sources, 6 competitors, 7 live crawled records, 4 demo records.
✔ [10/12] Datadog demonstration verified: 5 sources, 6 competitors, 7 live crawled records, 4 demo records.
✔ [11/12] Multi-tenant strict isolation verified: 0 cross-contamination between MeetUniversity, Stripe, and Datadog.
✔ [12/12] Overall intelligence volume verified: 62 total records (42 live crawled across all companies; requirement was minimum 30).
=================================================================
ALL 12 VERIFICATION GATES PASSED PERFECTLY!
=================================================================
```

---

## Public Cloud Deployment (Vercel & Render)

Signal Stack is production-ready for public cloud deployment:
- **Frontend (Vercel)**: Global Edge CDN with automated SPA rewrites via [`frontend/vercel.json`](file:///frontend/vercel.json).
- **Backend (Render)**: Python FastAPI with dynamic `$PORT` and 0.0.0.0 host binding via [`render.yaml`](file:///render.yaml).
- **Database (PostgreSQL)**: Fully compatible with Render Managed PostgreSQL or SQLite; automated migration script in [`backend/scripts/migrate_sqlite_to_postgres.py`](file:///backend/scripts/migrate_sqlite_to_postgres.py).

For full step-by-step instructions, see the **[Public Cloud Deployment Guide](file:///docs/DEPLOYMENT_GUIDE.md)**.

---

## Docker Deployment

To launch the full production stack with Docker Compose:
```bash
docker-compose up --build
```
- Backend available at: `http://localhost:8000`
- Frontend available at: `http://localhost:5173`

---

## Documentation Links
- [Public Cloud Deployment Guide](file:///docs/DEPLOYMENT_GUIDE.md)
- [System Architecture](file:///docs/ARCHITECTURE.md)
- [API Documentation](file:///docs/API_DOCUMENTATION.md)
- [Technical Engineering Report](file:///docs/TECHNICAL_REPORT.md)
- [Cost Statement](file:///docs/COST_STATEMENT.md)
- [Demo Recording Script](file:///docs/DEMO_SCRIPT.md)
- [Automated Verification Evidence](file:///docs/TEST_EVIDENCE.md)

---

## License
MIT License – Engineered for the EDXSO AI Engineer Intern Assessment.
