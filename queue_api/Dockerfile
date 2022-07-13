FROM python:3.10-bullseye
RUN apt-get update && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa
#    apt install python 3.8 -y && \
#    update-alternatives -- install /usr/bin/python python /user/bin/python3.8 1 && \
#    update-alternatives -- set python /usr/bin/python3.8 && \
#    update-alternatives -- install /usr/bin/python3 python3 /user/bin/python3.8 1

RUN apt-get install -y \
    git
#    build-essential cargo
#    libpq-dev python3.8-dev \
#    python3-pip \

COPY queue_api /root/queue_api
COPY setup.py /root/
COPY requirements.txt /root/
COPY install.sh /root/

WORKDIR /root/

RUN python3 -m pip install -U pip
RUN ./install.sh
RUN mkdir -p /var/log/gunicorn

CMD gunicorn -w 2 \
    --bind 0.0.0.0:8080 \
    --error-logfile /var/log/gunicorn/error.log \
    --access-logfile /var/log/gunicorn/access.log \
    --capture-output \
    --log-level debug \
    --timeout 300 \
    "queue_api.app:create_app()"