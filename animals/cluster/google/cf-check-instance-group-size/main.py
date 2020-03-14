import requests
from googleapiclient.discovery import build

RABBITMQ_HOST = 'rabbit-1-rabbitmq-vm-py.europe-west1-b.c.animals-cluster-1.internal'


def entrypoint(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print('event: ', event, ' context: ', context)
    print(f'RABBITMQ_HOST: {RABBITMQ_HOST!r}')
    response = requests.get(f'http://{RABBITMQ_HOST}:15672/api/queues/', auth=('guest', 'guest'))
    response.raise_for_status()
    rabbitmq_message_count = response.json()[0]['messages']
    print(f'rabbitmq message count {rabbitmq_message_count}')

    service = build('compute', 'v1', cache_discovery=False)
    request = service.instanceGroupManagers().get(
        project='animals-cluster-1', zone='europe-west1-b', instanceGroupManager='instance-group-2'
    )
    result = request.execute()
    print('rresult ', result)
    print('targetSize: ', result['targetSize'])
