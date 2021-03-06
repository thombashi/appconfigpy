AUTHOR := thombashi
PACKAGE := appconfigpy
BUILD_WORK_DIR := _work
PKG_BUILD_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)


.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: build-remote
build-remote:
	@rm -rf $(BUILD_WORK_DIR)
	@mkdir -p $(BUILD_WORK_DIR)
	@cd $(BUILD_WORK_DIR) && \
		git clone https://github.com/$(AUTHOR)/$(PACKAGE).git && \
		cd $(PACKAGE) && \
		tox -e build
	ls -lh $(PKG_BUILD_DIR)/dist/*

.PHONY: check
check:
	@tox -e lint

.PHONY: clean
clean:
	@rm -rf $(BUILD_WORK_DIR)
	@tox -e clean

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: release
release:
	@cd $(PKG_BUILD_DIR) && python setup.py release --sign
	@rm -rf dist/

.PHONY: setup
setup:
	@pip install --upgrade -e .[test] releasecmd tox
	pip check
