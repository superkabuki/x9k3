PY3 = python3
PYPY3 = pypy3

default: install

clean:
	rm -f dist/*
	rm -rf build/*

pkg: clean
	$(PY3) -m build -n

pypy3:  pkg
	$(PYPY3) -m pip install . --break-system-packages	

install: pkg
	$(PY3)  -m pip install . --break-system-packages	
	
upload: clean pkg	
	twine upload dist/*


