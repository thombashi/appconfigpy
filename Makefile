.PHONY: build
build:
	@python setup.py build
	@rm -rf build/

.PHONY: clean
clean:
	@rm -rf build dist .eggs/ .pytest_cache/ **/*/__pycache__/ *.egg-info/

.PHONY: fmt
fmt:
	@black $(CURDIR)
	@isort --apply --recursive

.PHONY: release
release:
	@python setup.py release
	@rm -rf dist/
