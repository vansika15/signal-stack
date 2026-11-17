# Signal Stack – System Architecture Documentation

## Executive Overview
**Signal Stack** is an autonomous competitive and market intelligence application engineered for cross-functional leadership, strategy directors, and product teams. It continuously monitors permitted public sources, ingests internal operational telemetry, analyzes competitive developments, ranks insights via an explainable 6-factor model, and generates weekly executive Monday Morning Intelligence Briefs with automated action tracking.

---

## High-Level Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                  CLIENT LAYER                                     |
|  React 18 + Vite + TypeScript + Tailwind CSS + Lucide Icons                       |
|  - Overview Dashboard    - Company Setup & Research   - 10-Question AI Interview  |
|  - 4-Pillar Signal Stack - Source Manager             - Real-Time Intelligence    |
|  - Monday Morning Brief  - Internal Telemetry Ingest  - Settings & Schedulers     |
+----------------------------------------+------------------------------------------+
                                         | REST APIs / JSON
                                         v
+-----------------------------------------------------------------------------------+
|                              FASTAPI BACKEND LAYER                                |
|  - Companies & Profiles Router         - Adaptive Interview Router                |
|  - Competitors & Landscape Router      - Source Manager & Audit Router            |
|  - Web Crawler & Diff Router           - Explainable Intelligence & Feed Router   |
|  - Monday Brief & Action Router        - Background Scheduler & Logs Router       |
+----------------------------------------+------------------------------------------+
                                         |
     +-----------------------------------+-----------------------------------+
     |                                   |                                   |
     v                                   v                                   v
+-----------------------+   +-----------------------+   +-----------------------+
|   AI SERVICE LAYER    |   | CRAWLER SERVICE LAYER |   | SCHEDULER & REPORT    |
| - Gemini 1.5 Flash    |   | - robots.txt parser   |   | - APScheduler Engine  |
|   (Free Tier API)     |   | - BeautifulSoup4      |   | - Monday Brief Gen    |
| - Domain Heuristic    |   | - SHA-256 Content Diff|   | - Action Tracker      |
|   Inference Fallback  |   | - Deduplication Engine|   | - ReportLab PDF Gen   |
| - 6-Factor Ranker     |   | - Error & Status Codes|   | - Monthly Health Audit|
+-----------------------+   +-----------------------+   +-----------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             DATA PERSISTENCE LAYER                                |
|  SQLAlchemy 2.0 ORM (PostgreSQL-Compatible SQLite Engine)                         |
|  - Companies             - CompanyProfiles       - Competitors                    |
|  - Sources (20+ verified)- CrawlHistory          - IntelligenceItems              |
|  - InterviewSessions     - InterviewQAs          - InternalDocuments              |
|  - MondayReports (10 Sec)- ActionItems           - ScheduledJobLogs               |
+-----------------------------------------------------------------------------------+
```

---

## Core Pillars of the Signal Stack

### 1. Customer Intelligence
Captures buyer decision triggers, prospective student frictions, drop-off bottlenecks, financing approval delays, and sentiment shifts from student forums, user reviews, and counseling records.

### 2. Competitor Intelligence
Monitors direct, indirect, and emerging competitors (e.g. ApplyBoard, LeverageEdu, IDP, Adyen, Dynatrace), tracking pricing models, agent commission rebates, product feature parity, and geographic expansions.

### 3. Market Intelligence
Tracks macro regulatory shifts, government visa policies (e.g. Canada IRCC caps, UK Graduate Visa Route, Australia Subclass 500 funds proof), and foreign exchange volatility.

### 4. Internal Intelligence
Ingests internal company operational telemetry, sales logs, counselor intake bottleneck audits, and conversion metrics to correlate internal capacity with external market demands.

---

## Explainable 6-Factor Multi-Criteria Ranking Formula

Every intelligence item is mathematically scored from **0.0 to 100.0** according to:

$$\text{Score} = 100 \times \sum_{i} (w_i \times f_i)$$

Where:
1. **Strategic Relevance ($w_1 = 0.25$):** Alignment with core company profile and strategic priorities.
2. **Business Impact ($w_2 = 0.25$):** High ($1.0$), Medium ($0.6$), Low ($0.25$).
3. **Action Urgency ($w_3 = 0.20$):** Immediate ($1.0$), Short-Term ($0.75$), Medium-Term ($0.45$), Watchlist ($0.20$).
4. **Credibility & Evidence ($w_4 = 0.15$):** Weighted combination of source reliability tier, direct excerpt presence, and verification status.
5. **Recency Decay ($w_5 = 0.10$):** Exponential decay based on days elapsed since publication/discovery.
6. **Information Novelty ($w_6 = 0.05$):** Uniqueness score evaluated against previously ingested developments.

Every item provides an algorithmic breakdown accessible in the UI via the Explainable Ranking Score Modal.

---

## Web Crawler & Change Detection Pipeline

1. **Robots.txt Verification:** Checks domain robots.txt using standard robotparser with safety timeouts.
2. **Polite HTTP Fetching:** Configured with custom User-Agent, redirect follow, and 8s timeout.
3. **HTML Sanitization:** Strips script, style, and navigation tags; extracts page titles, meta descriptions, headings, and article paragraphs.
4. **SHA-256 Content Hashing:** Hashes extracted text to detect content modifications since previous crawl.
5. **Deduplication:** Verifies headline similarity against existing database records.
6. **Error Classification:** Correctly flags and records 404, 403, 429 (rate-limited), timeouts (slow), and unreachable servers.
7. **Audit Records:** Stores execution duration, status codes, response sizes, and signal extraction counts in `CrawlHistory`.

---

## 10-Section Monday Morning Brief Generator

Every generated brief produces all 10 mandatory sections:
1. **Executive Summary:** Strategic macro synthesis.
2. **Customer Signals:** Student/buyer behavior, friction, and sentiment shifts.
3. **Competitor Intelligence:** Competitor maneuvers, pricing, and packaging.
4. **Market Intelligence:** Regulatory visa gazettes and macroeconomic trends.
5. **Internal Business Intelligence:** Operational intake bottlenecks and conversion telemetry.
6. **Opportunities Identified:** High-yield expansion, program diversification, and partnership targets.
7. **Risks and Threats:** Competitor encroachment, regulatory caps, and student attrition points.
8. **Recommended Actions for This Week:** Prioritized operational directives with ownership and due dates.
9. **What We Should Watch:** Key leading indicators and upcoming government announcements.
10. **Source Appendix:** Traceability index linking each signal to its verifiable source.
