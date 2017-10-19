PYTHON := python3.5

.PHONY: server
server:
	$(PYTHON) manage.py runserver 0.0.0.0:8000

.PHONY: install
install:
	pip install -U -r requirements.txt

.PHONY: test
test:
	py.test tests

.PHONY: debug_test
debug_test:
	py.test -s tests
