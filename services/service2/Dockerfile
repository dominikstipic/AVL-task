FROM python:latest

RUN curl -sL https://github.com/openfaas/classic-watchdog/releases/download/0.2.2/fwatchdog-amd64 > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog

ENV fprocess="python entrypoint.py"
COPY entrypoint.py /

RUN pip install requests

EXPOSE 8083
CMD [ "fwatchdog" ]