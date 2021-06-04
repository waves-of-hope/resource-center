#!/bin/bash

export ENCRYPTED_SECRET_FILEPATH=./secrets/encrypted/
export RAW_SECRET_FILEPATH="$HOME"/secrets

# different settings for CI
if "$CI" == true; then
    # use a different raw secret directory in GitHub actions
    export RAW_SECRET_FILEPATH=./secrets/raw
else
    # Authenticate using service account
    gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"

    # Copy the raw credentials for deployment
    mkdir ./secrets/raw/
    cp "$RAW_SECRET_FILEPATH"/"$GOOGLE_CLOUD_SERVICE_ACCOUNT_FILE" ./secrets/raw/
    export GOOGLE_APPLICATION_CREDENTIALS=./secrets/raw/"$GOOGLE_CLOUD_SERVICE_ACCOUNT_FILE"
fi

# Set project id
gcloud config set project "$GOOGLE_CLOUD_PROJECT"

# Create a version using the latest commit hash
export VERSION=$(git rev-parse --short HEAD)

# Create requirements.txt
pipenv lock -r > requirements.txt

# Rename .env, Pipfile and Pipfile.lock
if test -e ".env"; then
    mv .env env.txt
fi
mv Pipfile Pipfile.txt
mv Pipfile.lock Pipfile.lock.txt

# Add the environment variables to app.yaml
echo "" >> app.yaml
echo "env_variables:" >> app.yaml

env_variables=(
    # Django
    "ADMINS"
    "ADMIN_URL"
    "ALLOWED_HOSTS"
    "DJANGO_DEBUG"
    "DJANGO_SECRET_KEY"

    # Database
    "DATABASE_INSTANCE_CONNECTION_NAME"
    "DATABASE_URL"
    "DB_ENGINE"
    "DB_NAME"
    "DB_USER"
    "DB_PASSWORD"

    # Email
    "DJANGO_EMAIL_HOST_USER"
    "DJANGO_EMAIL_HOST_PASSWORD"

    # File storage
    "GCP_STORAGE_BUCKET_NAME"
    "GOOGLE_APPLICATION_CREDENTIALS"
)

for var in "${env_variables[@]}"; do
    # get the environment variable string(key) and actual value
    case "$var" in
        *"CREDENTIALS"* | *"PASSWORD"* | *"SECRET"* | *"URL"*)
            echo "  $var: '${!var}'" >> app.yaml
            ;;

        *)
            echo "  $var: ${!var}" >> app.yaml
            ;;
    esac
done

# Deploy the application
gcloud -q app deploy app.yaml --version $VERSION

# Undo changes made to app.yaml
git checkout -- app.yaml

# Delete the raw credentials from the repo to avoid accidental commit
rm -rf ./secrets/raw/

# Restore .env, Pipfile and Pipfile.lock
if test -e "env.txt"; then
    mv env.txt .env
fi
mv Pipfile.txt Pipfile
mv Pipfile.lock.txt Pipfile.lock

# Delete requirements.txt
rm requirements.txt
