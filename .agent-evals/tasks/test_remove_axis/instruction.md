`_remove_axis(s, axes, axis_to_remove)` in `mkl_fft/_fft_utils.py` is a helper used when N-dimensional transforms are
reduced by one axis. Given a shape `s` and the transform axes `axes`, it drops the entry at position `axis_to_remove`
from both and returns `(new_shape, new_axes)`, renumbering the remaining axes so that they still refer to the same
dimensions of the array after the removed dimension is gone. Negative values for the axes and for `axis_to_remove` are
supported.

The function has no direct tests. Add tests that check its results are correct, including negative axes, axes in
different orders, removing the first, last and a middle entry, and the smallest inputs the function accepts. Put the
tests in `mkl_fft/tests/` as a new file that `python -m pytest` runs without extra options. Do not modify library
code: add test files only. Make sure the tests pass.

When you are done, end your answer with a fenced ```json block of the form `{"targets": ["mkl_fft/tests/<file>.py"]}`
listing the test files you added.
