# `fftn`/`fft2` of real input disagree with NumPy for multi-dimensional arrays

For **real** (`float32`/`float64`) input with two or more dimensions, `mkl_fft.fftn`, `mkl_fft.ifftn`,
`mkl_fft.fft2` and `mkl_fft.ifft2` return results that differ from `numpy.fft` — not by rounding, but in whole
blocks of output elements. One-dimensional transforms and complex input are correct, and a few shapes (for
example `(2, n)` or `(1, n)`) happen to give the right answer.

```python
import numpy as np
import mkl_fft

x = np.random.default_rng(0).standard_normal((4, 6))
print(np.allclose(mkl_fft.fftn(x), np.fft.fftn(x)))                 # False
print(np.allclose(mkl_fft.fftn(x + 0j), np.fft.fftn(x + 0j)))       # True
print(np.allclose(mkl_fft.fftn(x[:2]), np.fft.fftn(x[:2])))         # True

y = np.random.default_rng(1).standard_normal((5, 6, 7)).astype(np.float32)
print(np.allclose(mkl_fft.ifftn(y, axes=(1, 2)), np.fft.ifftn(y, axes=(1, 2)), atol=1e-5))   # False
```

Expected: for real input of any shape and memory layout (C, Fortran, strided, negative strides), any `axes` and
every `norm`, these functions agree with `numpy.fft` to within floating-point rounding for the input precision
(complex64 results for `float32`, complex128 for `float64`), including very large and very small magnitudes and
inputs containing NaN. Complex-input and 1-D results must not change.

Do not weaken or delete existing tests.
