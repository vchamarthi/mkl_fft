# Author notes: numeric_fftn_real_input_hermitian

Not shown to the agent under evaluation.

- base: 4e84e7e (upstream master after #389)
- `setup.patch` injects a one-line bug into the real-input N-D backend in `mkl_fft/src/mklfft.c.src`
  (`@inp_type_name@_@out_type_name@_mkl_@op_name@_out`, "copy conjugate even harmonics"): the source index of the
  Hermitian mirror is reflected only along the last axis (`src_ki = (i == last_idx) ? ni - dest_ki : dest_ki;`)
  instead of along every axis (`src_ki = (dest_ki) ? ni - dest_ki : dest_ki;`). The oracle is the reverse patch.
- The bug is invisible when every non-last transformed axis has length <= 2 and for 1-D input.
- The existing suite catches it (244 failures in test_fftnd.py / test_dispatch_equivalence.py), so the task
  measures locating and fixing a C-backend bug from its symptoms; the probe adds layouts, magnitudes, NaN, norms.
- probe.py: 106 cases; 80 fail with the bug, 0 fail on the correct code. Comparison is norm-wise
  (max |got - want| <= (rtol + atol) * max |want|) with rtol = 2**11 eps, atol = 2**9 eps of the result's real
  dtype, from mkl_fft/tests/test_fftnd.py. NaN propagation is compared per complex element because MKL and
  pocketfft legitimately produce NaN in different real/imaginary parts of the same element.
