import os
import sys

from confluent_kafka import Producer

sasl_mechanism = 'PLAIN'
security_protocol = 'SASL_SSL'

TOPIC_NAME = 'qoi0pdec-default'


class KafkaProducerClient:

    def __init__(self) -> None:
        conf = {
            'bootstrap.servers': os.environ['CLOUDKARAFKA_BROKERS'],
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': os.environ['CLOUDKARAFKA_USERNAME'],
            'sasl.password': os.environ['CLOUDKARAFKA_PASSWORD']
        }

        self.producer = Producer(**conf)

    def delivery_callback(self, err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s [%d]\n' %
                             (msg.topic(), msg.partition()))

    def send_message(self, message):
        self.producer.produce(TOPIC_NAME, str(message), callback=self.delivery_callback)
        self.producer.poll(0)
        self.producer.flush()
