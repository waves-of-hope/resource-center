#!/bin/sh

# Authenticate using service account
gcloud auth activate-service-account --key-file=$GAE_SA_KEY

# Set project id
gcloud config set project $GCP_PROJECT_ID

# Create a version using the latest commit hash
export VERSION=$(git rev-parse --short HEAD)

# Deploy the application
gcloud -q app deploy app.yaml --version $VERSION --promote