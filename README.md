

docker run -d --restart=always -v /run/:/run/ jetson_stats_gtc:latest python3 -m jetson-status --mqtt_broker_ip 192.168.49.109 --mqtt_broker_port 1883 --cpu_core_num 8

-v /home/seeed/Desktop/jetson-status/jetson-status.py:/opt/jetson-status.py
docker build -f Dockerfile . -t jetson_stats_gtc
