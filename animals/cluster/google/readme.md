


0. Deploy rabbitmq: `gcloud deployment-manager deployments create rabbit-1 --template rabbitmq_vm.py`
0. Create Google storage bucket
0. Create worker service account with persmissions to read-write from bucket
0. Specify environment variables GOOGLE_APPLICATION_CREDENTIALS, RABBITMQ_HOST

## Create worker VM image


Create micro instance with Ubuntu 18.04 LTS Minimal:
add ssh key during creation or project wide ssh key for `ubuntu` user.

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
pip3 install -r requirements.txt
```

Stop the machine and create image. Or don't stop, create snapshot and then image from snapshot.


