# 🚀 Vercel Deployment Guide

This project deploys on Vercel using `@vercel/python` and the Flask app exported from `api/index.py`.

## 1) Required Environment Variables

Set these in **Vercel → Project → Settings → Environment Variables**:

- `APP_ENV=production` (or `FLASK_ENV=production`)
- `JWT_SECRET_KEY=<strong-random-secret>`
- `DATABASE_URL=<postgresql://...>`
- `RUN_DB_CREATE_ALL=false`

In production:
- `JWT_SECRET_KEY` is required
- `DATABASE_URL` must be a persistent database (SQLite is rejected)

## 2) Deploy

1. Import the GitHub repository into Vercel.
2. Confirm the framework preset is **Other**.
3. Keep `vercel.json` as-is (routes all requests to `api/index.py`).
4. Deploy.

## 3) Initialize Database Schema Once

Do this once per environment (from local machine or CI):

```bash
APP_ENV=production \
JWT_SECRET_KEY=... \
DATABASE_URL=postgresql://... \
flask --app app:create_app init-db
```

`db.create_all()` is intentionally not run on every production cold start.

## 4) Static HTML Routes

The Flask page routes (e.g. `/`, `/login`) try to serve HTML files from:
1. repository root
2. `templates/`

If a file is missing from deployment artifacts, the route returns a clear `404` JSON error.

## 5) Local Vercel Test

```bash
npm i -g vercel
vercel dev
```

