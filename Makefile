.DEFAULT_GOAL := help

help: ## Displays this help message.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

source: ## Sources python. - source bot-env/bin/activate
	'msource bot-env/bin/activate'

build: ## Runs the bot.
	python3 bot.py