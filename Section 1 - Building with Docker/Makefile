SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: help

help: ## Output help for each target
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

create-virtualenv: # Create virtual environment and install dependencies
	python3 -m venv .venv
	python3 -m pip install -r requirements.txt

start-ve: # Start virtual environment
	source .venv/bin/activate

build: ## Build the Docker container
	docker build -t $(DOCKER_TAG)

run: ## Run the Docker container
	docker run -it -rm -p