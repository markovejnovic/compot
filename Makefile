.PHONY: build upload

VERSION = $(shell cat compot/__init__.py | grep -i __version__ | \
		  sed 's/__version__[[:space:]]=[[:space:]]//gI' | sed "s/'//g")

build:
	python setup.py sdist bdist_wheel
	twine check dist/*

upload: build
	twine upload dist/compot-ui-${VERSION}.tar.gz \
		dist/compot_ui-${VERSION}-py3-none-any.whl
