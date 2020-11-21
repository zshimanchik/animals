from googleapiclient.discovery import build


def entrypoint(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print(f'event: {event!r}, context: {context}')
    increment = int(event['attributes']['increment'])
    project = event['attributes']['project']  # example: 'animals-cluster-1'
    zone = event['attributes']['zone']  # example: 'europe-west1-b'
    instance_group = event['attributes']['instance_group']  # example: 'instance-group-2'
    print(f'increment: {increment} project: {project} zone: {zone} instance_group: {instance_group}')

    service = build('compute', 'v1', cache_discovery=False)
    result = service.instanceGroupManagers().get(
        project=project, zone=zone, instanceGroupManager=instance_group
    ).execute()
    target_size = result['targetSize']
    print(f'current targetSize: {target_size}',)
    target_size += increment
    print(f'new targetSize: {target_size}')

    result = service.instanceGroupManagers().resize(
        project=project, zone=zone, instanceGroupManager=instance_group, size=target_size
    ).execute()
    print(f'result {result}')
