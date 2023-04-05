FROM ghcr.io/openfaas/of-watchdog:0.9.11 as watchdog
FROM mcr.microsoft.com/quantum/iqsharp-base:latest

USER root
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

ARG ADDITIONAL_PACKAGE
# Alternatively use ADD https:// (which will not be cached by Docker builder)

RUN apt-get -qy update && apt-get --no-install-recommends -qy install ${ADDITIONAL_PACKAGE} && rm -rf /var/lib/apt/lists/*

USER jovyan

ENV PATH=$PATH:/home/jovyan/.local/bin

WORKDIR /home/jovyan/

COPY index.py           .
COPY requirements.txt   .

RUN pip install -r requirements.txt

USER root
RUN chown jovyan:jovyan index.py

USER jovyan

# Build the function directory and install any user-specified components

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /home/jovyan/function/
COPY function/requirements.txt	.
RUN pip install --user -r requirements.txt
COPY --chown=jovyan:jovyan function/*.qs /home/jovyan/

#install function code
USER root

# Reduce size https://medium.com/@lmakarov/the-backlash-of-chmod-chown-mv-in-your-dockerfile-f12fe08c0b55
COPY --chown=jovyan:jovyan function/   .

USER jovyan
ARG TEST_COMMAND=tox
ARG TEST_ENABLED=false
RUN if [ "$TEST_ENABLED" = "false" ]; then \
    echo "skipping tests";\
    else \
    eval "$TEST_COMMAND"; \
    fi

WORKDIR /home/jovyan/

# #configure WSGI server and healthcheck
ENV fprocess="python index.py"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]