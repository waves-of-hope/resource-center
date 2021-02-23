# Google Cloud Command Reference

- Create a project: \
    `$ gcloud projects create [PROJECT_ID] --name=[PROJECT_NAME]`

- Create/set a billing account for the project
  * Only done via Cloud Shell

- Create a service account:
    ```
    $ gcloud iam service-accounts create [SERVICE_ACCOUNT_ID] \
      > --description="DESCRIPTION" \
      > --display-name="DISPLAY_NAME"
    ```

- Add an IAM policy to a service account:
    ```
    $ gcloud projects add-iam-policy-binding [PROJECT_ID] \
      > --member="serviceAccount:SERVICE_ACCOUNT_ID@PROJECT_ID.iam.gserviceaccount.com" \
      > --role="ROLE_NAME"
    ```

- List all service accounts:
\
    `$ gcloud iam service-accounts list`

- List all Google Cloud regions: \
    `$ gcloud compute regions list`

- Set a default region/zone for the project: \
    `$ gcloud config set compute/region [REGION]`

- Enable the Cloud Storage service: \
    `$ gcloud services enable storage-component.googleapis.com`

- Create a bucket: \
    `$ gsutil mb gs://[BUCKET_NAME]`

- Create a Cloud SQL instance:
    ```
    $ gcloud sql instances create [INSTANCE_NAME] \
      > --region=[REGION] --tier=[TIER] \
      > --backup-start-time=[BACKUP_START_TIME] \
      > --storage-auto-increase
    ```

- Enable the SQL Admin API (to use the Cloud SQL proxy): \
    `$ gcloud services enable sqladmin.googleapis.com`

- List App Engine regions: \
    `$ gcloud app regions list`

- Create an app: \
    `$ gcloud app create --region=[REGION]`

- Enable the App Engine Admin API: \
    `$ gcloud services enable appengine.googleapis.com`

- Enable the Cloud Datastore API: \
    `$ gcloud services enable datastore.googleapis.com`
