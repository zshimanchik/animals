#!/usr/bin/env bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$BASEDIR"

gcloud functions deploy cf-change-cluster-size \
    --entry-point=entrypoint \
    --region=europe-west1 \
    --ignore-file=deploy.sh \
    --memory=128 \
    --runtime=python37 \
    --max-instances=1 \
    --trigger-topic=change-cluster-size \
    --quiet
