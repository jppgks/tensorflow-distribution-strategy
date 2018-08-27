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
chief=($hosts)
chief=${chief[0]}
# Chief and task attributes may be redundant when using MirroredStrategy
# only added this because TF complained that we were using TF_CONFIG without specifying those attributes
export CLUSTER_SPEC='{"worker": '"$worker_string"'}'
echo 'CLUSTER_SPEC: '"$CLUSTER_SPEC"
#export TF_CONFIG='{"cluster": {"chief": ["'"$chief"':2222"], "worker": '"$worker_string"'}, "task": {"type": "chief", "index": 0}}'
#echo 'TF_CONFIG: '"$TF_CONFIG"

