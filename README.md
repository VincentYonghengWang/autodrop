<<<<<<< HEAD
# autodrop
dropshipping app
=======
# AutoDrop

AutoDrop is a full-stack command center for an automated dropshipping pipeline. This repository includes:

- FastAPI backend
- SQLAlchemy models for robot workflows
- Celery worker and beat configuration
- React admin dashboard
- Docker Compose for local development

## Quick start

1. Copy `.env.example` to `.env`
2. Start the stack:

```bash
docker compose up --build
```

3. Open:

- API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Dashboard: `http://localhost:5173`
- Flower: `http://localhost:5555`

## Services

- `backend`: FastAPI API and dashboard data endpoints
- `worker`: Celery worker running robot tasks
- `beat`: Celery beat scheduler
- `db`: PostgreSQL 15
- `redis`: Redis 7
- `flower`: Celery monitoring UI
- `frontend`: React admin dashboard

>>>>>>> 300a270 (Initial AutoDrop app scaffold)
