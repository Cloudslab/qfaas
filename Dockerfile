FROM python:3.10.3

RUN apt update
RUN apt install -y git curl gawk
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.24.0/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl
# COPY .kube/config ~/.kube/config

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY qfaas-fn /app/qfaas-functions
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

COPY . .

EXPOSE 5000

CMD ["./entrypoint.sh"]
