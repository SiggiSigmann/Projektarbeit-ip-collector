#!/bin/bash
#start venv and run server script

python3 -m venv .

source bin/activate

pip install -r requirements.txt

python server.py

deactivate
