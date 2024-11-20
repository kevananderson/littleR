# Makefile for managing package
VENV := .venv
NAME := littleR
PYTHON := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip
ACTIVATE := $(VENV)/Scripts/activate
DIST := dist
EGGINFO := $(NAME).egg-info

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
	@echo   env        - Create a virtual environment and install dependancies.
	@echo   all        - Create environment, install dependancies, and build package.
	@echo   install    - Install dependencies from requirements.txt.
	@echo   test       - Run tests.
	@echo   lint	   - Run the fast rust linter.
	@echo   pylint     - Run the slower pylint linter.
	@echo   package    - Build the package.
	@echo   clean      - Remove Package build files.
	@echo   uninstall  - Remove the virtual environment.
	@echo   help       - Display this help message.