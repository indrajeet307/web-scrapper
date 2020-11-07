lint:
	isort --gitignore --check .
	black --check .

lint-repair:
	isort --gitignore .
	black .
	echo ">>> Use 'git status' to check updated files"

unit-test:
	python3.6 -m unittest test_read_html.py

