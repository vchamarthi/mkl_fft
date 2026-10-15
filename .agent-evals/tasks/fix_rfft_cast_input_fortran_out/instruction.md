# `rfft`/`rfftn` with a Fortran-ordered `out` return wrong values for integer or `float16` input

`mkl_fft.rfft` and `mkl_fft.rfftn`/`rfft2` accept input of any real dtype; inputs that are not `float32` or
`float64` (integers, `float16`, `longdouble`) are computed in double precision. When such an input is
Fortran-ordered and a Fortran-ordered `out=` array is passed, the values written to `out` are wrong. The same call
without `out=`, or with a `float64` input, is correct.

```python
import numpy as np
import mkl_fft

x = np.asfortranarray(np.arange(6 * 7 * 8).reshape(6, 7, 8) % 13)   # int64, Fortran order

out = np.empty((4, 7, 8), dtype=complex, order="F")
mkl_fft.rfft(x, axis=0, out=out)
print(np.allclose(out, np.fft.rfft(x, axis=0)))        # False
print(np.allclose(mkl_fft.rfft(x, axis=0),
                  np.fft.rfft(x, axis=0)))             # True without out=

out2 = np.empty((6, 7, 5), dtype=complex, order="F")
mkl_fft.rfftn(x, out=out2)
print(np.allclose(out2, np.fft.rfftn(x)))              # False
```

Expected: `rfft` (every `axis`) and `rfftn`/`rfft2` return `out` itself, filled with the same values as
`numpy.fft` applied to the input converted to `float64`, for integer, `float16`, `float64` and `longdouble` input,
whatever the memory order of the input and of `out`. Results for `float32`/`float64` input must not change.

Do not weaken or delete existing tests.
