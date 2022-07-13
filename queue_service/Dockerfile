FROM ubuntu:18.04
RUN apt-get update && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt install python 3.8 -y && \
    update-alternatives -- install /usr/bin/python python /user/bin/python3.8 1 && \
    update-alternatives -- set python /usr/bin/python3.8 && \
    update-alternatives -- install /usr/bin/python3 python3 /user/bin/python3.8 1

RUN apt-get install -y \
    libpq-dev python3.8-dev \
    python3-pip git \
    build-essential cargo

COPY queue_service /root/queue_service
COPY setup.py /root/
COPY requirements.txt /root/
COPY install.sh /root/

WORKDIR /root/

RUN python3 -m pip install -U pip
RUN ./install.sh

# more to add here