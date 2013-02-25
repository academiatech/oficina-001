.SILENT:

all: clean

clean:
	find . -name '*.pyc' | xargs rm -f
	rm -rf build

start:
	PYTHONPATH=`pwd`:`pwd`/mybookmarks python mybookmarks/server.py ${PORT}

test: clean
	echo "Running tests..."
	PYTHONPATH=`pwd` \
		nosetests -s --verbose --with-coverage --cover-package=mybookmarks tests/*
