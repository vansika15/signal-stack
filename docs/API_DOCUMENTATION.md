# Signal Stack – API Documentation

All API endpoints are prefixed with `/api` and return standard JSON responses. Interactive OpenAPI / Swagger UI documentation is available at `http://localhost:8000/docs`.

---

## 1. Companies & Research

### `GET /api/companies`
Lists all registered companies.
- **Response:** Array of `CompanyResponse`

### `GET /api/companies/{company_id}`
Returns details and AI profile for a specific company.
- **Response:** `CompanyResponse`

### `POST /api/companies/research`
Dynamically researches any company website using Gemini AI / domain heuristics.
- **Request Body:**
  ```json
  {
    "website": "https://example.com",
    "company_name": "Optional Name"
  }
  ```
- **Response:** Structured industry, business model, and strategic priorities.

### `POST /api/companies`
Creates and initializes a new company in the workspace.
- **Request Body:** `CompanyCreate`

### `PUT /api/companies/{company_id}`
Updates company fields or business context.
- **Request Body:** `CompanyUpdate`

---

## 2. Adaptive 10-Question Diagnostic Interview

### `GET /api/interviews/{company_id}/session`
Fetches or starts the current 10-question interview session for the company.
- **Response:** `InterviewSessionResponse`

### `POST /api/interviews/{company_id}/start`
Generates a brand new 10-question diagnostic interview tailored to company industry and profile.

### `POST /api/interviews/{session_id}/answer/{qa_id}`
Submits ground-truth answer for a question and dynamically generates a follow-up interrogation and strategic takeaway.
- **Request Body:**
  ```json
  { "answer_text": "Executive response..." }
  ```

### `POST /api/interviews/{session_id}/followup/{qa_id}`
Submits answer to the adaptive follow-up question.
- **Request Body:**
  ```json
  { "follow_up_answer": "Follow-up response..." }
  ```

---

## 3. Competitor Intelligence

### `GET /api/competitors/{company_id}`
Returns all monitored competitors categorized by tier (Direct, Indirect, Emerging).

### `POST /api/competitors/{company_id}`
Manually registers a competitor.

### `POST /api/competitors/{company_id}/discover`
Triggers AI landscape discovery to detect 5–10 competitors.

### `DELETE /api/competitors/{competitor_id}`
Removes a competitor from monitoring.

---

## 4. Source Manager & Health Audits

### `GET /api/sources/{company_id}`
Lists all public monitoring sources (20+ verified for MeetUniversity).

### `POST /api/sources/{company_id}`
Adds a new source with documented relevance explanation.

### `POST /api/sources/{company_id}/discover`
Auto-discovers recommended permitted public sources for the company.

### `PUT /api/sources/{source_id}/status`
Updates source status (`approved`, `pending`, `rejected`).

### `POST /api/sources/audit`
Runs a real-time availability and HTTP status code health audit across sources.

---

## 5. Web Crawler & Change Detection

### `POST /api/crawler/crawl/{source_id}`
Performs live crawl of a specific source: checks robots.txt, computes SHA-256 diff, extracts signals, logs history.

### `POST /api/crawler/crawl-all/{company_id}`
Executes a crawl sweep across all approved sources for the company.

### `GET /api/crawler/history/{company_id}`
Returns historical crawl logs, duration ms, status codes, and change detection flags.

---

## 6. Signal Stack & Intelligence Feed

### `GET /api/intelligence/{company_id}`
Returns ranked intelligence feed with optional query parameters:
- `category`: Filter by pillar
- `search`: Keyword search in headline/summary
- `impact`: Filter by High, Medium, Low
- `urgency`: Filter by Immediate, Short-Term, Medium-Term, Watchlist
- `verification`: Filter by Verified, Pending Verification, Unverified

### `POST /api/intelligence/{company_id}`
Creates a signal item, automatically executing the explainable 6-factor ranking calculation.

### `GET /api/intelligence/{item_id}/ranking-breakdown`
Returns exact mathematical breakdown and component weights for the signal's ranking score.

---

## 7. Monday Morning Intelligence Brief & Actions

### `GET /api/reports/{company_id}`
Lists historical Monday briefs.

### `POST /api/reports/generate/{company_id}`
Synthesizes all 10 executive sections from active signals and extracts weekly action items.

### `GET /api/reports/{report_id}/download-pdf`
Generates and downloads styled ReportLab PDF brief.

### `GET /api/reports/{company_id}/actions`
Returns all action items with status, ownership, and due dates.

### `PUT /api/reports/actions/{action_id}`
Updates action item status (`todo`, `in_progress`, `completed`).

---

## 8. Schedulers & Settings

### `GET /api/scheduler/status`
Returns scheduler running state, cron schedules, and active jobs.

### `POST /api/scheduler/trigger/{job_name}`
Manually triggers `weekly_brief`, `monthly_audit`, or `crawler_sweep`.

### `GET /api/scheduler/history`
Returns execution history and failed-job logs.

### `GET /api/settings` and `POST /api/settings`
Reads and updates API credentials, crawl intervals, and scheduler configuration.
