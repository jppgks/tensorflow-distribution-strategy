import sys

import json
import os
import tensorflow as tf

tf_cluster = os.environ.get('CLUSTER_SPEC')
tf_cluster_json = json.loads(tf_cluster)
os.environ["TF_CONFIG"] = json.dumps({
  "cluster": tf_cluster_json,
  "task": {"type": "worker", "index": 0}
})
sys.stdout.write(os.environ["TF_CONFIG"])

tf.contrib.distribute.run_standard_tensorflow_server().join()
