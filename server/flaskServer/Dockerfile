FROM python:3.8

COPY requirements.txt .
COPY execute.sh .
COPY server.py .

RUN pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT [ "./execute.sh" ]

#Only if ENTRYPOINT stops => CMD tail -f /dev/null

