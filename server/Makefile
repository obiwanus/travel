PYTHON := python3.5

.PHONY: server
server:
	pip install -U -r requirements.txt
	$(PYTHON) manage.py runserver 0.0.0.0:8000

.PHONY: emailserver
emailserver:
	$(PYTHON) -u -m smtpd -n -c DebuggingServer localhost:1025

.PHONY: test
test:
	py.test tests
