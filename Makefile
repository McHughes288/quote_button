.DEFAULT_GOAL=all
cov_dir:=htmlcov
pytest_args:= -v --color=yes --junit-xml ut_results.xml --cov-report=html:$(cov_dir) --cov-report=term --disable-pytest-warnings
includes="."

all: deps check

deps:
	./scripts/setup.sh
check:
	black --check "${includes}"
	flake8 --max-line-length=100 "${includes}"
	pylint "${includes}"
clean:
	$(RM) -r $(wildcard ut_*.xml) $(cov_dir) .pytest_cache .coverage exp models logs
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
format:
	black "${includes}"