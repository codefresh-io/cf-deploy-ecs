FROM python:2.7


ENV SHELL /bin/bash

RUN pip install boto3 && echo "/cfecs" > /usr/local/lib/python2.7/site-packages/cf.pth

COPY cfecs-update /
COPY cfecs/ cfecs/

ENTRYPOINT ["/cfecs-update"]