import time
import json
import argparse
from jtop import jtop
import paho.mqtt.client as mqtt


def parse_args():
    parser = argparse.ArgumentParser(description="Control smart furniture by LLM")
    parser.add_argument("--mqtt_broker_ip", type=str, default='192.168.49.109', help="IP of mqtt broker")  # 192.168.49.104
    parser.add_argument("--mqtt_broker_port", type=int, default=1883, help="Port of mqtt broker")
    parser.add_argument("--cpu_core_num", type=int, default=8, help="Port of mqtt broker")
    args = parser.parse_args()
    return args


class MQTT:
    def __init__(self, mqtt_broker="192.168.49.74", mqtt_port=1883):
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.connect(mqtt_broker, mqtt_port)
        self.client.loop_start()

    def send_msg(self, topic, message):
        try:
            self.client.publish(topic, message)
        except:
            pass

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    def release(self):
        self.client.loop_stop()
        self.client.disconnect()


def main_loop(args):
    try:
        mqtt_client = MQTT(mqtt_broker=args.mqtt_broker_ip, mqtt_port=args.mqtt_broker_port)
        jetson = jtop()
        jetson.start()
        while jetson.ok():
            data = jetson.stats
            del data['time'] 
            del data['uptime']

            CPU = 0
            for i in range(1, args.cpu_core_num + 1):
                CPU += data[f'CPU{i}']
                CPU /= 2
                del data[f'CPU{i}']

            data['CPU']=round(CPU, 2)
            payload = json.dumps(data)
            mqtt_client.send_msg("/sys_info", payload)
            print(data)
    finally:
        jetson.close()
        mqtt_client.release()
        print("Main loop closed!")



if __name__ == '__main__':
    args = parse_args()
    while True:
        main_loop(args)
        time.sleep(2)


