help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:  ## Clean python bytecodes, optimized files, logs, cache, coverage...
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".cache" -type d | xargs rm -rf
	@find . -name ".coverage" -type f | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log
	@echo 'Temporary files deleted'

conf-env:  ## Generate the .env file for local development
	@cp -n localenv .env
	@echo 'Please configure params from .env file before starting'

install: ## Install app dependencies
	@echo 'Creating container...'
	@docker-compose up -d || (echo "Could not create container $$?"; exit 1)
	@pip install pipenv || (echo "Could not install pipenv $$?"; exit 1)
	@pipenv install || (echo "Could not install pip dependencies $$?"; exit 1)
	@echo 'Done!'

runserver: ## Starts API web server
	@uvicorn api.main:app --reload

import: ## Imports data from "starlink_historical_data.json" file into database
	@python import.py || (echo "Could not import data $$?"; exit 1)

migrate: ## Create database tables 
	@alembic upgrade head || (echo "Could not apply migrations $$?"; exit 1)
