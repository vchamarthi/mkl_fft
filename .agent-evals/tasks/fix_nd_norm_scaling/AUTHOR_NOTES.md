# Author notes: fix_nd_norm_scaling

Not shown to the agent under evaluation.

- source: https://github.com/IntelPython/mkl_fft/pull/370
- commit: f9f45234b63fde855ad500a28e546a19ef5e567a
- base: f83b9d41f4e823880242519773d487d2091bf6d6 (the fix's parent)
- subject: fix: norm scaling

## Files changed by the fix

- `.pre-commit-config.yaml` (M)
- `CHANGELOG.md` (M)
- `mkl_fft/_fft_utils.py` (M)
- `mkl_fft/_mkl_fft.py` (M)
- `pyproject.toml` (M)

## Hidden tests (from the fix commit)

- `mkl_fft/tests/test_repoevals_fix_nd_norm_scaling_dispatch_equivalence.py`: test_fftn_axes_subset, test_rfftn_axes_subset, test_fft_axis_3d, test_fft_axis_4d, test_rfft_axis_3d, test_ortho_preserves_norm, test_ortho_roundtrip_is_identity, test_fftn_axes_subset_norm, test_rfftn_axes_subset_norm, test_empty_axes_r2c_raises_like_numpy, test_fft2_on_3d_norm, test_fft_axis_norm, test_fftn_axes_subset_out, test_c2c_out_with_norm, test_rfftn_out_with_norm, test_irfftn_out_with_norm, test_c2c_shape_arg_with_norm, test_irfftn_shape_arg_with_norm, test_rfftn_shape_arg_with_norm, test_r2c_axes_subset_s_and_norm, test_out_with_s_and_norm, test_fft2_family_with_s_and_norm
