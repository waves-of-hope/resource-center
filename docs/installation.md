# Installation

## Required Software
1. Git
1. Python
1. Firefox web browser
1. Geckodriver
1. MySQL (preferably with MySQL workbench)

## Local Setup
1. Clone the repository
1. Create the following **environment variables**:
    - `SECRET_KEY`
    - `DATABASE`
    - `DB_USER`
    - `DB_PASSWORD`
    - `DJANGO_EMAIL_HOST_USER` - a gmail account
    - `DJANGO_EMAIL_HOST_PASSWORD` - password to the gmail account

1. Create and activate a virtual environment using `pipenv`
   by running `$ pipenv shell`
1. Install dev dependencies by running `$ pipenv install --dev`
1. Run the tests using `$ python manage.py test
   --settings=resource_center.settings.test`. 
    - Make sure you have `geckodriver` installed and in your `PATH` 
    before attempting to run the test.
    Read [selenium python docs](https://selenium-python.readthedocs.io/installation.html#drivers)
    for more information on how to do this.
    - You could also add this flag `--exclude-tag=functional`
    to run unit tests only.

## Notes
-  **Environment variables** can be stored in a `.env` file in the
   repository root. `Pipenv` automatically sets the variables defined
   in `.env` as environment variables when the virtual environment is activated.
