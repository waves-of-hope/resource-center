#!/bin/sh

export ENCRYPTED_SECRET_FILEPATH=./secrets/encrypted/
export RAW_SECRET_FILEPATH=$HOME/secrets

# Authenticate using service account
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

# Set project id
gcloud config set project $GOOGLE_CLOUD_PROJECT

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

# Add the environment variables to app.yaml
echo "env_variables:" >> $APP_YAML
echo "  ADMINS: ${ADMINS}" >> $APP_YAML
echo "  ADMIN_URL: ${ADMIN_URL}" >> $APP_YAML
echo "  ALLOWED_HOSTS: $ALLOWED_HOSTS" >> $APP_YAML
echo "  DATABASE_INSTANCE_CONNECTION_NAME: ${DATABASE_INSTANCE_CONNECTION_NAME}" >> $APP_YAML
echo "  DATABASE: ${DATABASE}" >> $APP_YAML
echo "  DB_USER: ${DB_USER}" >> $APP_YAML
echo "  DB_PASSWORD: ${DB_PASSWORD}" >> $APP_YAML
echo "  DJANGO_DEBUG: ${DJANGO_DEBUG}" >> $APP_YAML
echo "  DJANGO_EMAIL_HOST_USER: ${DJANGO_EMAIL_HOST_USER}" >> $APP_YAML
echo "  DJANGO_EMAIL_HOST_PASSWORD: ${DJANGO_EMAIL_HOST_PASSWORD}" >> $APP_YAML
echo "  DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY}" >> $APP_YAML
echo "  GCP_STORAGE_BUCKET_NAME: ${GCP_STORAGE_BUCKET_NAME}" $APP_YAML
echo "  GOOGLE_APPLICATION_CREDENTIALS: secrets/raw/${SECRET_FILE}" >> $APP_YAML

# Deploy the application
gcloud -q app deploy $APP_YAML --version $VERSION

# Undo changes made to app.yaml
git checkout -- $APP_YAML

# Delete the raw credentials from the repo to avoid accidental commit
rm -rf ./secrets/raw/

# Restore Pipfile and Pipfile.lock
mv Pipfile.txt Pipfile
mv Pipfile.lock.txt Pipfile.lock

# Delete requirements.txt
rm requirements.txt
