from googleapiclient.discovery import build

PROJECT = 'animals-cluster-1'
ZONE = 'europe-west1-b'
INSTANCE_GROUP = 'instance-group-2'

def entrypoint(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print(f'event: {event!r}, context: {context}')
    increment = int(event['attributes']['increment'])
    print(f'increment: {increment}')

    service = build('compute', 'v1', cache_discovery=False)
    result = service.instanceGroupManagers().get(
        project=PROJECT, zone=ZONE, instanceGroupManager=INSTANCE_GROUP
    ).execute()
    target_size = result['targetSize']
    print(f'current targetSize: {target_size}',)
    target_size += increment
    print(f'new targetSize: {target_size}')

    result = service.instanceGroupManagers().resize(
        project=PROJECT, zone=ZONE, instanceGroupManager=INSTANCE_GROUP, size=target_size
    ).execute()
    print(f'result {result}')
