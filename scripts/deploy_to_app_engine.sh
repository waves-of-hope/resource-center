#!/bin/sh

# Authenticate using service account
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

# Set project id
# gcloud config set project $GOOGLE_CLOUD_PROJECT

# Create a version using the latest commit hash
export VERSION=$(git rev-parse --short HEAD)

# Create requirements.txt
pipenv lock -r > requirements.txt

# Rename Pipfile and Pipfile.lock
mv Pipfile secrets/raw/
mv Pipfile.lock secrets/raw/

# Deploy the application
gcloud -q app deploy $APP_YAML --version $VERSION --promote

# Restore Pipfile and Pipfile.lock
mv secrets/raw/Pipfile .
mv secrets/raw/Pipfile.lock .

# Delete requirements.txt
rm requirements.txt
