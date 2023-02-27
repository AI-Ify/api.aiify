.PHONY: debug run setup help

help:
	@echo "Makefile options: \n\
	run:   -> run the backend api \n\
	debug: -> run api in debug mode \n\
	setup: -> install all python requirements"

run:
	uvicorn src.main:app

debug:
	uvicorn src.main:app --reload

setup:
	pip install --user -r requirements.txt