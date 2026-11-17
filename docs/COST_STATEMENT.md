# Signal Stack – Cost Statement & Financial Projection

## 1. Overview
Signal Stack is designed with cost efficiency and enterprise scalability as primary engineering objectives. The application is capable of running **at $0.00 infrastructure cost** in development and pilot staging, utilizing free tiers across AI, compute, and database services.

---

## 2. Itemized Cost Breakdown (Development & Pilot Staging)

| Component | Provider / Tier | Allocated Resource | Monthly Cost |
| :--- | :--- | :--- | :--- |
| **Generative AI Engine** | Google Gemini 1.5 Flash (Free Tier) | 15 RPM, 1,500 RPD, 1M TPM | **$0.00** |
| **Backend Compute & API** | Local Container / Free VPS (e.g. Render / Fly.io / Railway free) | 1 Shared vCPU, 512MB RAM | **$0.00** |
| **Web Crawler Network** | Standard HTTP/HTTPS Requests | ~1,200 crawls / month (polite rate limits) | **$0.00** |
| **Database Persistence** | Embedded SQLite / Supabase Free Postgres | Up to 500MB storage | **$0.00** |
| **Frontend Static Hosting** | Vercel / Netlify / Cloudflare Pages | Unlimited bandwidth & builds | **$0.00** |
| **PDF Generation Engine** | Local ReportLab open-source Python library | In-process PDF compilation | **$0.00** |
| **Total Staging Cost** | | | **$0.00 / month** |

---

## 3. Gemini 1.5 Flash Token Consumption Analysis

| Operation | Input Tokens | Output Tokens | Invocations / Mo | Total Tokens | Free Tier Coverage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Company Research** | 450 | 650 | 10 | 11,000 | 100% (Well within limits) |
| **10-Question Diagnostic** | 600 | 950 | 10 | 15,500 | 100% |
| **Follow-Up Interrogation** | 350 | 250 | 50 | 30,000 | 100% |
| **Internal Doc Ingestion** | 1,200 | 400 | 30 | 48,000 | 100% |
| **Monday Brief (10 Sec)** | 2,800 | 1,600 | 12 (4 wks x 3 comps) | 52,800 | 100% |
| **Monthly Total** | | | | **~157,300 tokens** | **< 1% of free monthly quota** |

---

## 4. Production Scale Projection (100 Active Enterprise Companies)

When scaling Signal Stack to 100 enterprise organizations tracking 2,000 sources:

| Infrastructure Item | Sizing & Specification | Estimated Monthly Cost |
| :--- | :--- | :--- |
| **Google Gemini API** | Pay-as-you-go ($0.075 / 1M input, $0.30 / 1M output) | **$4.85** |
| **Backend & Crawler Service** | 2x Scaled Virtual Servers (2 vCPU, 4GB RAM) | **$24.00** |
| **Managed Database** | AWS RDS PostgreSQL (db.t4g.micro) | **$18.00** |
| **S3 Object Storage** | PDF Report & Crawl Snapshot Archive (20GB) | **$0.50** |
| **Cloudflare CDN & WAF** | Pro Tier with automated DDoS mitigation | **$20.00** |
| **Total Production Estimate** | Supporting 100 Companies & 2,000 Sources | **~$67.35 / month** |

*Cost per monitored company in full production: **~$0.67 / month**.*
