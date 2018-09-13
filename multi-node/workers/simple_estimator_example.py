# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""A simple example to test the a DistributionStrategy with Estimators.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import tensorflow as tf


def build_model_fn_optimizer():
  """Simple model_fn with optimizer."""
  # TODO(anjalisridhar): Move this inside the model_fn once OptimizerV2 is
  # done?
  optimizer = tf.train.GradientDescentOptimizer(0.2)

  def model_fn(features, labels, mode):  # pylint: disable=unused-argument
    """model_fn which uses a single unit Dense layer."""
    # You can also use the Flatten layer if you want to test a model without any
    # weights.
    layer = tf.layers.Dense(1, use_bias=True)
    logits = layer(features)

    if mode == tf.estimator.ModeKeys.PREDICT:
      predictions = {"logits": logits}
      return tf.estimator.EstimatorSpec(mode, predictions=predictions)

    def loss_fn():
      y = tf.reshape(logits, []) - tf.constant(1.)
      return y * y

    if mode == tf.estimator.ModeKeys.EVAL:
      return tf.estimator.EstimatorSpec(mode, loss=loss_fn())

    assert mode == tf.estimator.ModeKeys.TRAIN

    global_step = tf.train.get_global_step()
    train_op = optimizer.minimize(loss_fn(), global_step=global_step)
    return tf.estimator.EstimatorSpec(mode,
                                      loss=loss_fn(),
                                      train_op=train_op)

  return model_fn


def model_main():
  def input_fn():
    features = tf.data.Dataset.from_tensors([[1.]]).repeat(10)
    labels = tf.data.Dataset.from_tensors(1.).repeat(10)
    return tf.data.Dataset.zip((features, labels))

  train_spec = tf.estimator.TrainSpec(input_fn=input_fn)
  eval_spec = tf.estimator.EvalSpec(input_fn=input_fn)

  distribution = tf.contrib.distribute.CollectiveAllReduceStrategy(
    num_gpus_per_worker=4)

  config = tf.estimator.RunConfig(
    train_distribute=distribution,
    session_config=tf.ConfigProto(
      # auto-use different device when operation not supported on assigned device
      # see https://github.com/tensorflow/tensorflow/issues/2285#issuecomment-217949259
      allow_soft_placement=True,
      log_device_placement=True)
  )

  estimator = tf.estimator.Estimator(
    model_fn=build_model_fn_optimizer(),
    config=config,
    model_dir="/scratch/leuven/319/vsc31962")

  tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)
