import mkl

import numpy as np

import pytest

from numpy.testing import assert_allclose

import mkl_fft.interfaces.scipy_fft as fft

@pytest.fixture(scope="module")
def x():
    return np.random.randn(512, 128)  # Must be large enough to qualify for mt

def test_invalid_workers(x):
    # cpus = os.cpu_count()
    threads = mkl.get_max_threads()  # pylint: disable=no-member
    # cpus and threads are usually the same but in CI, cpus = 4 and threads = 2
    # SciPy uses `os.cpu_count()` to get the number of workers, while
    # `mkl_fft.interfaces.scipy_fft` uses `mkl.get_max_threads()`

    fft.ifft([1], workers=-threads)

    with pytest.raises(ValueError, match="workers must not be zero"):
        fft.fft(x, workers=0)

    with pytest.raises(ValueError, match="workers value out of range"):
        fft.ifft(x, workers=-threads - 1)

def test_set_get_workers():
    # cpus = os.cpu_count()
    threads = mkl.get_max_threads()  # pylint: disable=no-member

    # default value is max number of threads unlike stock SciPy
    assert fft.get_workers() == threads
    with fft.set_workers(4):
        assert fft.get_workers() == 4

        with fft.set_workers(-1):
            assert fft.get_workers() == threads

        assert fft.get_workers() == 4

    # default value is max number of threads unlike stock SciPy
    assert fft.get_workers() == threads

    with fft.set_workers(-threads):
        assert fft.get_workers() == 1

def test_set_workers_invalid():

    with pytest.raises(ValueError, match="workers must not be zero"):
        with fft.set_workers(0):
            pass

    with pytest.raises(ValueError, match="workers value out of range"):
        # pylint: disable=no-member
        with fft.set_workers(-mkl.get_max_threads() - 1):
            pass
