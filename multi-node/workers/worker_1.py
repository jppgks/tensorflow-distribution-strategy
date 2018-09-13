from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

import json
import os
from .simple_estimator_example import model_main

tf_cluster = os.environ.get('CLUSTER_SPEC')
tf_cluster_json = json.loads(tf_cluster)
os.environ["TF_CONFIG"] = json.dumps({
  "cluster": tf_cluster_json,
  "task": {"type": "worker", "index": 1}
})
sys.stdout.write(os.environ["TF_CONFIG"])

model_main()
