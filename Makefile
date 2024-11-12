# Makefile for managing package
VENV := .venv
PYTHON := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip

.PHONY: all
all: $(VENV) install
	@echo ************
	@echo !!! DONE !!!
	@echo ************
	
$(VENV):
	@echo **************************
	@echo create virtual environment
	@echo **************************
	python -m venv .venv


.PHONY: install
install: $(VENV)
	@echo *************************
	@echo install required packages
	@echo *************************
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt


.PHONY: clean
clean:
	@echo ***************************
	@echo CLEAN all build directories
	@echo ***************************
	rmdir $(VENV) /s /q


.PHONY: help
help:
	@echo Targets:
	@echo   all        - Create environment and install dependancies.
	@echo   $(VENV)      - Create a virtual environment
	@echo   install    - Install dependencies from requirements.txt
	@echo   clean      - Remove the virtual environment
	@echo   help       - Display this help message