# Author notes: feature_patch_restore_unbalanced_warning

Not shown to the agent under evaluation.

- source: https://github.com/IntelPython/mkl_fft/pull/295
- commit: 5ae4bf4912daa7acc946ca0ac93fd35d6d29c51e
- base: 27583c9155356b4126385085b6dd28df95b73b44 (the fix's parent)
- subject: Use `RuntimeWarning` when unpatching more than patching

## Files changed by the fix

- `CHANGELOG.md` (M)
- `mkl_fft/_patch_numpy.py` (M)

## Hidden tests (from the fix commit)

- `mkl_fft/tests/test_patch.py`

## Authoring decisions

- Labelled `feature`: the change replaces a verbose-only stdout message by a `RuntimeWarning`, so the instruction
  has to name the warning category and message prefix the hidden test checks (`pytest.warns(RuntimeWarning,
  match="restore_numpy_fft*")`). That is an API requirement a user would state, not a hint at the code.
