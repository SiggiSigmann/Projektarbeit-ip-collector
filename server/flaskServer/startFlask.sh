#!/bin/bash
#install requirement(most will be already installed in container tobiassigmann/ip_collector)
#to update use dockerfile and readme in createDockerContainer
pip3 install -r requirements.txt

#start flask server
python3 server.py