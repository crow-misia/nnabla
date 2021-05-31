# Copyright (c) 2017 Sony Corporation. All Rights Reserved.
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

#
# *WARNING*
# THIS FILE IS AUTO-GENERATED BY CODE GENERATOR.
# 1. IMPLEMENT BACKWARD WRT INPUTS OF THE CORRESPONDING FUNCTION
# 2. IMPLEMENT BACKWARD_FUNCTION_CLASS IF NECESSARY (see e.g., affine.py)
# 3. UPDATE THE MAPPING IF NECESSARY (see function_backward_functions.py.tmpl)


import nnabla.functions as F

from .pow_scalar import pow_scalar_backward
from .add_scalar import add_scalar_backward
from .mul2 import mul2_backward
from .sum import sum_backward


def weight_normalization_backward(inputs, dim=0, eps=1e-12):
    """
    Args:
      inputs (list of nn.Variable): Incomming grads/inputs to/of the forward function.
      kwargs (dict of arguments): Dictionary of the corresponding function arguments.

    Return:
      list of Variable: Return the gradients wrt inputs of the corresponding function.
    """
    dy = inputs[0]
    w = inputs[1]
    g = inputs[2]

    # Reshape for F.mul2 broadcasting
    gshape = g.shape
    rgshape = [1 if i != dim else w.shape[dim] for i in range(w.ndim)]
    g = F.reshape(g, rgshape)

    # Create axes for F.sum
    sum_axes = list(filter(lambda x: x != dim, range(w.ndim)))

    # Recompute intermediate data of composite graph
    # pow -> sum -> add -> pow -> mul -> mul
    w_pow = F.pow_scalar(w, 2.0)
    w_sum = F.sum(w_pow, sum_axes, True)
    w_add = F.add_scalar(w_sum, eps)
    w_norm_inv = F.pow_scalar(w_add, -0.5)
    w_wn = F.mul2(w, w_norm_inv)
    # y = F.mul2(w_wn, g)

    # Backprop composite functions
    # pow <- sum <- add <- pow <- mul <- mul
    dw, dg = mul2_backward([dy, w_wn, g])
    dw, dw_mid = mul2_backward([dw, w, w_norm_inv])
    dw_mid = pow_scalar_backward([dw_mid, w_add], -0.5)
    dw_mid = add_scalar_backward([dw_mid, w_sum], eps)
    dw_mid = sum_backward([dw_mid, w_pow], sum_axes, True)
    dw_mid = pow_scalar_backward([dw_mid, w], 2.0)

    dw += dw_mid

    # Reshape to original shape of `g`
    dg = F.reshape(dg, gshape)
    return dw, dg
