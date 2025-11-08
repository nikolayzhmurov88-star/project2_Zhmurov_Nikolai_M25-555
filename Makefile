install:
	poetry install

project:
	poetry database

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl --break-system-packages

lint:
	poetry run ruff check