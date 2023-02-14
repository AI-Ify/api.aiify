.PHONY: debug run

run:
	python3 -m flask --app backend run

debug:
	python3 -m flask --app backend --debug run
