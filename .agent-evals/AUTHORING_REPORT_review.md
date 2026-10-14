
## Follow-up from `repoevals check` (CI)

- `test_remove_axis`: mutants m10 and m14 (`<` → `<=` on the pivot) survive the reference tests; they are equivalent for valid input (`pivot` equals another axis only when axes are duplicated, which N-D transforms reject). Moved to `mutants_rejected/`.
- Several task bases predate mkl_fft's move from setuptools to meson-python (mid-2026): the environment needs `setuptools>=77` as well.
