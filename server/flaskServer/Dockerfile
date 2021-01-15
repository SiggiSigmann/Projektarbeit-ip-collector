FROM tobiassigmann/ip_collector:latest

COPY requirements.txt .
COPY execute.sh .
COPY server.py .
COPY tracert.py .
COPY plotter.py .
COPY subnetze.py .
COPY evaluation.py .
COPY static/* static/
COPY html/* html/
COPY files/* files/
COPY dbconnector/* dbconnector/

EXPOSE 80

ENTRYPOINT [ "./execute.sh" ]