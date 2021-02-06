#!/bin/sh

export ENCRYPTED_SECRET_FILEPATH=./secrets/encrypted/
export RAW_SECRET_FILEPATH=$HOME/secrets

# Authenticate using service account
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

# Set project id
# gcloud config set project $GOOGLE_CLOUD_PROJECT

# Create a version using the latest commit hash
export VERSION=$(git rev-parse --short HEAD)

# Create requirements.txt
pipenv lock -r > requirements.txt

# Rename Pipfile and Pipfile.lock
mv Pipfile Pipfile.txt
mv Pipfile.lock Pipfile.lock.txt

# Copy the raw credentials for deployment
mkdir ./secrets/raw/
cp $RAW_SECRET_FILEPATH/$SECRET_FILE ./secrets/raw/

# Deploy the application
gcloud -q app deploy $APP_YAML --version $VERSION --promote

# Delete the raw credentials from the repo to avoid accidental commit
rm -rf ./secrets/raw/

# Restore Pipfile and Pipfile.lock
mv Pipfile.txt Pipfile
mv Pipfile.lock.txt Pipfile.lock

# Delete requirements.txt
rm requirements.txt
