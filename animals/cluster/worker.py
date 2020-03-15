import functools
import json
import logging
import os
import sys
import threading
import time

import pika

import cluster.google_serializer as serializer
from cluster.publish import change_cluster_size
from engine.world import World
from engine.world_constants import WorldConstants

logger = logging.getLogger(__name__)
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS', 'guest')
QUEUE_NAME = 'task_queue'


def ack_message(channel, delivery_tag, new_message=None):
    """Note that `channel` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if channel.is_open:
        if new_message is not None:
            channel.basic_publish(
                exchange='',
                routing_key=QUEUE_NAME,
                body=new_message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
        else:
            change_cluster_size(-1)
        channel.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        logger.error('Trying to ack_message, but channel is closed.')


def do_work(connection, channel, delivery_tag, job):
    logger.info(f'Worker begin. Delivery tag: {delivery_tag}. Raw job: {job!r}')
    # Parse job
    job = json.loads(job)
    snapshot_dir = job['snapshot_dir']
    latest_tick = job.get('latest_tick')
    cycle_amount = job.get('cycle_amount', 1000)
    max_cycle = job.get('max_cycle', 10_000)

    # Load or Create world
    if latest_tick:
        save_path = os.path.join(snapshot_dir, f'{latest_tick}.wrld')
        logger.info(f'Loading from {save_path}')
        world = serializer.load(save_path)
    else:
        logger.info(f'Creating new world {snapshot_dir}')
        world = World(WorldConstants())
        save_path = os.path.join(snapshot_dir, '0.wrld')
        serializer.save(world, save_path)

    world_start_time = world.time
    stop_world = False
    logger.info(f'World {save_path} calculating for {cycle_amount}. max_cycle {max_cycle}')
    start_time = time.time()
    # Calculate world
    for _ in range(cycle_amount):
        world.update()
        if world.time >= max_cycle or len(world.animals) == 0:
            stop_world = True
            break

    # Analyzing performance
    elapsed = time.time() - start_time
    performance = elapsed / ((world.time - world_start_time) or 1)
    logger.info(f'World {save_path} calculated: {world.time} wtime, {elapsed:.3f}s elapsed, '
                 f'{performance:.6f} performance')
    # Saving world
    save_path = os.path.join(snapshot_dir, f'{world.time}.wrld')
    logger.info(f'Saving {save_path}')
    serializer.save(world, save_path)

    # Preparing new job
    if not stop_world:
        job['latest_tick'] = world.time
        new_job = json.dumps(job)
    else:
        logger.info(f'World {save_path} is finished')
        new_job = None

    logger.info(f'Worker done. Delivery tag: {delivery_tag}. new_message: {new_job}')
    cb = functools.partial(ack_message, channel, delivery_tag, new_message=new_job)
    connection.add_callback_threadsafe(cb)


def on_message(channel, method_frame, header_frame, body, args):
    (connection, threads) = args
    logger.info('on_message begin. delivery_tag=%r, body=%r', method_frame.delivery_tag, body)
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(connection, channel, delivery_tag, body))
    t.start()
    threads.append(t)
    logger.info('on_message done. delivery_tag=%r', method_frame.delivery_tag)


if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s [%(name)s:%(lineno)-3d] %(levelname)-7s: %(message)s'
    logging.basicConfig(level=logging.WARNING, format=LOG_FORMAT, stream=sys.stdout)
    logger.setLevel(logging.DEBUG)

    import google.cloud.logging

    # Instantiates a client
    client = google.cloud.logging.Client()

    # Connects the logger to the root logging handler; by default this captures
    # all logs at INFO level and higher
    client.setup_logging()

    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(RABBITMQ_HOST, credentials=credentials, heartbeat=60)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)  # having more than one will influence on random.state

    threads = []
    on_message_callback = functools.partial(on_message, args=(connection, threads))
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message_callback)

    logger.info('Listening for new messages from rabbitmq...')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    # Wait for all to complete
    for thread in threads:
        thread.join()

    connection.close()
