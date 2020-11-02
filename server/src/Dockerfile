FROM python:3.8

COPY requirements.txt .
COPY execute.sh .

RUN pip install -r requirements.txt

COPY server.py .


CMD [ "./execute.sh" ] 
CMD tail -f /dev/null