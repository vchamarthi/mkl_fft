import numpy as np

from numpy.testing import assert_allclose

import mkl_fft

reps_32 = (2**11) * np.finfo(np.float32).eps

atol_32 = (2**9) * np.finfo(np.float32).eps


def test_gh109():
    b_int = np.array([[5, 7, 6, 5], [4, 6, 4, 8], [9, 3, 7, 5]], dtype=np.int64)
    b = np.asarray(b_int, dtype=np.float32)

    r1 = mkl_fft.fftn(
        b, shape=None, axes=(0,), overwrite_x=False, forward_scale=1 / 3
    )
    r2 = mkl_fft.fftn(
        b_int, shape=None, axes=(0,), overwrite_x=False, forward_scale=1 / 3
    )

    assert_allclose(r1, r2, rtol=reps_32, atol=atol_32)
