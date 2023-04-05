# FROM python:3.9.10-slim-buster
# RUN pip3 install cirq
FROM python:3.9.10-slim-bullseye

RUN apt-get update \
&& pip install --upgrade pip \
&& rm -rf /var/lib/apt/lists/*

# Add non root user
RUN addgroup --system app && adduser app --system --ingroup app
USER app

ENV PATH=$PATH:/home/app/.local/bin
RUN pip install --user cirq