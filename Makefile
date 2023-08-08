.DEFAULT_GOAL=help
ROOT_DIR:=./
VENV_BIN_DIR:=venv/bin

PIP:="$(VENV_BIN_DIR)/pip"
FLAKE8:="$(VENV_BIN_DIR)/flake8"

help:
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

define create-venv
python -m venv venv
endef

venv: # Create virtual environment
	@$(create-venv)

install: venv # Install project dependencies
	@$(PIP) install -r requirements.txt

freeze: venv # Freeze project dependencies
	@$(PIP) freeze > requirements.txt

migrations: venv # Run database migrations
	@python manage.py makemigrations
	@python manage.py migrate

admin: venv # Create admin superuser
	@python manage.py createsuperuser

runserver: venv # Run development server
	@python manage.py runserver

test: venv # Run tests
	@python manage.py test

check: venv # Perform system check
	@python manage.py check

lint: venv # Check code style
	@$(FLAKE8) --exit-zero

dockerdown: # Shut down docker compose
	@docker-compose down -v
