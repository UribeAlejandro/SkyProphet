.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

.PHONY: help
help:			## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: venv
venv:			## Create a virtual environment
	@echo "Creating virtualenv ..."
	@rm -rf .venv
	@python3 -m venv .venv
	@./.venv/bin/pip install -U pip
	@echo
	@echo "Run 'source .venv/bin/activate' to enable the environment"

.PHONY: install
install:		## Install dependencies
	pip install -r requirements-dev.txt
	pip install -r requirements-test.txt
	pip install -r requirements.txt

STRESS_URL = http://127.0.0.1:8000
.PHONY: stress-test
stress-test:		## Starts a server & run stress-tests
	mkdir -p reports/stress || true
	locust -f tests/stress/api_stress.py --print-stats --html reports/stress/index.html --run-time 60s --headless --users 100 --spawn-rate 10 -H $(STRESS_URL)

.PHONY: model-test
model-test:		## Run model-tests and coverage
	mkdir reports || true
	pytest --cov=challenge tests/model

.PHONY: api-test
api-test:		## Run api-tests and coverage
	mkdir -p reports/coverage || true
	pytest --cov=challenge tests/api

SERVER_URL = 0.0.0.0:8000
.PHONY: run-server
run-server: 		## Run the server
	gunicorn --bind $(SERVER_URL) challenge.api:app --reload -k uvicorn.workers.UvicornWorker
