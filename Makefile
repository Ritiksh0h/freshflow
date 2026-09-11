.PHONY: setup lint format typecheck test bronze silver gold dashboard clean

setup:
	pip install -e ".[dev]"
	pre-commit install

lint:
	ruff check src tests

format:
	black src tests
	ruff check --fix src tests

typecheck:
	mypy src

test:
	pytest

bronze:
	python -m freshflow.bronze.ingest

silver:
	python -m freshflow.silver.clean

gold:
	python -m freshflow.gold.replenishment

dashboard:
	streamlit run src/freshflow/dashboard.py

clean:
	rm -rf spark-warehouse metastore_db derby.log .pytest_cache .ruff_cache .mypy_cache
