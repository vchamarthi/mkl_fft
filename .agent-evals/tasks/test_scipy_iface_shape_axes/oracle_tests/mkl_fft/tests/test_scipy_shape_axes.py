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

"""Reference tests for shape/axes handling of the SciPy interface."""

import numpy as np
import pytest

pytest.importorskip("scipy")

import mkl_fft.interfaces.scipy_fft as mfft  # noqa: E402
from mkl_fft.interfaces._scipy_fft import (  # noqa: E402
    _init_nd_shape_and_axes,
)

x3 = np.zeros((4, 5, 6))


def test_defaults_use_all_axes():
    shape, axes = _init_nd_shape_and_axes(x3, None, None)
    assert shape == (4, 5, 6)
    assert axes == [0, 1, 2]


def test_return_types():
    shape, axes = _init_nd_shape_and_axes(x3, [3, 3], [0, 1])
    assert isinstance(shape, tuple)
    assert isinstance(axes, list)


@pytest.mark.parametrize(
    "axes, expected_axes, expected_shape",
    [
        ([0], [0], (4,)),
        ([2, 0], [2, 0], (6, 4)),
        ([-1], [2], (6,)),
        ([-3, -2], [0, 1], (4, 5)),
        (1, [1], (5,)),
        (np.int64(-1), [2], (6,)),
        ((np.int32(0), 2), [0, 2], (4, 6)),
    ],
)
def test_axes_only(axes, expected_axes, expected_shape):
    shape, ax = _init_nd_shape_and_axes(x3, None, axes)
    assert ax == expected_axes
    assert shape == expected_shape


@pytest.mark.parametrize(
    "shape, expected_shape, expected_axes",
    [
        ([7], (7,), [2]),
        ([7, 8], (7, 8), [1, 2]),
        ([1, 2, 3], (1, 2, 3), [0, 1, 2]),
        (9, (9,), [2]),
        ([-1, 3], (5, 3), [1, 2]),
        ([3, -1], (3, 6), [1, 2]),
    ],
)
def test_shape_only(shape, expected_shape, expected_axes):
    s, ax = _init_nd_shape_and_axes(x3, shape, None)
    assert s == expected_shape
    assert list(ax) == expected_axes


@pytest.mark.parametrize(
    "shape, axes, expected_shape, expected_axes",
    [
        ([3, 2], [0, 2], (3, 2), [0, 2]),
        ([-1, 2], [-3, 1], (4, 2), [0, 1]),
        ([2, -1], [2, 0], (2, 4), [2, 0]),
        (8, 1, (8,), [1]),
    ],
)
def test_shape_and_axes(shape, axes, expected_shape, expected_axes):
    s, ax = _init_nd_shape_and_axes(x3, shape, axes)
    assert s == expected_shape
    assert ax == expected_axes


@pytest.mark.parametrize(
    "axes", [[3], [-4], [0, 3], [0, -4], [10]]
)
def test_axes_out_of_range(axes):
    with pytest.raises(ValueError, match="exceeds dimensionality"):
        _init_nd_shape_and_axes(x3, None, axes)


@pytest.mark.parametrize("axes", [[0, 0], [1, -2], [2, 0, -1]])
def test_axes_not_unique(axes):
    with pytest.raises(ValueError, match="unique"):
        _init_nd_shape_and_axes(x3, None, axes)


@pytest.mark.parametrize("axes", [[0.5], ["a"], [0, 1.0]])
def test_axes_not_integers(axes):
    with pytest.raises(ValueError, match="axes must be a scalar or iterable"):
        _init_nd_shape_and_axes(x3, None, axes)


@pytest.mark.parametrize("shape", [[2.5], [2, "b"], 3.0])
def test_shape_not_integers(shape):
    with pytest.raises(ValueError, match="shape must be a scalar or iterable"):
        _init_nd_shape_and_axes(x3, shape, None)


def test_shape_axes_length_mismatch():
    with pytest.raises(ValueError, match="same length"):
        _init_nd_shape_and_axes(x3, [2, 3], [0])
    with pytest.raises(ValueError, match="same length"):
        _init_nd_shape_and_axes(x3, [2], [0, 1])


def test_shape_longer_than_ndim():
    with pytest.raises(ValueError, match="more axes than are present"):
        _init_nd_shape_and_axes(x3, [1, 2, 3, 4], None)
    # exactly ndim is fine
    s, _ = _init_nd_shape_and_axes(x3, [1, 2, 3], None)
    assert s == (1, 2, 3)


@pytest.mark.parametrize("shape", [[0], [3, 0], [-2], [1, -3]])
def test_invalid_number_of_points(shape):
    with pytest.raises(ValueError, match="invalid number of data points"):
        _init_nd_shape_and_axes(x3, shape, None)


def test_invreal_default_last_axis_length():
    s, ax = _init_nd_shape_and_axes(x3, None, None, invreal=True)
    assert s == (4, 5, 10)
    assert ax == [0, 1, 2]
    s, ax = _init_nd_shape_and_axes(x3, None, [2, 0], invreal=True)
    # the last axis in `axes` is the one whose length is 2 * (n - 1)
    assert s == (6, 6)
    assert ax == [2, 0]
    s, ax = _init_nd_shape_and_axes(x3, None, [-2], invreal=True)
    assert s == (8,)
    assert ax == [1]


def test_invreal_explicit_shape_is_kept():
    s, ax = _init_nd_shape_and_axes(x3, [3, 7], [0, 2], invreal=True)
    assert s == (3, 7)
    assert ax == [0, 2]
    s, _ = _init_nd_shape_and_axes(x3, [-1], None, invreal=True)
    assert s == (6,)


def test_invreal_length_one_last_axis():
    y = np.zeros((4, 1))
    with pytest.raises(ValueError, match="invalid number of data points"):
        _init_nd_shape_and_axes(y, None, None, invreal=True)


def test_public_functions_use_it():
    x = np.random.default_rng(0).standard_normal((4, 5, 6))
    assert mfft.fftn(x, s=[3, -1], axes=[0, 2]).shape == (3, 5, 6)
    assert mfft.irfftn(mfft.rfftn(x)).shape == (4, 5, 6)
    assert mfft.irfftn(mfft.rfftn(x), axes=[-2]).shape == (4, 8, 4)
    with pytest.raises(ValueError, match="unique"):
        mfft.fftn(x, axes=[1, 1])
    with pytest.raises(ValueError, match="exceeds dimensionality"):
        mfft.ifftn(x, axes=[3])
