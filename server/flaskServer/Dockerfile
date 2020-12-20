FROM python:3.8

COPY requirements.txt .
COPY execute.sh .
COPY server.py .
COPY tracert.py .
COPY plotter.py .
COPY static/* static/
COPY html/* html/
COPY dbconnector/* dbconnector/

EXPOSE 80

ENTRYPOINT [ "./execute.sh" ]