#!/bin/bash

# Store hostnames of assigned nodes
hosts=$(cat $PBS_NODEFILE | tr "\n" " ")

# Construct ClusterSpec
worker_string="["
for hostname in $hosts; do
  worker_string+="\"$hostname"':2222", '
done
worker_string=${worker_string::-2}
worker_string+="]"

export CLUSTER_SPEC='{"worker": '"$worker_string"'}'
echo 'CLUSTER_SPEC: '"$CLUSTER_SPEC"
