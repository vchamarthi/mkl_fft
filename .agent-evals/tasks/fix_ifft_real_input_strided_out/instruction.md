# `ifft`/`ifftn` of real input with a non-contiguous `out` give wrong results and write outside `out`

When the input of `mkl_fft.ifft` (or `ifftn`/`ifft2`) is **real** and an `out=` array is passed that is not
contiguous (a strided slice, a negative-step view, or a view into a larger array), the result written to `out` is
wrong and memory of the underlying array *outside* the `out` view is modified. The forward `fft` with the same
arguments is correct, as is `ifft` of complex input.

```python
import numpy as np
import mkl_fft

x = np.random.default_rng(0).random(48)[::2]          # real input
base = np.full(48, -1 - 1j)
out = base[::2]                                        # non-contiguous out

mkl_fft.ifft(x, out=out)
print(np.allclose(out, np.fft.ifft(x)))                # False
print(np.count_nonzero(base[1::2] != -1 - 1j))         # 12: elements that are not part of out were changed

x3 = np.random.default_rng(0).random((20, 30, 40))[::2, ::3, ::4]
b3 = np.full((20, 30, 40), -1 - 1j)
o3 = b3[::2, ::3, ::4]
mkl_fft.ifftn(x3, out=o3)
print(np.allclose(o3, np.fft.ifftn(x3)))               # False
```

Larger inputs or negative strides can also crash the interpreter.

Expected: for real `float32`/`float64` input, `ifft` (any `axis`) and `ifftn`/`ifft2` (any `axes`) fill any
writable `out` of the right shape and dtype — positive or negative strides, C or Fortran order, or a view into a
larger array — with the same values as `numpy.fft`, return `out` itself, and never write outside of it.

Do not weaken or delete existing tests.
