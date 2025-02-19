.PHONY: install test test-unit test-functional test-coverage clean

install:
	pip install -r requirements.txt

test-unit: install
	PYTHONPATH=$(PYTHONPATH):$(PWD) pytest tests/unit -v

test-functional: install
	PYTHONPATH=$(PYTHONPATH):$(PWD) QT_QPA_PLATFORM=offscreen pytest tests/functional -v

test: test-unit test-functional

test-coverage: install
	PYTHONPATH=$(PYTHONPATH):$(PWD) pytest tests/unit -v --cov=src --cov-report=html
	PYTHONPATH=$(PYTHONPATH):$(PWD) QT_QPA_PLATFORM=offscreen pytest tests/functional -v --cov=src --cov-append --cov-report=html
	open htmlcov/index.html

clean:
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +