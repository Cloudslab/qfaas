#!/bin/bash

source .env
curl -sSL ${QFAAS_URL_OPENFAAS} | sh

# cd /app
# git clone https://oauth2:${QFAAS_GITLAB_API_TOKEN}@${QFAAS_URL_GITLAB}
# cd /app/qfaas-functions
# git checkout main
# git config --global user.email "${QFAAS_EMAIL_GITLAB}"

cd /app
# uvicorn qfaas.core.app:app --host 0.0.0.0 --port=5000 --root-path /api
export PYTHONPATH=$PWD
python qfaas/main.py