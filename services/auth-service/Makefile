.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[35m  %-25s\033[0m %s\n", $$1, $$2}'


run:	## Start Gateway Clipper API Service
	@echo "--- Starting Gateway Clipper API Service ---"
	scripts/setup/setup-data.sh
	docker compose down
	docker compose --profile core --profile api build --parallel
	docker compose --profile core --profile api up --remove-orphans --force-recreate
.PHONY:	run


.PHONY:	lint-all
lint-all:	black bandit pycln isort  ## Perform all linting and security checks (black bandit pycln isort).


.PHONY:	black
black: ## Format code using black
	@echo "--- Performing black reformatting ---"
	black ./src/


.PHONY: bandit
bandit:	## Perform python code security checks using bandit
	@echo "--- Performing bandit code security scanning ---"
	bandit ./src/ --configfile pyproject.toml --recursive --format json --verbose


.PHONY: isort
isort: ## Perform isort to sort through python imports
	@echo "--- Perform python import sorting ---"
	isort ./src/


.PHONY: pycln
pycln: ## Perform python import clean
	@echo "--- Perform python import clean ---"
	pycln ./src/
