install:
	poetry install

run:
	poetry run uvicorn main:app --host localhost --port 8086 --reload

test:
	poetry run pytest test


.PHONY: install run test
