# Author notes: test_scipy_iface_shape_axes

Not shown to the agent under evaluation.

- base: 4e84e7e (upstream master). `author mutants` defaulted to HEAD (the fork's merge commit d020950, which adds
  `.github/workflows/repoevals.yml`); the base was changed to the upstream commit, where `_scipy_fft.py` is identical.
- 20 generated mutants of `_init_nd_shape_and_axes`, all killed by the reference tests (43 tests in
  `oracle_tests/mkl_fft/tests/test_scipy_shape_axes.py`). Two near-duplicate constant tweaks of the `invreal` line
  (`* 3`, `- 0`) were removed to reduce the weight of that one line: 18 mutants remain, 7 of them still on the
  `invreal` branch.
