# `fft`/`ifft` with `out=` ignore integer/bool/`float16` input and mis-handle padded strided input

Passing `out=` to `mkl_fft.fft`, `mkl_fft.ifft` or the `fftn`/`ifftn`/`fft2` family gives wrong results in two
situations where the same call without `out=` is correct.

1. **Input dtypes that must be converted.** For input that is not `float32`, `float64`, `complex64` or
   `complex128` (for example `bool`, `int8`, `uint8`, `int32`, `int64`, `float16`), `out` is returned with its
   previous contents; the transform is never written into it. For `longdouble`/`clongdouble` input the call
   without `out=` raises `ValueError` ("... single or double precision"), but with `out=` it silently returns.

   ```python
   import numpy as np
   import mkl_fft

   x = np.arange(1, 17)                    # int64
   out = np.full(16, -1 - 1j)
   r = mkl_fft.fft(x, out=out)
   print(r is out, np.allclose(out, np.fft.fft(x)))   # True False -- out still holds -1-1j
   print(np.allclose(mkl_fft.fft(x), np.fft.fft(x)))  # True

   mkl_fft.fft(np.ones(8, np.longdouble), out=np.empty(8, complex))   # no error
   ```

2. **Strided input and `out` with the same layout.** When `x` and `out` are views with the same non-contiguous
   layout and `x` is either zero-padded (`n` larger than its length along `axis`) or of a dtype listed above, the
   values in `out` are wrong.

   ```python
   shape = (20, 33, 54)
   base = np.full(shape, -1 - 1j)
   out = base[::2, ::3, ::4]                                   # shape (10, 11, 14)
   x = (np.random.default_rng(0).integers(-50, 50, size=shape) + 0j)[::2, ::3, ::4][:, :, :-3]
   mkl_fft.fft(x, n=14, axis=2, out=out)
   print(np.allclose(out, np.fft.fft(x, n=14, axis=2)))        # False
   ```

Expected: with `out=`, `fft`/`ifft` (any `n` and `axis`) and `fftn`/`ifftn` (any `axes`) return `out` filled with
the same values as `numpy.fft`, for every input dtype numpy.fft accepts (integer and `bool` input is computed as
`complex128`), for C-ordered, Fortran-ordered and strided `x`/`out`, and never write outside of `out`.
`longdouble`/`clongdouble` input must raise the same `ValueError` with and without `out=`.

Do not weaken or delete existing tests.
