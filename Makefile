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
