# AutoDrop

AutoDrop is a hackathon-built prototype for an automated dropshipping operating system. It combines product discovery, candidate screening, listing generation, storefront publishing, checkout, and operator analytics in a single local application.

This repository reflects a focused sprint completed in roughly 6.5 hours, from 9:30 AM to 4:00 PM. It is intentionally presented as a prototype rather than a production commerce platform. The goal of the project is to demonstrate workflow design, product thinking, and end-to-end integration under tight time constraints.

## Project Scope

AutoDrop explores the question: what parts of a dropshipping workflow can be meaningfully automated in one product loop?

In its current form, the app demonstrates a coherent operator-to-storefront pipeline:

1. discover a product signal
2. turn that signal into a product candidate
3. generate listing content
4. publish the item into a storefront
5. allow a customer to add the item to cart and check out
6. reflect the resulting activity back in an operator dashboard

That is the intended scope of this repository. It is not a claim that every marketplace, supplier, payment processor, or logistics system is fully integrated.

## What Is Implemented Today

### Operator Dashboard

The owner-facing interface includes:

- summary metrics for revenue, products, exceptions, and activity
- a pipeline view for trend intake, scouting, listing, publishing, and analytics
- robot activity logs
- catalog and product-status visibility
- trigger buttons for running key automation steps locally

### Customer Storefront

The customer-facing interface includes:

- hero product section
- multi-product grid
- bundled local product images
- add-to-cart behavior
- cart review
- checkout form with shipping and payment fields
- order confirmation messaging
- creator-content section with playable video modal
- voice-assistant entry point

### Backend Workflow

The backend includes working modules for:

- trend signal ingestion
- product approval / rejection
- listing and copy preparation
- influencer content record generation
- storefront publishing
- simulated checkout and order routing
- analytics updates

The modules are intentionally lightweight, but they are wired together and runnable in local mode.

## What Is Real vs. Simulated

This distinction matters for a public README, so it is explicit here.

### Real in the Current Prototype

- local full-stack app with a working frontend and backend
- persistent local database using SQLite
- live UI refresh between owner and storefront views
- cart and checkout flow inside the app
- local product catalog growth triggered from automation actions
- optional MiniMax integration for text generation
- optional ElevenLabs integration for voice output
- lightweight live public-source search in `Trend Radar` before fallback behavior

### Simulated or Simplified

- marketplace publishing is simulated rather than connected end-to-end to all real platforms
- supplier routing is simulated
- checkout is not connected to a real payment processor
- shipping, returns, and fulfillment are mocked
- trend search is intentionally lightweight and not equivalent to official platform-grade ingestion
- AI-generated creator content is represented in the UI, but not as a fully deployed media production system

## Architecture

### Backend

The backend is a FastAPI application with SQLAlchemy models and robot-style workflow modules.

Important areas:

- `backend/app/api`
- `backend/app/core`
- `backend/app/models.py`
- `backend/app/robots`
- `backend/app/services`
- `backend/app/worker`

Core data concepts:

- `trend_signals`
- `product_candidates`
- `channel_listings`
- `orders`
- `order_mappings`
- `robot_activity`
- `exceptions`

### Frontend

The frontend is a React + Vite application.

Important areas:

- `frontend/src`
- `frontend/public/products`

The UI is split into two primary surfaces:

- `Owner UI` for operations and automation control
- `Customer UI` for the storefront experience

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm

### Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload --port 8001
```

Backend URLs:

- API: [http://127.0.0.1:8001/api](http://127.0.0.1:8001/api)
- Docs: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

### Frontend

In a second terminal:

```bash
cd frontend
npm install
VITE_API_URL=http://localhost:8001 npm run dev
```

Frontend URL:

- App: [http://localhost:5173](http://localhost:5173)

## Environment Configuration

The app runs locally without most third-party credentials, but some features become richer when keys are present.

Common optional variables:

- `MINIMAX_API_KEY`
- `MINIMAX_MODEL`
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_VOICE_ID`
- `DATABASE_URL`
- `REDIS_URL`

See:

- `.env.example`
- `backend/app/core/config.py`

## Demo Flow

The intended local demonstration flow is:

1. open `Owner UI`
2. trigger `Launch Automation` or `Run Radar`
3. watch the activity feed and pipeline update
4. switch to `Customer UI`
5. confirm the newly added or refreshed product appears in the storefront
6. add products to cart
7. complete checkout
8. return to `Owner UI` and inspect the updated state

## Testing

Backend tests:

```bash
source .venv/bin/activate
python -m pytest
```

Frontend build:

```bash
cd frontend
npm run build
```

## Known Limitations

This project should be evaluated as a hackathon prototype.

Known limitations include:

- limited coverage of real third-party marketplace APIs
- simulated commerce and fulfillment steps
- lightweight trend ingestion rather than a hardened production crawler or official data pipeline
- minimal auth and security posture
- no production deployment hardening in this repository
- no formal payment, tax, or compliance integration

## Why This Repository Is Public

This repository is useful as:

- a prototype of an automation-heavy commerce workflow
- a reference for tying a control dashboard to a storefront in one codebase
- an example of how to build a coherent product demo quickly

It should not be interpreted as a turnkey production dropshipping system.

## Repository Hygiene

Generated runtime artifacts such as the local SQLite database should remain untracked. The repo is intended to contain source code, static assets, and configuration templates, not local machine state.
