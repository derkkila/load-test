FROM python:2.7-wheezy

# Install locust
RUN pip install pyzmq locustio faker

ADD locustfile.py /config/locustfile.py
ADD . /usr/local/bin
RUN chmod -R 775 /usr/local/bin/

ENV LOCUST_FILE /usr/local/bin/locustfile.py

EXPOSE 8089

ENTRYPOINT ["/usr/local/bin/runLocust.sh"]
