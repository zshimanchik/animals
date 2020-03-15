import argparse
import logging
import os
import subprocess as sp

from google.cloud import pubsub_v1
import pika
import json

logger = logging.getLogger(__name__)
QUEUE = 'task_queue'
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS', 'guest')


def change_cluster_size(increment=1):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('animals-cluster-1', 'change-cluster-size')
    publisher.publish(topic_path, b'', increment=str(increment)).result()
    print('Sent signal to increase cluster size')


def publish_job_to_queue(snapshot_dir, max_cycle, cycle_amount, latest_tick=None):
    message = {
        "snapshot_dir": snapshot_dir,
        "max_cycle": max_cycle,
        "cycle_amount": cycle_amount,
        "latest_tick": latest_tick,
    }

    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent %r" % message)
    connection.close()


def get_git_hash():
    result = sp.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, check=True, encoding='utf8')
    return result.stdout.strip()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir", help="Path to bucket directory where results will be stored.")
    parser.add_argument("max_cycle", type=int, help="Limit of world time.")
    parser.add_argument("cycle_amount",
                        type=int,
                        help="How many cycles worker will calculate before saving result. Job size.")
    parser.add_argument("-l", "--latest_tick",
                        type=int,
                        help="If specified worker will load world from '{snapshot_dir}/{latest_tick}.wlrd'",
                        required=False,
                        default=None)
    args = parser.parse_args()
    publish_job_to_queue(args.snapshot_dir, args.max_cycle, args.cycle_amount, args.latest_tick)
    change_cluster_size()
