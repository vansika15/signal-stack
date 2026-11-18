# Signal Stack – Public Cloud Deployment Guide
*Production Deployment: Frontend on Vercel + Backend on Render + Managed PostgreSQL*

---

## 1. Architecture Overview

Signal Stack is configured for decoupled, resilient public cloud hosting using GitHub continuous deployment:

```
+------------------------------------+           +---------------------------------------+
|         VERCEL (FRONTEND)          |           |            RENDER (BACKEND)           |
|  - Vite + React 18 + TypeScript    |  HTTPS    |  - FastAPI (Python 3.11/3.13)         |
|  - Global Edge CDN                 +---------->+  - Uvicorn on 0.0.0.0:$PORT           |
|  - Config: VITE_API_BASE_URL       |   REST    |  - APScheduler (1 Worker, No Dups)    |
|  - vercel.json SPA rewrites        |           |  - CORS with Vercel Domain & Preview  |
+------------------------------------+           +-------------------+-------------------+
                                                                     |
                                                                     v
                                                 +---------------------------------------+
                                                 |         RENDER POSTGRESQL (DB)        |
                                                 |  - Managed Free Instance              |
                                                 |  - Persistent relational storage      |
                                                 |  - Zero data loss across redeploys    |
                                                 +---------------------------------------+
```

---

## 2. Step 1: Deploy Backend & Database on Render

### Option A: Automatic Deployment using Render Blueprint (Recommended)
The repository includes a ready-to-use [`render.yaml`](file:///c:/Users/hp/.gemini/antigravity/scratch/signal-stack/render.yaml) blueprint:
1. Log in to [Render.com](https://dashboard.render.com/).
2. Click **New +** -> **Blueprint**.
3. Connect your GitHub repository: `https://github.com/vansika15/signal-stack`.
4. Render will read `render.yaml` and automatically configure:
   - **Database**: `signal-stack-db` (Free PostgreSQL).
   - **Web Service**: `signal-stack-backend` (Python 3.11).
5. (Optional) Provide your `GEMINI_API_KEY` in the prompt, or leave blank to use the built-in domain reasoning engine.
6. Click **Apply**.
7. Once deployed, copy your backend service URL (e.g. `https://signal-stack-backend.onrender.com`).

---

### Option B: Manual Web Service Setup on Render
If configuring manually without a Blueprint:
1. **Create PostgreSQL Database**:
   - Click **New +** -> **PostgreSQL**.
   - Name: `signal-stack-db`
   - Plan: **Free**
   - Click **Create Database** and copy the **Internal Database URL** (or External Database URL).
2. **Create Web Service**:
   - Click **New +** -> **Web Service**.
   - Connect repository `https://github.com/vansika15/signal-stack`.
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `python run_backend.py`
3. **Environment Variables**:
   | Variable | Value | Description |
   | :--- | :--- | :--- |
   | `PYTHON_VERSION` | `3.11.9` | Python runtime version |
   | `APP_ENV` | `production` | Production mode |
   | `HOST` | `0.0.0.0` | Bound host |
   | `PORT` | `10000` *(Render sets this automatically)* | Listening port |
   | `DATABASE_URL` | *`postgresql://...` from Step 1* | PostgreSQL connection string |
   | `CORS_ORIGINS` | `*` *(or your Vercel URL)* | Cross-Origin Resource Sharing |
   | `SCHEDULER_ENABLED` | `true` | Enables autonomous background jobs |
   | `GEMINI_API_KEY` | *(Optional)* | Google Gemini AI key (empty = offline fallback) |

---

## 3. Step 2: Database Setup & Data Migration

### Automatic Initialization
When the backend starts up on Render for the first time:
- SQLAlchemy executes `Base.metadata.create_all()` to generate all tables.
- `seed_database(db)` executes idempotently, populating MeetUniversity (20 sources, 8 competitors, 12 benchmark signals, 10-question founder interview), Stripe (6 sources, 6 competitors, 4 signals), and Datadog (5 sources, 6 competitors, 4 signals).

### Migrating Existing Local Crawled Records to Hosted PostgreSQL
To transfer your exact local SQLite records (including all 42 live crawled evidence records) into your hosted PostgreSQL database without losing any data:
```bash
# From your local terminal:
cd backend
python scripts/migrate_sqlite_to_postgres.py "postgresql://user:password@host:5432/signal_stack"
```
The migration script automatically checks every table, preserves IDs and relationships, skips duplicates, and confirms 100% record integrity.

---

## 4. Step 3: Deploy Frontend on Vercel

1. Log in to [Vercel](https://vercel.com/).
2. Click **Add New...** -> **Project**.
3. Import the GitHub repository: `https://github.com/vansika15/signal-stack`.
4. Configure Project Settings:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click `Edit` and select `frontend`.
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. **Environment Variables**:
   - Add `VITE_API_BASE_URL`: Paste your Render backend URL (e.g. `https://signal-stack-backend.onrender.com`).
6. Click **Deploy**.
7. In ~30 seconds, Vercel will assign your public production URL (e.g. `https://signal-stack.vercel.app`).

---

## 5. Step 4: Final Production CORS Configuration

Once Vercel gives you your frontend domain (e.g. `https://signal-stack.vercel.app`):
1. In Render Dashboard -> `signal-stack-backend` -> **Environment**.
2. Update `CORS_ORIGINS`:
   ```
   https://signal-stack.vercel.app
   ```
   *(The backend automatically accepts both the exact production URL and all Vercel branch preview URLs matching `https://.*\.vercel\.app`).*
3. Render will auto-redeploy with strict CORS enforcement.

---

## 6. Verification Checklist

1. **Backend Health Check**:
   Open `https://<your-backend>.onrender.com/api/health`.
   Expected response:
   ```json
   {
     "status": "healthy",
     "database": "connected",
     "scheduler": true
   }
   ```
2. **API Interactive Docs**:
   Open `https://<your-backend>.onrender.com/docs` to verify OpenAPI Swagger documentation.
3. **Frontend Dashboard**:
   Open `https://<your-frontend>.vercel.app`.
   - Verify KPI cards render.
   - Switch between **MeetUniversity**, **Stripe**, and **Datadog**.
   - Navigate to **Monday Brief** and click **Download PDF**.
   - Check **Source Manager** and trigger a test crawl on an approved source.

---

## 7. Important Actions Requiring User Authorization

Because deploying to cloud platforms requires logging into your personal accounts:
1. **GitHub Repository Access**: Your GitHub repository is publicly accessible at `https://github.com/vansika15/signal-stack`.
2. **Render Account**: You will need to create a free account at [render.com](https://render.com) and authorize Render to connect to your GitHub repository.
3. **Vercel Account**: You will need to log into [vercel.com](https://vercel.com) and import the repository.
4. **No Paid Services Required**: All recommended setups utilize 100% free tiers on both Vercel and Render.
