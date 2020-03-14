#!/usr/bin/env bash

gcloud deployment-manager deployments create rabbit-1 --template rabbitmq_vm.py
