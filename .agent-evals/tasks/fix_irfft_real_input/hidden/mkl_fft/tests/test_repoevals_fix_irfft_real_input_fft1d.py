import numpy as np

import pytest

from numpy import random as rnd

from numpy.testing import TestCase, assert_, assert_allclose

import mkl_fft

from .helper import requires_numpy_2

def naive_fft1d(vec):
    L = len(vec)
    phase = -2j * np.pi * (np.arange(L) / float(L))
    phase = np.arange(L).reshape(-1, 1) * phase
    return np.sum(vec * np.exp(phase), axis=1)

def _datacopied(arr, original):
    """
    Strict check for `arr` not sharing any data with `original`,
    under the assumption that arr = asarray(original)
    """
    if arr is original:
        return False
    if not isinstance(original, np.ndarray) and hasattr(original, "__array__"):
        return False
    return arr.base is None

class DuckArray(np.ndarray):
    pass

@requires_numpy_2
@pytest.mark.parametrize("dt", ["i4", "f4", "f8", "c8", "c16"])
def test_irfft_dtype(dt):
    x = np.array(rnd.random((20, 20)), dtype=dt)
    result = mkl_fft.irfft(x)
    expected = np.fft.irfft(x)
    assert_allclose(result, expected, rtol=1e-7, atol=1e-7, strict=True)
