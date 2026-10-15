# Copyright (c) 2026, Intel Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Reference tests for the norm-scale and N-D argument helpers."""

import math

import numpy as np
import pytest
from numpy.testing import assert_allclose

import mkl_fft
from mkl_fft._fft_utils import _compute_fwd_scale, _cook_nd_args


@pytest.mark.parametrize("norm", [None, "backward"])
@pytest.mark.parametrize("n", [None, 8, [4, 5]])
def test_scale_backward_is_one(norm, n):
    assert _compute_fwd_scale(norm, n, (3, 7)) == 1.0


@pytest.mark.parametrize("bad", ["Forward", "none", "", 1, "orthonormal"])
def test_scale_invalid_norm(bad):
    with pytest.raises(ValueError, match="Invalid norm value"):
        _compute_fwd_scale(bad, 8, 8)


@pytest.mark.parametrize(
    "n, shape, total",
    [
        (8, 100, 8),
        (np.int64(12), 100, 12),
        (np.int32(5), 3, 5),
        ([2, 3, 4], None, 24),
        ((6, 5), None, 30),
        (np.array([3, 7]), None, 21),
        (np.array(9), None, 9),
        (None, 10, 10),
        (None, (4, 5), 20),
        (None, [2, 2, 2], 8),
    ],
)
def test_scale_forward_and_ortho(n, shape, total):
    assert_allclose(_compute_fwd_scale("forward", n, shape), 1.0 / total)
    assert_allclose(
        _compute_fwd_scale("ortho", n, shape), 1.0 / math.sqrt(total)
    )


def test_scale_n_takes_precedence_over_shape():
    assert_allclose(_compute_fwd_scale("forward", 4, 1000), 0.25)
    assert_allclose(_compute_fwd_scale("ortho", (2, 8), (100, 100)), 0.25)


@pytest.mark.parametrize("norm", ["forward", "ortho"])
def test_scale_zero_length(norm):
    assert _compute_fwd_scale(norm, 0, 5) == 1
    assert _compute_fwd_scale(norm, [3, 0], None) == 1


@pytest.mark.parametrize("norm", ["forward", "ortho", "backward"])
def test_scale_matches_numpy_1d(norm):
    x = np.random.default_rng(1).standard_normal(12)
    assert_allclose(
        mkl_fft.fft(x, n=10, norm=norm), np.fft.fft(x, n=10, norm=norm)
    )
    assert_allclose(mkl_fft.ifft(x, norm=norm), np.fft.ifft(x, norm=norm))


a3 = np.zeros((4, 5, 6))


def test_cook_defaults():
    s, axes = _cook_nd_args(a3)
    assert s == [4, 5, 6]
    assert list(axes) == [-3, -2, -1]


@pytest.mark.parametrize(
    "axes, expected_s",
    [([0], [4]), ([2, 0], [6, 4]), ([-1, 1], [6, 5]), ((1,), [5])],
)
def test_cook_axes_only(axes, expected_s):
    s, ax = _cook_nd_args(a3, axes=axes)
    assert s == expected_s
    assert list(ax) == list(axes)


@pytest.mark.parametrize(
    "s, expected_axes",
    [([7], [-1]), ((7, 8), [-2, -1]), ([1, 2, 3], [-3, -2, -1])],
)
def test_cook_shape_only(s, expected_axes):
    s_out, ax = _cook_nd_args(a3, s=s)
    assert s_out == list(s)
    assert list(ax) == expected_axes


def test_cook_shape_and_axes():
    s, ax = _cook_nd_args(a3, s=(3, 9), axes=(2, 0))
    assert s == [3, 9]
    assert list(ax) == [2, 0]


def test_cook_returns_list_shape():
    s, _ = _cook_nd_args(a3, s=(2, 2))
    assert isinstance(s, list)


@pytest.mark.parametrize(
    "s, axes", [((2, 3), (0,)), ((2,), (0, 1)), (None, (0, 5)), (None, (7,))]
)
def test_cook_length_mismatch_or_bad_axis(s, axes):
    with pytest.raises(ValueError, match="different lengths"):
        _cook_nd_args(a3, s=s, axes=axes)


def test_cook_invreal_default_length():
    s, ax = _cook_nd_args(a3, invreal=True)
    assert s == [4, 5, 10]
    s, ax = _cook_nd_args(a3, axes=(2, 1), invreal=True)
    # the last axis given is the one whose output length is 2 * (n - 1)
    assert s == [6, 8]
    assert list(ax) == [2, 1]


def test_cook_invreal_explicit_shape_is_kept():
    s, ax = _cook_nd_args(a3, s=(3, 7), axes=(0, 2), invreal=True)
    assert s == [3, 7]
    s, ax = _cook_nd_args(a3, s=(5,), invreal=True)
    assert s == [5]
    assert list(ax) == [-1]


@pytest.mark.parametrize("norm", ["forward", "ortho"])
def test_nd_scale_matches_numpy(norm):
    x = np.random.default_rng(2).standard_normal((4, 5, 6))
    assert_allclose(
        mkl_fft.fftn(x, axes=(0, 2), norm=norm),
        np.fft.fftn(x, axes=(0, 2), norm=norm),
    )
    y = np.fft.rfftn(x)
    assert_allclose(
        mkl_fft.irfftn(y, norm=norm), np.fft.irfftn(y, norm=norm)
    )
