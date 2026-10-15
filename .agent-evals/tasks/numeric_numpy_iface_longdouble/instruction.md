# `mkl_fft.interfaces.numpy_fft` loses precision and overflows for long double input

MKL has no long double FFT, so the NumPy interface (`mkl_fft.interfaces.numpy_fft`, also what
`mkl_fft.patch_numpy_fft()` installs into `numpy.fft`) is meant to compute `np.longdouble` / `np.clongdouble` input
in double precision. Instead, results for such input come back with single-precision dtypes and accuracy, and
values outside the `float32` range overflow or underflow:

```python
import numpy as np
import mkl_fft.interfaces.numpy_fft as mfft

x = np.random.default_rng(0).standard_normal(32).astype(np.longdouble)
print(mfft.fft(x).dtype)                     # complex64
print(mfft.irfft(x.astype(np.clongdouble)).dtype)   # float32

ref = np.fft.fft(x.astype(np.float64))
print(np.abs(mfft.fft(x) - ref).max())       # ~1e-6, far from double-precision rounding

big = x * np.longdouble(1e200)
print(np.isfinite(mfft.fft(big)).all())      # False (with an overflow RuntimeWarning)
```

Expected: for `longdouble` and `clongdouble` input, every function of `mkl_fft.interfaces.numpy_fft`
(`fft`, `ifft`, `rfft`, `irfft`, `hfft`, `ihfft`, `fft2`, `ifft2`, `fftn`, `ifftn`, `rfftn`, `irfftn`) returns the
same dtype and values (up to double-precision rounding) as `numpy.fft` applied to the input converted to
`float64`/`complex128` — for any `n`, `norm`, strides, very large or very small magnitudes and NaN values. Input of
other dtypes must behave as before.

Do not weaken or delete existing tests.
