PYTHON := python3.5

.PHONY: server
server:
	$(PYTHON) manage.py runserver 0.0.0.0:8000

.PHONY: emailserver
emailserver:
	$(PYTHON) -u -m smtpd -n -c DebuggingServer localhost:1025

.PHONY: install
install:
	pip install -U -r requirements.txt

.PHONY: test
test:
	py.test tests
