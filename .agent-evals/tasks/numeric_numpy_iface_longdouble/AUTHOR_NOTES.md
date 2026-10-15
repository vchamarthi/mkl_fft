# Author notes: numeric_numpy_iface_longdouble

Not shown to the agent under evaluation.

- base: 4e84e7e (upstream master after #389)
- `setup.patch` changes `_downcast_float128_array` in `mkl_fft/interfaces/_float_utils.py` (ndarray branch) to
  convert `longdouble` to `float32` and `clongdouble` to `complex64` instead of `float64`/`complex128`, a
  copy-paste-style error modelled on the neighbouring `_upcast_float16_array` ("convert to single precision").
  The oracle is the reverse patch.
- No existing test covers long double input to the NumPy interface (`test_interfaces.py` passes with the bug), so
  the probe is the only detector. 153 cases: 129 fail with the bug, 0 on the correct code.
- x86-only: on platforms where `longdouble` is `float64` the helper is a no-op. `requires.cpu_flags = ["sse2"]`
  restricts the task to x86.
- Comparison: norm-wise, rtol = 2**11 eps, atol = 2**9 eps of the result's real dtype (mkl_fft/tests/test_fftnd.py).
