
# Please note, the tag of the base image must match the jtop version in the host machine.
FROM rbonghi/jetson_stats:4.2.3

WORKDIR /opt/
COPY . /opt/

RUN pip3 install --no-cache-dir --verbose paho-mqtt==1.6.1

# CMD python3 /opt/jetson-status.py

