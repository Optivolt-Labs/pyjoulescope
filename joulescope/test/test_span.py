# Copyright 2018 Jetperch LLC
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

"""
Test spans
"""

import unittest
from joulescope.span import Span
import numpy as np


class TestSpan(unittest.TestCase):

    def test_trivial(self):
        s = Span([0.0, 20.0], 1.0, 11)
        self.assertEqual(20.0, s.s_limit_max)
        self.assertEqual(10.0, s.a_limit_min)
        self.assertEqual([1.0, 11.0], s.conform([1.0, 11.0]))
        self.assertEqual(1.0, s.quants_per([1.0, 11.0]))
        self.assertEqual(([1.0, 11.0], 1.0), s.conform_quant_per([1.0, 11.0]))
        span, steps_per, axis = s.conform_discrete([1.0, 11.0])
        self.assertEqual([1.0, 11.0], span)
        self.assertEqual(1.0, steps_per)
        self.assertEqual([1.0, 11.0], s.scale([1.0, 11.0]))

    def test_conform_discrete_range_trim(self):
        s = Span([10.0, 30.0], 1.0, 11)
        sc, spans_per, x = s.conform_discrete([0.0, 40.0])
        np.testing.assert_allclose([10.0, 30.0], sc)
        self.assertEqual(2, spans_per)
        np.testing.assert_allclose(np.arange(10, 31, 2, dtype=np.float), x)

    def test_conform_discrete_min_gain(self):
        s = Span([10.0, 30.0], 1.0, 11)
        sc, spans_per, x = s.conform_discrete([19.5, 20.5])
        np.testing.assert_allclose([10, 20], sc)
        self.assertEqual(1, spans_per)
        np.testing.assert_allclose(np.arange(10, 21, dtype=np.float), x)