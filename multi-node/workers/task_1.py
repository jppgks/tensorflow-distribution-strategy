import tensorflow as tf
import os
import json

tf_config = os.environ.get('CLUSTER_SPEC')
tf_config_json = json.loads(tf_config)
cluster = tf.train.ClusterSpec(tf_config_json)
server = tf.train.Server(cluster, job_name="worker", task_index=1)

