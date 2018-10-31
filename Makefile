coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=py17track tests
init:
	pip install pip pipenv
	pipenv lock
	pipenv install --dev
lint:
	pipenv run flake8 py17track
	pipenv run pydocstyle py17track
	pipenv run pylint py17track
publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg py17track.egg-info/
test:
	pipenv run py.test
typing:
	pipenv run mypy --ignore-missing-imports py17track
