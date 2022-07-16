FROM python:3.9-bullseye
RUN apt-get update && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa

RUN apt-get install -y git

COPY queue_service /root/queue_service
COPY setup.py /root/
COPY requirements.txt /root/
COPY install.sh /root/

WORKDIR /root/

RUN python3 -m pip install -U pip
RUN ./install.sh

CMD ["python", "queue_service/queue_service.py"]
