

0. Add project wide ssh key for `ubuntu` user.
1. Set gcloud default project `gcloud config set project <my-project>`
2. Deploy rabbitmq: `gcloud deployment-manager deployments create rabbit-1 --template rabbitmq_vm.py`
3. Create Google storage bucket
4. Create worker service account with `Storage Object Admin` and `Logs Writer` roles.
5. For local development you need to specify environment variables GOOGLE_APPLICATION_CREDENTIALS, RABBITMQ_HOST
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

6. Stop the machine and create image. Or don't stop, create snapshot and then image from snapshot.
7. Delete instance from step 6
8. Create instance template.
Machine type: f1-micro
Boot disk: custom image from previous step
Service account: from step 4
Startup script:
```
cd /home/ubuntu
export RABBITMQ_HOST=$(curl "http://metadata.google.internal/computeMetadata/v1/instance/attributes/RABBITMQ_HOST" -H "Metadata-Flavor: Google")
source venv/bin/activate
cd animals
git branch
git pull origin
pip install -r requirements.txt
pip install -r requirements_cluster.txt
cd animals
PYTHONPATH=$(pwd) nohup python cluster/worker.py &
```
Metadata:
    Name: RABBITMQ
    Value: <ip address from rabbitmq instance from step 2>
Preemptibility: On

9. Create instance group.
Location: Single zone - europe-west4-a
Instance template: from step 8
Autoscaling mode: Don't autoscale
Number of instances: How much do you want
Autohealing: No health check 

10. Establish ssh tunnel to rabbitmq management server: `ssh -L 5672:localhost:5672 -L 15672:localhost:15672 ubuntu@<ip>`
While this session open you can access RabbitMQ management WEB UI via http://localhost:15672/

11. Add new task 
Go to Queues -> task_queue -> Publish message
Example of body:
`{"snapshot_dir": "gs://animals-cluster-1/world3/", "max_cycle": 5000, "cycle_amount": 1000}`

12. You can check worker logs in stackdriver logging with filter `resource.type="global"`. However it works pretty bad.


# todo: control autoscaling group via worker -> pubsub -> cloud function -> change autoscaling group
# todo: or via custom metric in stackdriver deriving rabbitmq queue length (questionable). Autoscaling via CPU works bad
# todo: migrate workers to containers with COS VMs, so logging will be better and reliable, but will require buidling phase
