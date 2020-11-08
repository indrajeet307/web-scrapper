venv:
	python3.6 -m venv VENV

install:
	pip install -r Requirements.txt

lint:
	isort --gitignore --check .
	black -l 100 --check .

lint-repair:
	isort --gitignore .
	black -l 100 .
	echo ">>> Use 'git status' to check updated files"

unit-test:
	python3.6 -m unittest test_read_html.py -v

