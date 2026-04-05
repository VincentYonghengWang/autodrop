# AutoDrop

AutoDrop is a full-stack dropshipping command center designed to show how product discovery, listing generation, storefront publishing, checkout, and post-order operations can be automated in one workflow.

The project was built as a hackathon-ready product demo, but it is structured like a real multi-service commerce app:

- FastAPI backend for APIs and orchestration
- React + Vite frontend for the owner dashboard and customer storefront
- SQLAlchemy models for products, trends, orders, activity, and exceptions
- robot modules for trend scanning, product scouting, listing creation, publishing, routing, analytics, and customer support
- local SQLite mode for easy demos
- optional service integrations such as MiniMax and ElevenLabs

## What AutoDrop Does

AutoDrop models the lifecycle of an automated dropshipping business:

1. discover products from trend sources
2. evaluate candidate products for margin and supplier fit
3. generate product copy and campaign content
4. publish items to the storefront
5. let customers add to cart and complete checkout
6. route orders and update business metrics

The current app includes both an internal operator view and a customer-facing ecommerce experience.

## Main Features

### Owner UI

The owner dashboard is the operational control room. It shows:

- revenue, live products, exception count, and activity metrics
- the product pipeline from trend intake to publishing and analytics
- recent robot activity and pipeline progress
- live catalog rows with source, margin, channel, and factory hint data
- trigger buttons for the most important workflows

### Customer UI

The storefront is a polished commerce surface with:

- hero product section
- trending product grid
- creator campaign section
- factory district spotlight section
- cart review and multi-item checkout flow
- floating voice assistant button

### Automation Robots

The backend is organized around robot modules:

- `Trend Radar`
  Finds product opportunities from live public sources and curated fallback signals.
- `Product Scout`
  Converts signals into product candidates with margin-aware pricing.
- `Listing Factory`
  Generates listing assets and product copy, including MiniMax-backed copy when configured.
- `Influencer Factory`
  Creates creator campaign records for promoted products.
- `Multi-Channel Publisher`
  Pushes products into channel listings and marks them live.
- `Order Router`
  Simulates routing paid orders to suppliers.
- `Analytics Brain`
  Updates winner/loser state and dashboard metrics.
- `CS Bot`
  Represents the support automation layer.

## Current Demo Capabilities

The current version is optimized for a strong local demo:

- each `Run Radar` or `Launch Automation` run can add a new product to the storefront
- product cards use relevant local image assets to avoid hotlink failures
- the cart supports multiple items, quantity changes, shipping/tax totals, and checkout
- the owner dashboard updates after checkout
- the storefront includes playable creator video modals
- the voice assistant can answer product questions
- the listing pipeline can use MiniMax for product copy generation

## Architecture

### Backend

Important backend folders:

- [backend/app/api](/Users/yongheng8tb/Downloads/Autodrop/backend/app/api)
- [backend/app/core](/Users/yongheng8tb/Downloads/Autodrop/backend/app/core)
- [backend/app/models.py](/Users/yongheng8tb/Downloads/Autodrop/backend/app/models.py)
- [backend/app/robots](/Users/yongheng8tb/Downloads/Autodrop/backend/app/robots)
- [backend/app/services](/Users/yongheng8tb/Downloads/Autodrop/backend/app/services)
- [backend/app/worker](/Users/yongheng8tb/Downloads/Autodrop/backend/app/worker)

Core backend concepts:

- `trend_signals` store raw trend discoveries
- `product_candidates` store approved products that can move to publishing
- `channel_listings` represent published items
- `orders` and `order_mappings` represent sales and routing state
- `robot_activity` drives the owner activity feed

### Frontend

Important frontend folders:

- [frontend/src](/Users/yongheng8tb/Downloads/Autodrop/frontend/src)
- [frontend/public/products](/Users/yongheng8tb/Downloads/Autodrop/frontend/public/products)

Core frontend behavior:

- owner dashboard pulls `/api/dashboard`
- storefront pulls `/api/storefront`
- trigger buttons call workflow endpoints
- checkout posts to `/api/storefront/checkout/:product_id`
- voice assistant posts to `/api/storefront/voice-assistant`

## Local Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm

### Backend Setup

```bash
cd /Users/yongheng8tb/Downloads/Autodrop
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload --port 8001
```

Backend endpoints:

- API root: [http://127.0.0.1:8001/api](http://127.0.0.1:8001/api)
- docs: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

### Frontend Setup

In a second terminal:

```bash
cd /Users/yongheng8tb/Downloads/Autodrop/frontend
npm install
VITE_API_URL=http://localhost:8001 npm run dev
```

Frontend URL:

- app UI: [http://localhost:5173](http://localhost:5173)

## Environment Variables

AutoDrop works in local mode without most external credentials, but some features become richer when keys are provided.

Examples include:

- `MINIMAX_API_KEY`
- `MINIMAX_MODEL`
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_VOICE_ID`
- `DATABASE_URL`
- `REDIS_URL`

See:

- [.env.example](/Users/yongheng8tb/Downloads/Autodrop/.env.example)
- [backend/app/core/config.py](/Users/yongheng8tb/Downloads/Autodrop/backend/app/core/config.py)

## How To Demo The App

### Simple Demo Flow

1. Open the app at [http://localhost:5173](http://localhost:5173)
2. Start in `Owner UI`
3. Click `Launch Automation`
4. Watch the workflow and activity feed update
5. Switch to `Customer UI`
6. Show the newly added product on the storefront
7. Add products to cart
8. Complete checkout
9. Switch back to `Owner UI` and show updated metrics

### Run Radar Flow

`Run Radar` is useful when you want to specifically demo product discovery:

1. click `Run Radar`
2. the backend searches live public trend sources first
3. it logs the search source and chosen product
4. the product moves through scouting and listing creation
5. the storefront refreshes with the new item

## AI and Voice Features

### MiniMax

When `MINIMAX_API_KEY` is configured:

- product descriptions can be generated by MiniMax
- creator campaign copy can be generated for the hero product

When MiniMax is unavailable, AutoDrop falls back gracefully to built-in copy.

### ElevenLabs

When `ELEVENLABS_API_KEY` is configured:

- the voice assistant can synthesize spoken product responses

If ElevenLabs is unavailable, the app can still fall back to browser speech features.

## Tests

Run backend tests with:

```bash
cd /Users/yongheng8tb/Downloads/Autodrop
source .venv/bin/activate
python -m pytest
```

Build the frontend with:

```bash
cd /Users/yongheng8tb/Downloads/Autodrop/frontend
npm run build
```

## Known Limitations

This is still a demo-oriented product implementation, not a full production commerce system.

Current limitations include:

- trend search is lightweight and currently relies on public-source scraping plus curated fallback signals
- checkout is simulated rather than connected to a live payment processor
- order routing is mocked/simulated
- channel publishing is simulated rather than fully connected to every marketplace
- some AI features fall back to static content if external APIs are unavailable

## Roadmap Ideas

Natural next steps for the project:

- live TikTok / Instagram / Amazon integrations
- richer supplier and cost intelligence
- real payment processing
- real inventory and shipping APIs
- analytics history views
- proper authentication and multi-user accounts
- persistent media generation pipeline

## Repository Notes

Local runtime files such as the SQLite database are intentionally kept out of Git. The working repo may contain a local `autodrop.db`, but that should remain a local artifact, not a tracked source file.
