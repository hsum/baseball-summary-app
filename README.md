# Baseball Summary App
-A FastAPI app deployed on GCP Cloud Functions to summarize MLB pitch speeds for a given date.

## Live Endpoint
- **GET** `https://us-central1-baseball-summary.cloudfunctions.net/pitch-summary/{date}`
  - Returns pitch stats for a given date (YYYY-MM-DD).
  - Example: `curl https://us-central1-baseball-summary.cloudfunctions.net/pitch-summary/2023-06-01`
  - Response: `{"date": "2023-06-01", "average_pitch_speed": 89.72, "max_pitch_speed": 102.9, "total_pitches": 1979}`

## Design Overview
`main.py` supports three execution paths—Cloud Functions, FastAPI, and CLI—each handling pitch data fetching with distinct runtime needs. Here’s how they work and why `get_pitch_summary` is `async`:

### Code Paths
1. **Cloud Functions (Live Deployment)**
   - **Trigger:** HTTP request (e.g., `/pitch-summary/2023-06-01`).
   - **Flow:** `gcp_pitch_summary` (sync) → `asyncio.run(get_pitch_summary(date))` → `statcast` fetch → JSON response.
   - **Sync Wrapper:** Uses `asyncio.run()` to run the async `get_pitch_summary` in Google Cloud Functions’ synchronous runtime (Flask-based via `functions-framework`).

2. **FastAPI (Local Testing)**
   - **Trigger:** `make test-api` → `curl http://localhost:8080/pitch-summary/2023-06-01`.
   - **Flow:** FastAPI’s async endpoint → `get_pitch_summary(date)` → `statcast` fetch → JSON response.
   - **Async Native:** Runs in FastAPI’s event loop, designed for non-blocking I/O.

3. **CLI (Local Execution)**
   - **Trigger:** `python main.py --date 2023-06-01`.
   - **Flow:** `cli()` → `asyncio.run(get_pitch_summary(date))` → `statcast` fetch → Console output.
   - **Sync Wrapper:** Like Cloud Functions, uses `asyncio.run()` for a single synchronous call.

### Async vs. Sync Design
- **Why Async?**
  - `get_pitch_summary` is `async` to align with FastAPI’s async-first framework, enabling non-blocking I/O for local testing.
  - Anticipates future async support in `pybaseball.statcast` (currently sync, but I/O-bound tasks like HTTP requests benefit from async potential).
  - Unified logic avoids duplicating code for sync and async contexts.

- **Sync Workarounds:**
  - **Cloud Functions:** Wraps `async` call in `asyncio.run()` because the Python runtime expects a synchronous entry point.
  - **CLI:** Uses `asyncio.run()` for simplicity in a single-threaded context.
  - Overhead is minimal, and it keeps the codebase DRY (Don’t Repeat Yourself).

- **Trade-Offs:**
  - Could be fully synchronous (simpler for Cloud Functions/CLI), but would break FastAPI compatibility or require separate implementations.
  - Current design balances local dev (async FastAPI) and cloud deployment (sync Cloud Functions) with flexibility for future async optimizations.

### Takeaway
The `async` core with sync wrappers ensures `main.py` works across all paths while staying forward-compatible. On `master`, it’s live and humming at 512MB on Cloud Functions!
