import paho.mqtt.client as mqtt

class MQTTAdapter:
    def __init__(self, broker_address):
        self.client = mqtt.Client()
        self.client.connect(broker_address)

    def publish(self, topic, message):
        self.client.publish(topic, message)
