INTEG_IMAGE=test-server-integ:latest
DUMMY_SERVER=dummy-server

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
	python -m unittest test_read_html.py -v

integ-test: build-integ-docker
	docker run --rm -d -p 8000:8000 --name ${DUMMY_SERVER} ${INTEG_IMAGE}
	sleep 5
	python3.6 -m unittest test_integ_read_html.py -v
	rc=$$?
	docker stop ${DUMMY_SERVER}
	exit $$rc

build-integ-docker:
	cd test-server; docker build . -t ${INTEG_IMAGE}

clean:
	rm -rf VENV
