# AI ScamShield (Backend)

## Local run (via docker-compose at repo root)
```bash
cp .env.example .env
```

Backend runs at: http://localhost:8000  
Docs: http://localhost:8000/docs

## Retrain models
```bash
python -m ml.train_text
python -m ml.train_url
```
(Inside container: `docker compose exec backend python -m ml.train_text`)
