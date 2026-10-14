import numpy as np

import pytest

from numpy import random as rnd

from numpy.testing import TestCase, assert_allclose

import mkl_fft

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
@pytest.mark.parametrize("shape", [(3, 4), (5,), (2, 3, 4), (10, 20)])
@pytest.mark.parametrize("norm", [None, "ortho", "forward", "backward"])
@pytest.mark.parametrize("func", ["fftn", "ifftn", "fft2", "ifft2"])
def test_empty_axes(dtype, shape, norm, func):
    if np.issubdtype(dtype, np.complexfloating):
        x = rnd.random(shape).astype(dtype) + 1j * rnd.random(shape).astype(
            dtype
        )
    else:
        x = rnd.random(shape).astype(dtype)

    # Test fftn with axes=()
    result = getattr(mkl_fft, func)(x, axes=(), norm=norm)
    expected = getattr(np.fft, func)(x, axes=(), norm=norm)

    rtol, atol = _get_rtol_atol(result)
    assert_allclose(result, expected, rtol=rtol, atol=atol, strict=True)
