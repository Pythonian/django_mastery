.DEFAULT_GOAL=help
ROOT_DIR:=./
VENV_BIN_DIR:=venv/bin

REQUIREMENTS_DIR:="requirements"
REQUIREMENTS_LOCAL:="$(REQUIREMENTS_DIR)/development.txt"

PIP:="$(VENV_BIN_DIR)/pip"
FLAKE8:="$(VENV_BIN_DIR)/flake8"

help:
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

define create-venv
python3 -m venv venv
endef

venv: # Create virtual environment
	@$(create-venv)

install: venv # Install local dependencies
	@$(PIP) install -r $(REQUIREMENTS_LOCAL)

migrations: venv # Run database migrations
	@python manage.py makemigrations
	@python manage.py migrate

superuser: venv # Create admin superuser
	@python manage.py createsuperuser

runserver: venv # Run development server
	@python manage.py runserver

test: venv # Run tests
	@python manage.py test

check: venv # Perform system check
	@python manage.py check

lint: venv # Check code style with flake8
	@$(FLAKE8) --exit-zero
