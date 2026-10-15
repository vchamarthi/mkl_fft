# `norm="ortho"` / `norm="forward"` give the wrong scale in some N-D transforms

With `norm="ortho"` or `norm="forward"`, several N-D transforms of `mkl_fft` return results that differ from
`numpy.fft` by a constant factor:

- `fftn`, `ifftn`, `rfftn`, `irfftn` and the `fft2` family when they are applied to only some of the axes of an
  array (for example `axes=(1, 2)` of a 3-D array, or `fft2` of a 3-D array);
- `irfftn` and `irfft2` when `s` is not given, even over all axes.

`norm="ortho"` then no longer preserves the L2 norm.

```python
import numpy as np
import mkl_fft

x = np.random.default_rng(0).standard_normal((4, 6, 8))

a = mkl_fft.fftn(x, axes=(1, 2), norm="ortho")
b = np.fft.fftn(x, axes=(1, 2), norm="ortho")
print(np.allclose(a, b))                                   # False; |a| is half of |b|

print(np.allclose(mkl_fft.fft2(x, norm="forward"),
                  np.fft.fft2(x, norm="forward")))         # False

y = np.fft.rfftn(x)
print(np.allclose(mkl_fft.irfftn(y, norm="forward"),
                  np.fft.irfftn(y, norm="forward")))       # False
print(np.allclose(mkl_fft.irfftn(y, s=(4, 6, 8), axes=(0, 1, 2), norm="forward"),
                  np.fft.irfftn(y, s=(4, 6, 8), axes=(0, 1, 2), norm="forward")))  # True
```

Expected: for every `norm`, every N-D function (`fftn`, `ifftn`, `rfftn`, `irfftn`, `fft2`, `ifft2`, `rfft2`,
`irfft2`), any `axes`, with and without `s` and with and without `out=`, the result matches `numpy.fft`.
The default `norm="backward"` already behaves correctly and must not change.

Do not weaken or delete existing tests.
