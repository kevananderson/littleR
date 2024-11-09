# Makefile for managing package
VENV := .venv
PYTHON := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip

.PHONY: all
all: $(VENV) requirements.txt


$(VENV):
	python -m venv .venv


.PHONY: install
install: requirements.txt $(VENV)
	$(PIP) install -r requirements.txt


requirements.txt: $(VENV)
	$(PIP) install -r requirements.txt


.PHONY: clean
clean:
	rmdir $(VENV) /s /q


.PHONY: help
help:
	@echo Targets:
	@echo   all        - Create environment and install dependancies.
	@echo   $(VENV)      - Create a virtual environment
	@echo   install    - Install dependencies from requirements.txt
	@echo   clean      - Remove the virtual environment
	@echo   help       - Display this help message