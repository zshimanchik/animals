import functools
import json
import logging
import os
import sys
import threading
import time
from logging import Formatter

import pika

import cluster.google_serializer as serializer
from cluster.publish import change_cluster_size
from engine.world import World
from engine.world_constants import WorldConstants

_LOGGER = logging.getLogger(__name__)
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS', 'guest')
GCE_PROJECT = None
GCE_ZONE = None
GCE_INSTANCE_GROUP = None
QUEUE_NAME = 'task_queue'
SIGTERM = False
SIGUSR1 = False


def do_work_wrapper(connection, channel, delivery_tag, job):
    try:
        return do_work(connection, channel, delivery_tag, job)
    except Exception as ex:
        _LOGGER.exception("Catched exception in do_work. %s. Doing harakiri.", ex, exc_info=ex)
        connection.add_callback_threadsafe(harakiri)


def do_work(connection, channel, delivery_tag, job):
    global SIGTERM
    global SIGUSR1
    _LOGGER.info(f'Worker begin. Delivery tag: {delivery_tag}. Raw job: {job!r}')
    # Parse job
    job = json.loads(job)
    snapshot_dir = job['snapshot_dir']
    latest_tick = job.get('latest_tick')
    cycle_amount = job.get('cycle_amount', 1000)
    max_cycle = job.get('max_cycle', 10_000)

    # Load or Create world
    if latest_tick:
        save_path = os.path.join(snapshot_dir, f'{latest_tick}.wrld')
        _LOGGER.info(f'Loading from {save_path}')
        world = serializer.load(save_path)
    else:
        _LOGGER.info(f'Creating new world {snapshot_dir}')
        world = World(WorldConstants())
        save_path = os.path.join(snapshot_dir, '0.wrld')
        serializer.save(world, save_path)

    world_start_time = world.time
    stop_world = False
    _LOGGER.info(f'World {save_path} calculating for {cycle_amount}. max_cycle {max_cycle}')
    start_time = time.time()
    # Calculate world
    for _ in range(cycle_amount):
        world.update()
        if world.time >= max_cycle or len(world.animals) == 0:
            stop_world = True
            break

        if SIGTERM is True:
            _LOGGER.warning("SIGTERM received in worker. Finishing it.")
            break

        if SIGUSR1 is True:
            _LOGGER.info(f"Current world {save_path} time is {world.time}")
            SIGUSR1 = False

    # Analyzing performance
    elapsed = time.time() - start_time
    performance = elapsed / ((world.time - world_start_time) or 1)
    _LOGGER.info(f'World: {save_path}, calculated: {world.time - world_start_time} ticks, '
                 f'world.time: {world.time} ticks, elapsed: {elapsed:.3f}s, performance: {performance:.6f} s/tick')
    # Saving world
    save_path = os.path.join(snapshot_dir, f'{world.time}.wrld')
    _LOGGER.info(f'Saving {save_path}')
    serializer.save(world, save_path)

    # Preparing new job
    if not stop_world:
        job['latest_tick'] = world.time
        new_job = json.dumps(job)
    else:
        _LOGGER.info(f'World {save_path} is finished')
        new_job = None

    _LOGGER.info(f'Worker done. Delivery tag: {delivery_tag}. new_message: {new_job}')
    cb = functools.partial(ack_message, channel, delivery_tag, new_message=new_job)
    connection.add_callback_threadsafe(cb)


def on_message(channel, method_frame, header_frame, body, args):
    (connection, threads) = args
    _LOGGER.info('on_message begin. delivery_tag=%r, body=%r', method_frame.delivery_tag, body)
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work_wrapper, args=(connection, channel, delivery_tag, body))
    t.start()
    threads.append(t)
    _LOGGER.info('on_message done. delivery_tag=%r', method_frame.delivery_tag)


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
            if GCE_INSTANCE_GROUP:
                _LOGGER.info('Sending signal to decrease cluster size')
                change_cluster_size(-1, GCE_PROJECT, GCE_ZONE, GCE_INSTANCE_GROUP)
            else:
                _LOGGER.info('This worker is not part of the instance_group. Skipping cluster size decrease.')

        channel.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        _LOGGER.error('Trying to ack_message, but channel is closed.')


def harakiri():
    _LOGGER.error("Doing haraiki")
    sys.exit(1)


def handle_sigterm(signalNumber, frame):
    global SIGTERM
    _LOGGER.warning('Received SIGTERM: %s', signalNumber)
    _LOGGER.info('Stopping consuming')
    channel.stop_consuming()
    SIGTERM = True


def handle_sigusr1(signalNumber, frame):
    global SIGUSR1
    _LOGGER.warning('Received SIGUSR1: %s', signalNumber)
    SIGUSR1 = True


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGUSR1, handle_sigusr1)

    import string
    import random

    worker_id = ''.join(random.choice(string.ascii_letters) for _ in range(10))

    import google.cloud.logging
    from google.cloud.logging.handlers.handlers import CloudLoggingHandler, EXCLUDED_LOGGER_DEFAULTS
    google_logging_client = google.cloud.logging.Client()

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(Formatter(
        f'%(asctime)s {worker_id} [%(name)s:%(lineno)-3d] %(levelname)-7s: %(message)s'))

    google_handler = CloudLoggingHandler(google_logging_client)
    google_handler.setFormatter(Formatter(f'{worker_id} [%(name)s:%(lineno)-3d] %(levelname)-7s: %(message)s'))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(google_handler)

    for logger_name in EXCLUDED_LOGGER_DEFAULTS:
        logger = logging.getLogger(logger_name)
        logger.propagate = False
        logger.addHandler(stdout_handler)

    os.environ.get('RABBITMQ_HOST', 'localhost')

    GCE_PROJECT = os.environ.get('GCE_PROJECT')
    GCE_ZONE = os.environ.get('GCE_ZONE')
    GCE_INSTANCE_GROUP = os.environ.get('GCE_INSTANCE_GROUP')
    _LOGGER.info(f'Current GCE_PROJECT: {GCE_PROJECT} GCE_ZONE: {GCE_ZONE} GCE_INSTANCE_GROUP: {GCE_INSTANCE_GROUP}')
    if any([GCE_PROJECT, GCE_ZONE, GCE_INSTANCE_GROUP]) and not all([GCE_PROJECT, GCE_ZONE, GCE_INSTANCE_GROUP]):
        _LOGGER.exception('All GCE parameters must be provided')
        sys.exit(1)

    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(RABBITMQ_HOST, credentials=credentials, heartbeat=60)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)  # having more than one will influence on random.state

    threads = []
    on_message_callback = functools.partial(on_message, args=(connection, threads))
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message_callback)

    _LOGGER.info('Listening for new messages from rabbitmq...')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        _LOGGER.info("KeyboardInterrupt sent. Stopping conusming RabbitMQ")
        channel.stop_consuming()

    # Wait for all to complete
    _LOGGER.info("Waiting for all threads to finish")
    for thread in threads:
        thread.join()

    connection.close()
