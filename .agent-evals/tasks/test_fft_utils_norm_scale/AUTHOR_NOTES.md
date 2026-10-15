# Author notes: test_fft_utils_norm_scale

Not shown to the agent under evaluation.

- base: 4e84e7e (upstream master).
- 12 mutants of `_compute_fwd_scale` + 12 of `_cook_nd_args` (two `author mutants` runs; file names restart at
  m01 for the second function: the `L7x-L8x` ones are `_compute_fwd_scale`, `L92-L111` are `_cook_nd_args`).
- All 24 are killed by the 45 reference tests in `oracle_tests/mkl_fft/tests/test_fft_utils_helpers.py`. Mutants
  that look equivalent are not: `nn != 1` divides by zero for zero lengths; negating the `isinstance` checks
  sends lists into `1 / list`.
