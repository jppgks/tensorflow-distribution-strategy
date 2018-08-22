import tensorflow as tf
import os
import json

tf_config = os.environ.get('TF_CONFIG')
tf_config_json = json.loads(tf_config)
cluster = tf_config_json.get('cluster')
cluster = tf.train.ClusterSpec(cluster)
server = tf.train.Server(cluster, job_name="worker", task_index=0)

