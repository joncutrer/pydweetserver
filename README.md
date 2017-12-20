# pydweetserver


Dweet.io API Compliant REST Web Server written in Python/Flask/MongoDB

Status: working but pending some refactoring

# Prerequisites

* Python 3.6
* pip install pipenv
* MongoDB Server running on localhost

# Installation

This python project uses pipenv so after cloning the repo you will need to install dependencies.

```bash
git clone https://github.com/joncutrer/pydweetserver.git
cd pydweetserver
pipenv install
pipenv run python pydweetserver/app.py

```
# How to use it

By default the REST API webserver will be running port 5000

### Start the server...

```bash
pipenv run python pydweetserver/app.py
```

browse to http://localhost:5000/

### Dweet something

http://localhost:5000/dweet/for/mything?foo=bar&temp=40&humidity=30


### Fetch the latest data for your thing

http://localhost:5000/get/latest/dweet/for/mything

There is a simple UI that will let you see you dweeted things

http://localhost:5000/see

The project aims to get API compatible with dweet.io, See: https://dweet.io/play/
