import numpy as np

import pytest

from numpy import random as rnd

from numpy.testing import TestCase, assert_allclose

import mkl_fft

from .helper import requires_numpy_2

reps_64 = (2**11) * np.finfo(np.float64).eps

reps_32 = (2**11) * np.finfo(np.float32).eps

atol_64 = (2**9) * np.finfo(np.float64).eps

atol_32 = (2**9) * np.finfo(np.float32).eps

def _get_rtol_atol(x):
    dt = x.dtype
    if dt == np.float64 or dt == np.complex128:
        return reps_64, atol_64
    elif dt == np.float32 or dt == np.complex64:
        return reps_32, atol_32
    else:
        assert (
            dt == np.float64
            or dt == np.complex128
            or dt == np.float32
            or dt == np.complex64
        ), "Unexpected dtype {}".format(dt)
        return reps_64, atol_64

@pytest.mark.parametrize(
    "dtype", [np.float32, np.float64, np.complex64, np.complex128]
)
@pytest.mark.parametrize("func", ["fftn", "ifftn", "fft2", "ifft2"])
def test_empty_axes_with_out(dtype, func):
    if np.issubdtype(dtype, np.complexfloating):
        x = rnd.random((3, 4)).astype(dtype) + 1j * rnd.random((3, 4)).astype(
            dtype
        )
    else:
        x = rnd.random((3, 4)).astype(dtype)

    # NumPy ignores out parameter when axes=() and returns input
    out = np.empty_like(x, dtype=dtype)
    result = getattr(mkl_fft, func)(x, axes=(), out=out)
    expected = getattr(np.fft, func)(x, axes=(), out=out)

    # Result should be the input array (out parameter ignored)
    assert result is x, f"{func} with axes=() should return input (ignore out)"
    assert expected is x, "NumPy should also return input"
    assert result is expected

@pytest.mark.parametrize(
    "dtype", [np.float32, np.float64, np.complex64, np.complex128]
)
@pytest.mark.parametrize("func", ["fftn", "ifftn", "fft2", "ifft2"])
def test_empty_axes_returns_same_object(dtype, func):
    if np.issubdtype(dtype, np.complexfloating):
        x = rnd.random((3, 4)).astype(dtype) + 1j * rnd.random((3, 4)).astype(
            dtype
        )
    else:
        x = rnd.random((3, 4)).astype(dtype)

    # Without out parameter, should return the same object
    result = getattr(mkl_fft, func)(x, axes=())

    # Verify it's the exact same object (identity check)
    assert (
        result is x
    ), f"{func} with axes=() should return the same object, not a copy"
