#!/bin/bash
BASEDIR=$(dirname $0)

pip3 install -r "${BASEDIR}"/requirements.txt
pip3 install -e "${BASEDIR}"