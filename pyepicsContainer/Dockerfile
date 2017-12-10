FROM sdmolloy/epics-basic
MAINTAINER Stephen Molloy <sdmolloy@gmail.com>

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python3.6 python3-pip && \
    pip3 install -r requirements.txt

COPY pyepics /opt/app/
