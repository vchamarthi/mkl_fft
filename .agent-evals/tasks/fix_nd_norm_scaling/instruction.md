# N-D transforms in the top-level API return wrongly scaled results for `norm="forward"` / `"ortho"`

The N-D functions in the top-level `mkl_fft` namespace (`fftn`, `ifftn`, `rfftn`, `irfftn`, and `fft2`, `ifft2`, `rfft2`, `irfft2`) silently return mis-scaled results with `norm="forward"` or `norm="ortho"` when `s` is not given. `norm=None`/`"backward"` is fine.

Case 1: transforming only some axes. An `"ortho"` transform must be unitary, but:

```python
import numpy as np
import mkl_fft

x = np.random.randn(16, 18) + 1j * np.random.randn(16, 18)
x /= np.sqrt((abs(x) ** 2).sum())          # unit L2 norm

y = mkl_fft.fftn(x, axes=(0,), norm="ortho")
print((abs(y) ** 2).sum())                 # expected 1.0, got something much smaller
print(np.allclose(y, np.fft.fftn(x, axes=(0,), norm="ortho")))   # expected True, got False
```

The same happens for `fft2` on a 3-D array (it transforms two of three axes), e.g. `mkl_fft.fft2(np.random.randn(8, 7, 13), norm="forward")` differs from `np.fft.fft2(..., norm="forward")`, and for `rfftn` with a subset of axes.

Case 2: inverse real transforms. `mkl_fft.irfftn(c, norm="forward")` and `norm="ortho"` (with `axes` all or a subset) do not agree with `numpy.fft.irfftn`, even when every axis is transformed.

Expected: for every `norm` in `{None, "backward", "forward", "ortho"}` and any `axes` (subset, reversed, negative, or `None`), the results of these functions equal those of `numpy.fft` (values, shape and dtype) for float64 and complex128 input. Results with an explicit `s` and 1-D transforms are already right and must stay so.

Do not weaken or delete existing tests.
