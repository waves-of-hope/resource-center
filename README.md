# Waves Resource Center
A digital platform for sharing educational resources

![Django CI](https://github.com/Waves-of-Hope-Foundation/resource-center/workflows/Django%20CI/badge.svg)

## Local Setup
1. Create the following [environment variables](#env-vars):
    - `SECRET_KEY`
    - `DEBUG`
    - `ALLOWED_HOSTS`
    - [`ADMINS`](https://docs.djangoproject.com/en/3.1/ref/settings/#admins)
    - [`MANAGERS`](https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-MANAGERS)
    - `EMAIL_HOST_USER` - a gmail account
    - `EMAIL_HOST_PASSWORD` - password to the gmail account
    - <a id='gs-bucket-name'>`GS_BUCKET_NAME`</a> - Google Cloud
        Storage bucket name
    - <a id='gs-sa-key'>`GS_SA_KEY`</a> - a json file containing
        credentials for a Google Cloud service account with the following roles:
        - Storage Object Creator
        - Storage Object Viewer 

1. Create and activate a **virtual environment** using [```pipenv```](https://pypi.org/project/pipenv/)
      by running ```$ pipenv shell```
1. Install the dependencies using ```$ pipenv install --dev```
1. Run database migrations using ```$ python manage.py migrate```
1. Run the tests using `$ python manage.py test`. 
    - Make sure you have `geckodriver` installed and in your `PATH` 
    before attempting to run the test.
    Read [selenium python docs](https://selenium-python.readthedocs.io/installation.html#drivers)
    for more information on how to do this.
    - You could also run `python manage.py test --exclude-tag=functional`
    to run unit tests only.

## Using Cloud SQL or local MySQL database:
1. Create the following [environment variables](#env-vars):
    - `INSTANCE_CONNECTION_NAME` - for Cloud SQL only
    - `DATABASE`
    - `USER`
    - `PASSWORD`

## Continuous Deployment to App Engine:
1. Ensure all previously indicated [environment variables](#env-vars)
    have been created
1. Create the following [environment variables](#env-vars):
    - `GCP_PROJECT_ID` - Google Cloud project ID
    - `GAE_SA_KEY`- a json file containing credentials for a Google Cloud
        service account with the following roles:
        - App Engine Deployer
        - App Engine Service Admin
        - Cloud Build Editor
        - Storage Object Creator
        - Storage Object Viewer 

1. Create `app.yaml` by running `$ python app.yaml.py`
1. Run `.github/scripts/deploy-gae.sh` in a Linux terminal.
    - Use Git bash or WSL if using Windows OS.

## Notes
-  <a id='env-vars'>Environment variables</a> can be stored in a
    `.env` file in the `resource-center` directory or `settings.ini`
    in the `resource_center` directory

- You need to provide your [`GS_BUCKET_NAME`](#gs-bucket-name)
    and [`GS_SA_KEY`](#gs-sa-key) for the project to work as is. 
    However, you can comment out the `DEFAULT_FILE_STORAGE` and 
    _Google Cloud Storage bucket_ settings to use a local `media`
    directory.