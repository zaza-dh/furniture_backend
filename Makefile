venv:
	pip3.6 install virtualenv
	python3.6 -m virtualenv venv36

install:
	pip install -e .

run: 
	python -m uvicorn ikea_backend.app:app

lint:
	flake8 rock_paper_scissors || isort --recursive .