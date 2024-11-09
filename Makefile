# Makefile for managing package
VENV_NAME := .venv

all: venv activate

venv:
	python -m venv $(VENV_NAME)

activate: .venv
	source $(VENV_NAME)/Scripts/activate

install: requirements.txt
	pip install -r requirements.txt

