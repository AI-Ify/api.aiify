.PHONY: debug run setup

run:
	uvicorn main:app

debug:
	uvicorn main:app --reload

setup:
	pip install -r requirements.txt