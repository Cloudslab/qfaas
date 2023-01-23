#!/bin/bash

source .env
curl -sSL ${QFAAS_URL_OPENFAAS} | sh

cd /app
git clone https://${QFAAS_USER_GITLAB}:${QFAAS_PASSWORD_GITLAB}@${QFAAS_URL_GITLAB}
cd /app/qfaas-fn
git checkout dev
git config --global user.email "${QFAAS_EMAIL_GITLAB}"

cd /app
# uvicorn qfaas.core.app:app --host 0.0.0.0 --port=5000 --root-path /api
export PYTHONPATH=$PWD
python qfaas/main.py
