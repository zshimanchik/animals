COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'
REGION = 'europe-west4'
ZONE = REGION + '-a'

container_manifest = '''
spec:
  containers:
    - name: rabbit
      image: 'docker.io/rabbitmq:3-management-alpine'
      stdin: false
      tty: false
  restartPolicy: Always
'''


def GenerateConfig(context):
  """Generate configuration."""

  res = []
  base_name = context.env['deployment'] + '-' + context.env['name']

  # Properties for the container-based instance.
  instance = {
      'zone': ZONE,
      'machineType': 'projects/{project}/zones/{zone}/machineTypes/f1-micro'.format(
          project=context.env['project'],
          zone=ZONE
      ),
      'metadata': {
          'items': [
              {
                  'key': 'gce-container-declaration',
                  'value': container_manifest,
              }, {
                  'key': 'google-logging-enabled',
                  'value': True,
              }
          ]
      },
      'disks': [{
          'deviceName': 'boot',
          'type': 'PERSISTENT',
          'autoDelete': True,
          'boot': True,
          'initializeParams': {
              'diskSizeGb': 10,
              'sourceImage': 'projects/cos-cloud/global/images/cos-stable-80-12739-91-0',
          },
      }],
      'networkInterfaces': [{
          'accessConfigs': [{
              'name': 'external-nat',
              'type': 'ONE_TO_ONE_NAT'
          }],
          'subnetwork': 'projects/{project}/regions/{region}/subnetworks/default'.format(
              project=context.env['project'],
              region=REGION
          ),
      }],
      'serviceAccounts': [{
          'email': 'default',
          'scopes': [
            "https://www.googleapis.com/auth/logging.write",
            "https://www.googleapis.com/auth/monitoring.write"
          ]
      }]
  }
  res.append({
      'name': base_name,
      'type': 'compute.v1.instance',
      'properties': instance
  })
  # Resources to return.
  resources = {
      'resources': res,
  }

  return resources
