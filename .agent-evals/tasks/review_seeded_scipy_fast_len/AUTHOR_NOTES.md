# Author notes: review_seeded_scipy_fast_len

Not shown to the agent under evaluation.

Synthetic change at 4e84e7e: adds `next_fast_len`/`prev_fast_len` (7-smooth lengths) to
`mkl_fft/interfaces/_scipy_fft.py`, exports `next_fast_len` from `scipy_fft.py`, documents both in the interfaces
README and adds tests to `test_interfaces.py`. All seeds were confirmed by running the patched tree:
`next_fast_len(8) == 9`, `next_fast_len(0) == 1` (scipy raises ValueError), `_is_fast_len(3**40) is False`,
`hasattr(scipy_fft, "prev_fast_len") is False`; the added tests pass despite S1.

Seeds: S1 off-by-one (start at target + 1), S2 accepts target 0, S3 float division in the factor loop, S4 debug
print, S5 prev_fast_len not exported from the public module, S6 weak test (`n >= target`, no prev_fast_len test),
S7 no CHANGELOG entry (CONTRIBUTING.md: user-visible changes need a `## [dev]` entry).

Decoys (acceptable):
- D1: the `real` argument is accepted and ignored, with a `# Note: ... not utilized` comment — the same idiom the
  interface uses for `overwrite_x` ("Note: overwrite_x is not utilized"). Fast lengths are backend-specific by
  definition, and OneMKL's fast radices are the same for real and complex transforms.
- D2: `prev_fast_len`'s `while not _is_fast_len(n): n -= 1` has no explicit lower bound but always terminates at 1
  (1 is a fast length) and `target >= 1` is checked.

Judgement calls: S2 relies on scipy's behaviour (`scipy.fft.next_fast_len(0)` raises "Target length must be
positive", checked with scipy 1.18). Decoy keywords are matched anywhere in the file by the grader (not only near
`lines`), so they are kept narrow.
