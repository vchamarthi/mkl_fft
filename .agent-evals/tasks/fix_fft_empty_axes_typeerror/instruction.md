# `mkl_fft.fftn(x, axes=())` raises TypeError

Calling the N-D transforms of the top-level `mkl_fft` API with an empty `axes` tuple crashes for real-valued input instead of behaving like NumPy:

```python
import numpy as np
import mkl_fft

x = np.random.rand(3, 4)
mkl_fft.fftn(x, axes=())
# TypeError: copyto() argument 1 must be a numpy.ndarray, not numpy.complex128
```

`numpy.fft.fftn(x, axes=())` returns the data unchanged (an empty set of axes is the identity transform), with the input dtype preserved and no normalisation applied, whatever `norm` is.

Expected: `mkl_fft.fftn`, `ifftn`, `fft2` and `ifft2` called with `axes=()` return the same values and the same dtype as the corresponding `numpy.fft` function, for float32, float64, complex64 and complex128 input, 1-D to 3-D arrays, and every `norm` value (`None`, `"backward"`, `"forward"`, `"ortho"`).

Do not weaken or delete existing tests.
