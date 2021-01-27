FROM tobiassigmann/ip_collector:latest

COPY requirements.txt .
COPY startFlask.sh .
COPY server.py .
COPY tracert.py .
COPY plotter.py .
COPY subnet.py .
COPY evaluation.py .
COPY static/* static/
COPY html/* html/
COPY files/* files/
COPY dbconnector/* dbconnector/

EXPOSE 80

ENTRYPOINT [ "./startFlask.sh" ]