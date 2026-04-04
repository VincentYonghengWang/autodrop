# AutoDrop

AutoDrop is a demo-first dropshipping command center built for fast hackathon storytelling:

- trend detection
- product scouting
- listing and content generation
- storefront publishing
- simulated checkout, routing, and analytics

## Fast local demo

1. Create and activate a virtual environment.
2. Install backend dependencies.
3. Start the API.
4. Start the frontend.

```bash
cd /Users/yongheng8tb/Downloads/Autodrop
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload
```

In a second terminal:

```bash
cd /Users/yongheng8tb/Downloads/Autodrop/frontend
npm install
npm run dev
```

Open:

- API docs: `http://localhost:8000/docs`
- App UI: `http://localhost:5173`

## Demo flow

1. Open `Owner UI`
2. Click `Launch Demo Loop`
3. Open `Customer UI`
4. Click `Buy demo product`
5. Switch back to `Owner UI` and show the new sale, routing, and updated metrics

## Tests

Run the backend tests with:

```bash
source .venv/bin/activate
python -m pytest
```
