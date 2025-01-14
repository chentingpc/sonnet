# Copyright 2019 The Sonnet Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or  implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Tests copying Sonnet modules."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy

from absl.testing import parameterized
from sonnet.src import test_utils
from sonnet.src.conformance import goldens
import tensorflow as tf


class CopyTest(test_utils.TestCase, parameterized.TestCase):

  @goldens.all_goldens
  def test_copy(self, golden):
    m1 = golden.create_module()
    golden.create_all_variables(m1)
    m2 = copy.deepcopy(m1)
    self.assertIsNot(m1, m2)

    # Check that module variables are recreated with equivalent properties.
    for v1, v2 in zip(m1.variables, m2.variables):
      self.assertIsNot(v1, v2)
      if tf.version.GIT_VERSION == "unknown":
        # TODO(tomhennigan) Remove version check when TF 2.1 is released.
        self.assertEqual(v1.name, v2.name)
      self.assertEqual(v1.device, v2.device)
      self.assertAllEqual(v1.read_value(), v2.read_value())

    if golden.deterministic:
      y1 = golden.forward(m1)
      y2 = golden.forward(m2)
      tf.nest.map_structure(self.assertAllEqual, y1, y2)

if __name__ == "__main__":
  # tf.enable_v2_behavior()
  tf.test.main()
