# Author notes: review_replay_370

PR: https://github.com/IntelPython/mkl_fft/pull/370 — fix: norm scaling
Reviewed revision: db030bac11cccb669d63498d34a3f3275a88b399
Base: f83b9d41f4e823880242519773d487d2091bf6d6

Edit gold.json: keep threads that ask for a change; remove praise, questions answered by the author, and
pure nits. Each remaining thread is a finding a good reviewer should make.

- `mkl_fft/tests/test_dispatch_equivalence.py:52` (vlad-perevezentsev): 'It looks like `numpy.fft` may be patched to `mkl_fft` when NumPy is installed from Intel channels (software.repos.intel.com/python/conda or gold)\n ```\n$ python '
- `mkl_fft/_fft_utils.py:81` (vlad-perevezentsev): 'This function almost exactly replicates the logic in `_cook_nd_args`\nIt looks like we can reuse it\nSomething like this\n```\ndef _nd_fwd_scale(x, s, axes, norm, i'
- `CHANGELOG.md:18` (vlad-perevezentsev): 'The changelog does not mention gh-336 which this PR also fixes'
- `mkl_fft/tests/test_dispatch_equivalence.py:258` (vlad-perevezentsev): 'It overlaps `test_empty_axes` and `test_empty_axes_returns_same_object` in `test_fftnd.py` almost entirely \nCould be removed '
- `mkl_fft/tests/test_dispatch_equivalence.py:131` (vlad-perevezentsev): 'You can parameterize it here and below to avoid skipping lines in the test log\n```\n_R2C_CASES = [("rfftn", dt) for dt in _REAL_DTYPES] + [\n    ("irfftn", dt) fo'
- `mkl_fft/tests/test_dispatch_equivalence.py:76` (vlad-perevezentsev): 'Could we add negative axes to `_AXES_3D`?'
- `mkl_fft/tests/test_dispatch_equivalence.py:412` (vlad-perevezentsev): 'A few combinations on the new code path are not covered yet : negative axes with norm . irfftn with subset axes, s, and norm , out= with s= and norm and fft2/rf'
