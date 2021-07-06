# Copyright 2019,2020,2021 Sony Corporation.
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

import pytest
import numpy as np
import nnabla.functions as F
from nbla_test_utils import list_context

ctxs = list_context('ATan2')


@pytest.mark.parametrize("ctx, func_name", ctxs)
@pytest.mark.parametrize("seed", [313])
def test_atan_forward_backward(seed, ctx, func_name):
    from nbla_test_utils import function_tester
    rng = np.random.RandomState(seed)
    inputs = [rng.randn(2, 3, 4).astype(np.float32) * 1]
    inputs += [rng.randn(2, 3, 4).astype(np.float32) * 1]
    function_tester(rng, F.atan2, np.arctan2, inputs, ctx=ctx, func_name=func_name,
                    atol_f=1e-3, atol_b=1e-2)


@pytest.mark.parametrize("ctx, func_name", ctxs)
@pytest.mark.parametrize("seed", [313])
def test_atan2_double_backward(seed, ctx, func_name):
    from nbla_test_utils import cap_ignore_region, backward_function_tester
    rng = np.random.RandomState(seed)
    inputs = [rng.randn(2, 3, 4).astype(np.float32) * 1]
    inputs += [rng.randn(2, 3, 4).astype(np.float32) * 1]
    backward_function_tester(rng, F.atan2,
                             inputs=inputs,
                             func_args=[], func_kwargs={},
                             atol_accum=3e-2,
                             dstep=1e-3,
                             ctx=ctx)
