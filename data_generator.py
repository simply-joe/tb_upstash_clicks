import json
from faker import Faker
from kafka import KafkaProducer
import argparse

fake = Faker()

def generate_demo_data():
    data = {
        "linkId": fake.random_int(min=1, max=100),
        "ip": fake.ipv4(),
        "userAgent": fake.user_agent(),
        "deviceType": fake.random_element(elements=("desktop", "mobile", "tablet")),
        "sourceUrl": fake.url(),
        "previousUrl": fake.url(),
        "redirectTargetUrl": fake.url(),
        "meta": json.dumps({"country_code": fake.country_code()}),
    }
    return data

def send_to_kafka(producer, topic, data):
    producer.send(topic, json.dumps(data).encode('utf-8'))

def main():
    parser = argparse.ArgumentParser(description='Generate and send demo data to Kafka.')
    parser.add_argument('--topic', required=True, help='Kafka topic to send data to')
    parser.add_argument('--username', required=True, help='Kafka SASL username')
    parser.add_argument('--password', required=True, help='Kafka SASL password')
    parser.add_argument('--amount', type=int, default=1, help='Amount of data to send to Kafka')

    args = parser.parse_args()

    kafka_bootstrap_servers = ['sweeping-ant-9955-us1-kafka.upstash.io:9092']
    
    kafka_producer = KafkaProducer(
        bootstrap_servers=kafka_bootstrap_servers,
        sasl_mechanism='SCRAM-SHA-256',
        security_protocol='SASL_SSL',
        sasl_plain_username=args.username,
        sasl_plain_password=args.password,
    )

    kafka_topic = args.topic

    for _ in range(args.amount):
        demo_data = generate_demo_data()
        send_to_kafka(kafka_producer, kafka_topic, demo_data)

    # Close the Kafka producer
    kafka_producer.close()

if __name__ == "__main__":
    main()
