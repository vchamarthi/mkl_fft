# `fftn` with `forward_scale` gives different results for integer and float32 input

When I call `mkl_fft.fftn` on a 2-D array with `axes=(0,)` and a custom `forward_scale`, the result depends on the input dtype in a way it should not. The same numbers passed as `float32` and as `int64` give results that differ by a constant factor.

```python
import numpy as np
import mkl_fft

b_int = np.array([[5, 7, 6, 5], [4, 6, 4, 8], [9, 3, 7, 5]], dtype=np.int64)
b = b_int.astype(np.float32)

r1 = mkl_fft.fftn(b, shape=None, axes=(0,), overwrite_x=False, forward_scale=1/3)
r2 = mkl_fft.fftn(b_int, shape=None, axes=(0,), overwrite_x=False, forward_scale=1/3)

print(np.allclose(r1, r2, rtol=1e-3))   # expected True, got False
print(r1[0], r2[0])                     # r2 is scaled by a different factor than r1
```

Expected: both calls return the same values (up to float32 rounding); `forward_scale` is the total factor applied to the whole transform, independent of the input dtype or of how many axes are transformed. `forward_scale=1.0` behaviour must not change.

Do not weaken or delete existing tests.
