#!/bin/sh

export ENCRYPTED_SECRET_FILEPATH=./secrets/encrypted/
export RAW_SECRET_FILEPATH=$HOME/secrets

# different settings for CI
if "$CI" == true; then
    # use a different raw secret directory in GitHub actions
    export RAW_SECRET_FILEPATH=./secrets/raw
else
    # Authenticate using service account
    gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

    # Copy the raw credentials for deployment
    mkdir ./secrets/raw/
    cp $RAW_SECRET_FILEPATH/$GOOGLE_CLOUD_SERVICE_ACCOUNT_FILE ./secrets/raw/
fi

# Set project id
gcloud config set project $GOOGLE_CLOUD_PROJECT

# Create a version using the latest commit hash
export VERSION=$(git rev-parse --short HEAD)

# Create requirements.txt
pipenv lock -r > requirements.txt

# Rename Pipfile and Pipfile.lock
mv Pipfile Pipfile.txt
mv Pipfile.lock Pipfile.lock.txt

# Add the environment variables to app.yaml
echo "" >> app.yaml
echo "env_variables:" >> app.yaml
echo "  ADMINS: ${ADMINS}" >> app.yaml
echo "  ADMIN_URL: ${ADMIN_URL}" >> app.yaml
echo "  ALLOWED_HOSTS: $ALLOWED_HOSTS" >> app.yaml
echo "  DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY}" >> app.yaml

echo "  DATABASE_INSTANCE_CONNECTION_NAME: ${DATABASE_INSTANCE_CONNECTION_NAME}" >> app.yaml
echo "  DB_NAME: ${DB_NAME}" >> app.yaml
echo "  DB_USER: ${DB_USER}" >> app.yaml
echo "  DB_PASSWORD: ${DB_PASSWORD}" >> app.yaml
echo "  DJANGO_DEBUG: ${DJANGO_DEBUG}" >> app.yaml

echo "  DJANGO_EMAIL_HOST_USER: ${DJANGO_EMAIL_HOST_USER}" >> app.yaml
echo "  DJANGO_EMAIL_HOST_PASSWORD: ${DJANGO_EMAIL_HOST_PASSWORD}" >> app.yaml

echo "  GCP_STORAGE_BUCKET_NAME: ${GCP_STORAGE_BUCKET_NAME}" >> app.yaml
echo "  GOOGLE_APPLICATION_CREDENTIALS: secrets/raw/${GOOGLE_CLOUD_SERVICE_ACCOUNT_FILE}" >> app.yaml

# Deploy the application
gcloud -q app deploy app.yaml --version $VERSION

# Undo changes made to app.yaml
git checkout -- app.yaml

# Delete the raw credentials from the repo to avoid accidental commit
rm -rf ./secrets/raw/

# Restore Pipfile and Pipfile.lock
mv Pipfile.txt Pipfile
mv Pipfile.lock.txt Pipfile.lock

# Delete requirements.txt
rm requirements.txt
