#!/usr/bin/env bash

set -ex

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${DIR}

test -f "${DIR}/google-credentials.json"

export GOOGLE_APPLICATION_CREDENTIALS="${DIR}/google-credentials.json"
cd animals
export PYTHONPATH=$(pwd)

if [[ -f ../venv/bin/activate ]]; then
    ../venv/bin/python cluster/worker.py
else
    pipenv run python cluster/worker.py
fi


