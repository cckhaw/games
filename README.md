# Arcade

Apple-HIG-styled arcade portal (`/`) with an admin CMS (`/admin`). Vite + React, Vercel serverless API, Vercel Blob storage.

## Run locally
`npm i && npm run dev` — with no API, the app falls back to `src/data/games.json` plus browser localStorage, so the admin UI works (any token is accepted in this mode).

## Deploy (production only)
1. Create a Vercel project and attach a **Blob** store (sets `BLOB_READ_WRITE_TOKEN`).
2. Set project env var `ADMIN_TOKEN` (the admin password).
3. Add GitHub secrets `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`.
4. Push to `main`: `.github/workflows/deploy.yml` runs `vercel deploy --prod`, then `scripts/prune-deployments.mjs` deletes every other deployment so only the latest remains.

Vercel's own Git integration is disabled in `vercel.json`, so PR/preview branches never deploy.

## Data
`src/data/games.json` is the seed. Once an admin saves, the catalog lives in Blob (`catalog/games.json`); tile images are resized to 960×720 WebP in the browser and stored under `tiles/`.
