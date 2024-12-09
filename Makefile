# Makefile for managing package
VENV := .venv
NAME := littleR
PYTHON := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip
ACTIVATE := $(VENV)/Scripts/activate
DIST := dist
EGGINFO := $(NAME).egg-info
SPHINX := docs
MAIN := main.py

.PHONY: env
env: $(ACTIVATE) install
	@echo *****************
	@echo !!! env: DONE !!!
	@echo *****************

.PHONY: all
all: $(ACTIVATE) install package
	@echo *****************
	@echo !!! all: DONE !!!
	@echo *****************
	
$(ACTIVATE):
	@echo **************************
	@echo create virtual environment
	@echo **************************
	python -m venv .venv

.PHONY: install
install: $(ACTIVATE)
	@echo *************************
	@echo install required packages
	@echo *************************
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install --upgrade build
	$(PIP) install -r requirements.txt

.PHONY: cli
cli: $(ACTIVATE)
	@echo *******
	@echo run CLI
	@echo *******
	$(PYTHON) $(MAIN)

.PHONY: format
format: $(ACTIVATE)
	@echo ***********
	@echo format code
	@echo ***********
	$(PYTHON) -m black ./$(NAME) ./test

.PHONY: test
test: $(ACTIVATE)
	@echo *********
	@echo run tests
	@echo *********
	$(PYTHON) -m pytest ./test

.PHONY: lint
lint: $(ACTIVATE)
	@echo *************
	@echo run fast lint
	@echo *************
	$(PYTHON) -m ruff check ./$(NAME)

.PHONY: pylint
pylint: $(ACTIVATE)
	@echo *************
	@echo run slow lint
	@echo *************
	$(PYTHON) -m pylint ./$(NAME)

.PHONY: html
html: $(ACTIVATE)
	@echo *************
	@echo generate HTML
	@echo *************
	$(PYTHON) -m sphinx -b html $(SPHINX)/source $(SPHINX)/build

.PHONY: package
package: $(ACTIVATE) install
	@echo *************
	@echo build package
	@echo *************
	$(PYTHON) -m build

.PHONY: clean
clean:
	@echo *************
	@echo clean package
	@echo *************
	rmdir $(DIST) /s /q
	rmdir $(EGGINFO) /s /q

.PHONY: uninstall
uninstall:
	@echo ***************
	@echo uninstall .venv
	@echo ***************
	rmdir $(VENV) /s /q

.PHONY: help
help:
	@echo Targets:
	@echo   env        - Create a virtual environment and install dependencies.
	@echo   all        - Create environment, install dependencies, and build package.
	@echo   install    - Install dependencies from requirements.txt.
	@echo   cli	       - Run the littleR command line interface.
	@echo   format	   - Format the code using Black.
	@echo   test       - Run tests.
	@echo   lint	   - Run the fast ruff linter.
	@echo   pylint     - Run the slower pylint linter.
	@echo   html       - Generate HTML documentation. Calls sphinx make.
	@echo   package    - Build the package.
	@echo   clean      - Remove Package build files.
	@echo   uninstall  - Remove the virtual environment.
	@echo   help       - Display this help message.