#!/bin/sh

#start venv and run server script
python3 -m venv .

source bin/activate

pip3 install -r requirements.txt

python3 server.py

deactivate
