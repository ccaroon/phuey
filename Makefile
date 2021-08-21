.PHONY: test
test:
	nosetests -v -s unit_tests/

.PHONY: cover
cover:
	nosetests -v -s unit_tests/ \
		--with-coverage \
		--cover-erase \
		--cover-html \
		--cover-inclusive \
		--cover-xml \
		--cover-package phuey/

.PHONY: dist
dist:
	python setup.py egg_info --tag-build=.$(shell date +%Y%m%d%H%M%S) sdist

.PHONY: clean
clean:
	rm -rf cover coverage.xml .coverage
	rm -rf dist
	find . -name "*.pyc" -exec rm {} \;
