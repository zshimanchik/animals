## Documentation (notes) for cluster deployment in google cloud

For local development you need to specify environment variables GOOGLE_APPLICATION_CREDENTIALS, RABBITMQ_HOST


0. Add project wide ssh key for `ubuntu` user.
1. Set gcloud default project `gcloud config set project <my-project>`
2. Deploy rabbitmq: `rabbitmq/deploy.sh`
3. Create Metadata entry in Project. Compute Engine -> Metadata -> Edit -> Add
Metadata:
    Name: `RABBITMQ`
    Value: `rabbit-1-rabbitmq-vm-py.europe-west1-b.c.animals-cluster-1.internal`
Value should match with instance name & zone created on step 2
4. Create Google storage bucket
5. Create worker service account with `Storage Object Admin` and `Logs Writer` roles.
6. Create worker VM image
Machine type: f1-micro
Boot disk: Ubuntu 18.04 LTS Minimal
7. Ssh to machine with `ubuntu` user and execute:
```
sudo apt update
sudo apt install python3.8 python3-pip git
pip3 install virtualenv
source ~/.profile
virtualenv --python=python3.8 venv
source ./venv/bin/active
pip install ipython
git clone https://github.com/zshimanchik/animals.git
cd animals
# checkout necessary branch
git checkout feature/google-cluster
pip install -r requirements.txt
pip install -r requirements_cluster.txt
```

8. Stop the machine and create image. Or don't stop, create snapshot and then image from snapshot.
9. Delete instance from step 6
10. Create instance template.
Machine type: f1-micro
Boot disk: custom image from step 8
Service account: from step 5
Preemptibility: On
Startup script:
```
cd /home/ubuntu
export RABBITMQ_HOST=$(curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/project/attributes/RABBITMQ_HOST)
export GCE_PROJECT=$(curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/project/project-id)
export GCE_ZONE=$(curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/zone | cut -d'/' -f4)
export GCE_INSTANCE_GROUP=$(curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/attributes/created-by | cut -d'/' -f6)

source venv/bin/activate
cd animals
git fetch origin
git checkout origin/animals-with-smells
pip install -r requirements.txt
pip install -r requirements_cluster.txt
cd animals
PYTHONPATH=$(pwd) nohup python cluster/worker.py &
```

11. Create instance group.
Location: Single zone - europe-west4-a
Instance template: from step 10
Autoscaling mode: Don't autoscale
Number of instances: How much do you want
Autohealing: No health check 

12. Establish ssh tunnel to rabbitmq management server: `ssh -L 5672:localhost:5672 -L 15672:localhost:15672 ubuntu@<ip>`
While this session open you can access RabbitMQ management WEB UI via http://localhost:15672/
Username and password: `guest`

13. Add new task
Via script that will add job into task_queue and send command to pubsub to increate cluster size:
`python publish.py gs://animals-cluster-1/world_201121_$(git rev-parse --short HEAD)_01/ 5000 1000 -p animals-cluster-1 -z europe-west1-b -i instance-group-2`
`python publish.py gs://animals-cluster-1/world_201121_$(git rev-parse --short HEAD)_02/ 10000 2000 -p animals-cluster-1 -z us-central1-a -i instance-group-3`
or without scaling cluster:
`python publish.py gs://animals-cluster-1/world_201121_$(git rev-parse --short HEAD)_03/ 10000 2000`

Or via rabbitmq WEB UI http://localhost:15672/, note it will not increase cluster size:
Go to: Queues -> task_queue -> Publish message
Example of body:
`{"snapshot_dir": "gs://animals-cluster-1/world3/", "max_cycle": 5000, "cycle_amount": 1000}`

14. You can check worker logs in stackdriver logging with filter `resource.type="global"`. However it works pretty bad.


Done: autoscaling via worker -> pubsub -> cloud function -> change autoscaling group

todo: or via custom metric in stackdriver deriving rabbitmq queue length (questionable). Autoscaling via CPU works bad
todo: or via cronjob, that will fetch queue length and resize instance group
todo: migrate workers to containers with COS VMs, so logging will be better and reliable, but will require buidling phase
