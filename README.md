# AI ScamShield – Full Working Local Stack

## One-command local startup
```bash
cp backend/.env.example backend/.env
docker compose up --build
```

Open:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Retrain models
```bash
docker compose exec backend python -m ml.train_text
docker compose exec backend python -m ml.train_url
```

## Deploy to Render
This repo includes a `render.yaml` Blueprint:
1. Push to GitHub.
2. In Render: **New → Blueprint** and select your repo.
3. Deploy.

Notes:
- The frontend uses same-origin `/api/*` calls in production.
- The Blueprint sets a rewrite rule to proxy `/api/*` to the backend.
- If Render assigns a different backend URL than `https://scamshield-backend-yb1y.onrender.com', update the `destination` in `render.yaml`.
