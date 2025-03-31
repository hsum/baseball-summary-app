.PHONY: setup install test test-api deploy deploy-verbose clean

setup:
	./setup_baseball-summary-app.sh

install:
	pip install -r requirements.txt

test:
	pytest -v tests/

test-api:
	uvicorn main:app --reload --port 8080

deploy:
	gcloud functions deploy pitch-summary \
		--runtime python311 \
		--trigger-http \
		--allow-unauthenticated \
		--entry-point gcp_pitch_summary \
		--memory 512MB

deploy-verbose:
	gcloud functions deploy pitch-summary \
		--runtime python311 \
		--trigger-http \
		--allow-unauthenticated \
		--entry-point gcp_pitch_summary \
		--memory 512MB \
		--verbosity=debug

clean:
	rm -rf __pycache__ *.pyc *.zip
