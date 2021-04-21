# Deployment

## Google Cloud Environment Setup
1. Create a Google Cloud project
    - <a id='gcp-project-id'>``GCP_PROJECT_ID``</a>
1. Create a Cloud Storage bucket
    - <a id='gs-bucket-name'>`GS_BUCKET_NAME`</a> - Google Cloud
        Storage bucket name
1. Create a Cloud SQL MySQL 2nd generation instance
    - Note the <a id='instance-connection-name'>`DATABASE_INSTANCE_CONNECTION_NAME`</a>
1. Create a database user
1. Create a database
1. Create 2 service accounts, create keys for them and save
   them in your local machine:
    - <a id='google-app-credentials'>`GOOGLE_APPLICATION_CREDENTIALS`</a> - a json file containing
        credentials for a Google Cloud service account with the following roles:
        - Storage Object Creator
        - Storage Object Viewer
    - <a id='app-engine-deployer'>`APP_ENGINE_DEPLOYER_SERVICE_ACCOUNT_FILE`</a>- a json file containing credentials for a Google Cloud
        service account with the following roles:
        - App Engine Deployer
        - App Engine Service Admin
        - Cloud Build Editor
        - Storage Object Creator
        - Storage Object Viewer 
1. Create an App Engine app

## App Engine Deployment
1. Set the required **environment variables**
1. Run `./scripts/deploy_to_app_engine.sh` in a Linux terminal.
    - Use Git bash or WSL if using Windows OS.

## Notes
- You need the Google Cloud SDK installed on your machine.
- [App Engine currently doesn't support `Pipfile`](https://cloud.google.com/appengine/docs/standard/python3/runtime#dependencies).
    Instead of doing the deployment manually, we recommend
    you use the utility script for deployment: `deploy_to_app_engine.sh`
    stored in the `scripts` directory. It does set up operations before
    deployment and clean up after deployment.
