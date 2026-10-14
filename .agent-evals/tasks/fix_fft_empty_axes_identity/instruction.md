# `fft2`/`fftn` with `axes=()` and `out=` do not match NumPy semantics

With an empty `axes` tuple the N-D transforms are the identity. NumPy returns the very same input array in that case and ignores the `out` argument. `mkl_fft` copies the data into `out` and returns `out` instead:

```python
import numpy as np
import mkl_fft

a = np.ones((2, 3, 4))
out = np.empty_like(a)

b_np = np.fft.fft2(a, axes=(), out=out)
b_mkl = mkl_fft.fft2(a, axes=(), out=out)

print(b_np is a, b_np is out)     # True False
print(b_mkl is a, b_mkl is out)   # False True   <- should match NumPy

print(mkl_fft.fftn(a, axes=()) is a)   # expected True, got False (a copy is returned)
```

Expected: for `fftn`, `ifftn`, `fft2` and `ifft2` (float32/float64/complex64/complex128 input) called with `axes=()`, `mkl_fft` returns the input array object itself, with or without `out`, exactly as `numpy.fft` does.

Note: the repository currently contains a test that asserts the old behaviour for `out` with `axes=()` (the result being `out`); that expectation should be updated to NumPy's behaviour. Apart from that, do not weaken or delete existing tests.
