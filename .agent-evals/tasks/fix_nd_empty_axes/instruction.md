# `fftn`/`ifftn`/`fft2`/`ifft2` fail with `axes=()`

Calling the N-D complex transforms with an empty tuple of axes raises an exception, while `numpy.fft` treats it as
an identity operation:

```python
import numpy as np
import mkl_fft

x = np.random.random((3, 4))

np.fft.fftn(x, axes=()) is x        # True: numpy returns the input itself
mkl_fft.fftn(x, axes=())            # raises TypeError
mkl_fft.ifft2(x + 0j, axes=(), norm="ortho")   # raises as well
```

Expected: `mkl_fft.fftn`, `ifftn`, `fft2` and `ifft2` with `axes=()` behave exactly as in NumPy 2.x — for
`float32`, `float64`, `complex64` and `complex128` input of any shape and for every `norm`, they return the input
array object itself (no copy, no dtype change, no scaling), and an `out=` argument is ignored in that case, as
NumPy does. Behaviour for non-empty `axes` must not change.

Do not weaken or delete existing tests.
