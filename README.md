# Baseball Pitch Summary App
A FastAPI app deployed on GCP Cloud Functions to summarize MLB pitch speeds for a given date.

## Setup
- Run `./setup_baseball-summary-app.sh`
- Install dependencies: `make install`
- Test locally: `make test` (pytest) or `make test-api` (FastAPI)

## Deployment
- Deploy: `make deploy`
- CI/CD: Auto-deploys on push to `master` via `cloudbuild.yaml`

## Endpoints
- GET `/pitch-summary/{date}`: Returns pitch stats for a date (YYYY-MM-DD).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
## Live Endpoint
- GET `https://us-central1-baseball-summary.cloudfunctions.net/pitch-summary/{date}`
  - Returns pitch stats for a given date (YYYY-MM-DD).
  - Example: `curl https://us-central1-baseball-summary.cloudfunctions.net/pitch-summary/2023-06-01`
