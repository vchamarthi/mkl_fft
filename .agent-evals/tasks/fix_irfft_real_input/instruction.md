# `mkl_fft.irfft` returns the wrong dtype for single-precision real input

With NumPy 2, `numpy.fft.irfft` keeps single precision for float32 input. `mkl_fft.irfft` upcasts and returns double precision:

```python
import numpy as np
import mkl_fft

x = np.random.rand(20, 20).astype(np.float32)   # real input
print(np.fft.irfft(x).dtype)    # float32
print(mkl_fft.irfft(x).dtype)   # float64  <- expected float32
```

Expected: for inputs of dtype int32, float32, float64, complex64 and complex128, `mkl_fft.irfft(x)` returns the same dtype and the same values (to about 1e-7) as `numpy.fft.irfft(x)`; in particular single-precision input, real or complex, gives single-precision output.

Do not weaken or delete existing tests.
