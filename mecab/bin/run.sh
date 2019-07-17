#!/usr/bin/env bash

PROJECT_ID=`gcloud config list project --format "value(core.project)"`
BUCKET="gs://${PROJECT_ID}-dataflow"
JOB_NAME="mecab-example-`date '+%Y%m%d%H%M%S'`"

python -m pipeline.task \
  --project=${PROJECT_ID} \
  --job_name=${JOB_NAME} \
  --staging_location=${BUCKET}/staging \
  --temp_location=${BUCKET}/temp \
  --runner="DataflowRunner"
