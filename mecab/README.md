# MeCab and NEologd on Dataflow

## Setup

### Install Python Packages

```bash
pip install -r requirements.txt
```

### Set Variables

```bash
PROJECT_ID="<Your Project ID>"
BUCKET="gs://${PROJECT_ID}-dataflow"
JOB_NAME="mecab-example-`date '+%Y%m%d%H%M%S'`"
```
### Create Google Cloud Storage Bucket

```bash
gsutil mb ${BUCKET}
```

## Run on Dataflow

```bash
python -m pipeline.task \
  --project=${PROJECT_ID} \
  --job_name=${JOB_NAME} \
  --staging_location=${BUCKET}/staging \
  --temp_location=${BUCKET}/temp \
  --runner="DataflowRunner"
```
