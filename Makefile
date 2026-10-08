# ----------------------------------------------------------------
# fast-parse-time
# ----------------------------------------------------------------

install:
	@echo Installing Microservice
	poetry check
	poetry lock
	poetry update
	poetry install
	poetry run pre-commit install

activate:
	@echo Activating Microservice
	poetry run pre-commit autoupdate

test:
	echo Unit Testing Microservice
	poetry run python -m pytest -q

build:
	@echo Building Microservice
	make install
	make test
	poetry build

linters:
	@echo "Running Linters"
	poetry run pre-commit run --all-files

freeze:
	@echo "Freezing Requirements"
	poetry run pip freeze > requirements.txt
	poetry run python -m pip install --upgrade pip

all:
	make build
	make linters
	make freeze
