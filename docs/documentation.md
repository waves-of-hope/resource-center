# Documentation

## Building Documentation
1. Activate the development virtual environment
1. Change the current directory to the docs folder within
    the repository by running `$ cd docs`
1. Run `$ ./make clean` to remove any docs previously built
1. Run `$ ./make html` to build the docs in HTML format
1. Change the current directory to the location of the built docs
    by running `$ cd _build/html`
1. Start the Python static files server by running
    `$ python -m http.server`
1. Visit `localhost:8000` in your browser to view the docs

## Generating the Documentation
1. Activate the development virtual environment
1. Generate the docs by running `$ sphinx apidoc -o docs .`
