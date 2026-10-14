# Copyright (c) 2017, Intel Corporation
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

import pytest

from mkl_fft._fft_utils import _remove_axis

# (s, axes, axis_to_remove, expected_s, expected_axes)
_CASES = [
    # remove the last / first / middle entry of identity axes
    ((4, 5, 6), (0, 1, 2), -1, (4, 5), (0, 1)),
    ((4, 5, 6), (0, 1, 2), 2, (4, 5), (0, 1)),
    ((4, 5, 6), (0, 1, 2), 0, (5, 6), (0, 1)),
    ((4, 5, 6), (0, 1, 2), 1, (4, 6), (0, 1)),
    ((4, 5, 6), (0, 1, 2), -2, (4, 6), (0, 1)),
    ((4, 5, 6), (0, 1, 2), -3, (5, 6), (0, 1)),
    # negative axes are normalized to non-negative ones
    ((4, 5, 6), (-3, -2, -1), -1, (4, 5), (0, 1)),
    ((4, 5, 6), (-3, -2, -1), 0, (5, 6), (0, 1)),
    ((4, 5, 6), (-3, -2, -1), 1, (4, 6), (0, 1)),
    ((4, 5, 6), (0, -2, 2), 1, (4, 6), (0, 1)),
    # permuted axes: axes above the removed one shift down by one
    ((4, 5, 6), (2, 0, 1), 0, (5, 6), (0, 1)),
    ((4, 5, 6), (2, 0, 1), 1, (4, 6), (1, 0)),
    ((4, 5, 6), (2, 0, 1), 2, (4, 5), (1, 0)),
    ((4, 5, 6), (1, 2, 0), 0, (5, 6), (1, 0)),
    ((4, 5, 6), (1, 2, 0), 1, (4, 6), (1, 0)),
    ((4, 5, 6), (1, 2, 0), -1, (4, 5), (0, 1)),
    ((4, 5, 6), (2, 1, 0), 1, (4, 6), (1, 0)),
    ((4, 5, 6), (2, 1, 0), 0, (5, 6), (1, 0)),
    ((4, 5, 6), (2, 1, 0), 2, (4, 5), (1, 0)),
    # two and one dimensional inputs
    ((5, 6), (-1, -2), -1, (5,), (0,)),
    ((5, 6), (-1, -2), 0, (6,), (0,)),
    ((5, 6), (0, 1), 0, (6,), (0,)),
    ((5, 6), (1, 0), 1, (5,), (0,)),
    ((7,), (0,), 0, (), ()),
    ((7,), (-1,), -1, (), ()),
    # four dimensions
    ((2, 3, 4, 5), (0, 1, 2, 3), 1, (2, 4, 5), (0, 1, 2)),
    ((2, 3, 4, 5), (3, 1, 0, 2), 1, (2, 4, 5), (2, 0, 1)),
    ((2, 3, 4, 5), (3, 1, 0, 2), 3, (2, 3, 4), (2, 1, 0)),
    ((2, 3, 4, 5), (3, 1, 0, 2), 0, (3, 4, 5), (1, 0, 2)),
]


@pytest.mark.parametrize("s, axes, axis, exp_s, exp_axes", _CASES)
def test_remove_axis(s, axes, axis, exp_s, exp_axes):
    ss, aa = _remove_axis(s, axes, axis)
    assert tuple(ss) == exp_s
    assert tuple(aa) == exp_axes


@pytest.mark.parametrize("s, axes, axis, exp_s, exp_axes", _CASES)
def test_remove_axis_result_types(s, axes, axis, exp_s, exp_axes):
    ss, aa = _remove_axis(s, axes, axis)
    assert isinstance(ss, tuple)
    assert isinstance(aa, tuple)
    assert len(ss) == len(s) - 1
    assert len(aa) == len(axes) - 1


@pytest.mark.parametrize("s, axes, axis, exp_s, exp_axes", _CASES)
def test_remove_axis_inputs_unchanged(s, axes, axis, exp_s, exp_axes):
    s_copy, axes_copy = list(s), list(axes)
    _remove_axis(tuple(s_copy), tuple(axes_copy), axis)
    assert s_copy == list(s)
    assert axes_copy == list(axes)


def test_remove_axis_sequence_of_s():
    # a list for `s` is sliced, not converted, and gives a list back
    ss, aa = _remove_axis([4, 5, 6], (0, 1, 2), 1)
    assert ss == [4, 6]
    assert aa == (0, 1)
