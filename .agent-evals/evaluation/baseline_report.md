# repoevals report

## Configurations

| configuration | tasks | runs | pass rate | 95% CI | median agent time (s) | cost $ | tokens | status |
|---|---|---|---|---|---|---|---|---|
| `claude-code|us.anthropic.claude-sonnet-5|guidance:none` | 12 | 36 | 0.9722 | 0.8889-1.0 | 225.0 | 32.46 | 678548 | {'pass': 35, 'fail': 1} |
| `claude-code|us.anthropic.claude-sonnet-5|guidance:raw` | 12 | 36 | 0.9722 | 0.8889-1.0 | 239.4 | 37.47 | 815377 | {'pass': 35, 'fail': 1} |

## By family

| configuration | family | tasks | pass rate | 95% CI |
|---|---|---|---|---|
| `claude-code|us.anthropic.claude-sonnet-5|guidance:none` | feature | 1 | 1.0 | 1.0-1.0 |
| `claude-code|us.anthropic.claude-sonnet-5|guidance:none` | fix | 5 | 1.0 | 1.0-1.0 |
| `claude-code|us.anthropic.claude-sonnet-5|guidance:none` | numeric | 2 | 1.0 | 1.0-1.0 |
| `claude-code|us.anthropic.claude-sonnet-5|guidance:none` | review | 2 | 0.8333 | 0.3333-1.0 |
| `claude-code|us.anthropic.claude-sonnet-5|guidance:none` | test | 2 | 1.0 | 1.0-1.0 |
| `claude-code|us.anthropic.claude-sonnet-5|guidance:raw` | feature | 1 | 1.0 | 1.0-1.0 |
| `claude-code|us.anthropic.claude-sonnet-5|guidance:raw` | fix | 5 | 1.0 | 1.0-1.0 |
| `claude-code|us.anthropic.claude-sonnet-5|guidance:raw` | numeric | 2 | 1.0 | 1.0-1.0 |
| `claude-code|us.anthropic.claude-sonnet-5|guidance:raw` | review | 2 | 0.8333 | 0.3333-1.0 |
| `claude-code|us.anthropic.claude-sonnet-5|guidance:raw` | test | 2 | 1.0 | 1.0-1.0 |

## Paired comparisons (b - a, same tasks)

| a | b | tasks | Δ pass rate | 95% CI | p (sign-flip) | better / worse |
|---|---|---|---|---|---|---|
| `claude-code|us.anthropic.claude-sonnet-5|guidance:none` | `claude-code|us.anthropic.claude-sonnet-5|guidance:raw` | 12 | +0.0 | 0.0-0.0 | 1.0 | 0 / 0 |

## Tasks  -  `claude-code|us.anthropic.claude-sonnet-5|guidance:none`

| task | runs | passed | pass@1 | pass@3 | pass^3 |
|---|---|---|---|---|---|
| feature_patch_restore_unbalanced_warning | 3 | 3 | 1.0 | 1.0 | 1.0 |
| fix_c2c_out_cast_or_padded_input | 3 | 3 | 1.0 | 1.0 | 1.0 |
| fix_ifft_real_input_strided_out | 3 | 3 | 1.0 | 1.0 | 1.0 |
| fix_nd_empty_axes | 3 | 3 | 1.0 | 1.0 | 1.0 |
| fix_nd_norm_subset_axes | 3 | 3 | 1.0 | 1.0 | 1.0 |
| fix_rfft_cast_input_fortran_out | 3 | 3 | 1.0 | 1.0 | 1.0 |
| numeric_fftn_real_input_hermitian | 3 | 3 | 1.0 | 1.0 | 1.0 |
| numeric_numpy_iface_longdouble | 3 | 3 | 1.0 | 1.0 | 1.0 |
| review_clean_norm_scale_docs | 3 | 3 | 1.0 | 1.0 | 1.0 |
| review_seeded_scipy_fast_len | 3 | 2 | 0.667 | 1.0 | 0.0 |
| test_fft_utils_norm_scale | 3 | 3 | 1.0 | 1.0 | 1.0 |
| test_scipy_iface_shape_axes | 3 | 3 | 1.0 | 1.0 | 1.0 |

## Tasks  -  `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`

| task | runs | passed | pass@1 | pass@3 | pass^3 |
|---|---|---|---|---|---|
| feature_patch_restore_unbalanced_warning | 3 | 3 | 1.0 | 1.0 | 1.0 |
| fix_c2c_out_cast_or_padded_input | 3 | 3 | 1.0 | 1.0 | 1.0 |
| fix_ifft_real_input_strided_out | 3 | 3 | 1.0 | 1.0 | 1.0 |
| fix_nd_empty_axes | 3 | 3 | 1.0 | 1.0 | 1.0 |
| fix_nd_norm_subset_axes | 3 | 3 | 1.0 | 1.0 | 1.0 |
| fix_rfft_cast_input_fortran_out | 3 | 3 | 1.0 | 1.0 | 1.0 |
| numeric_fftn_real_input_hermitian | 3 | 3 | 1.0 | 1.0 | 1.0 |
| numeric_numpy_iface_longdouble | 3 | 3 | 1.0 | 1.0 | 1.0 |
| review_clean_norm_scale_docs | 3 | 3 | 1.0 | 1.0 | 1.0 |
| review_seeded_scipy_fast_len | 3 | 2 | 0.667 | 1.0 | 0.0 |
| test_fft_utils_norm_scale | 3 | 3 | 1.0 | 1.0 | 1.0 |
| test_scipy_iface_shape_axes | 3 | 3 | 1.0 | 1.0 | 1.0 |

## Scores  -  `claude-code|us.anthropic.claude-sonnet-5|guidance:none`

| task:metric | mean |
|---|---|
| numeric_fftn_real_input_hermitian:case_pass_rate | 1.0 |
| numeric_numpy_iface_longdouble:case_pass_rate | 1.0 |
| review_clean_norm_scale_docs:precision | 0.3333 |
| review_seeded_scipy_fast_len:f1 | 0.7903 |
| review_seeded_scipy_fast_len:precision | 0.7737 |
| review_seeded_scipy_fast_len:recall | 0.8093 |
| test_fft_utils_norm_scale:kill_rate | 0.972 |
| test_scipy_iface_shape_axes:kill_rate | 1.0 |

## Scores  -  `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`

| task:metric | mean |
|---|---|
| numeric_fftn_real_input_hermitian:case_pass_rate | 1.0 |
| numeric_numpy_iface_longdouble:case_pass_rate | 1.0 |
| review_clean_norm_scale_docs:precision | 0.3333 |
| review_seeded_scipy_fast_len:f1 | 0.7167 |
| review_seeded_scipy_fast_len:precision | 0.724 |
| review_seeded_scipy_fast_len:recall | 0.714 |
| test_fft_utils_norm_scale:kill_rate | 1.0 |
| test_scipy_iface_shape_axes:kill_rate | 1.0 |

## Task health

- `feature_patch_restore_unbalanced_warning`: passes in every configuration
- `fix_c2c_out_cast_or_padded_input`: passes in every configuration
- `fix_ifft_real_input_strided_out`: passes in every configuration
- `fix_nd_empty_axes`: passes in every configuration
- `fix_nd_norm_subset_axes`: passes in every configuration
- `fix_rfft_cast_input_fortran_out`: passes in every configuration
- `numeric_fftn_real_input_hermitian`: passes in every configuration
- `numeric_numpy_iface_longdouble`: passes in every configuration
- `review_clean_norm_scale_docs`: passes in every configuration
- `test_fft_utils_norm_scale`: passes in every configuration
- `test_scipy_iface_shape_axes`: passes in every configuration

## Integrity flags (read these transcripts)

- `feature_patch_restore_unbalanced_warning` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/feature_patch_restore_unbalanced_warning/guidance_none/r0
- `feature_patch_restore_unbalanced_warning` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/feature_patch_restore_unbalanced_warning/guidance_raw/r0
- `feature_patch_restore_unbalanced_warning` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/feature_patch_restore_unbalanced_warning/guidance_raw/r1
- `feature_patch_restore_unbalanced_warning` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/feature_patch_restore_unbalanced_warning/guidance_raw/r2
- `fix_c2c_out_cast_or_padded_input` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/fix_c2c_out_cast_or_padded_input/guidance_none/r0
- `fix_c2c_out_cast_or_padded_input` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: history_mining, protected_modified  -  <runs>/fix_c2c_out_cast_or_padded_input/guidance_none/r1
- `fix_c2c_out_cast_or_padded_input` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/fix_c2c_out_cast_or_padded_input/guidance_none/r2
- `fix_c2c_out_cast_or_padded_input` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/fix_c2c_out_cast_or_padded_input/guidance_raw/r0
- `fix_c2c_out_cast_or_padded_input` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/fix_c2c_out_cast_or_padded_input/guidance_raw/r1
- `fix_c2c_out_cast_or_padded_input` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/fix_c2c_out_cast_or_padded_input/guidance_raw/r2
- `fix_ifft_real_input_strided_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: history_mining, protected_modified  -  <runs>/fix_ifft_real_input_strided_out/guidance_none/r0
- `fix_ifft_real_input_strided_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: history_mining, protected_modified  -  <runs>/fix_ifft_real_input_strided_out/guidance_none/r1
- `fix_ifft_real_input_strided_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/fix_ifft_real_input_strided_out/guidance_none/r2
- `fix_ifft_real_input_strided_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/fix_ifft_real_input_strided_out/guidance_raw/r0
- `fix_ifft_real_input_strided_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/fix_ifft_real_input_strided_out/guidance_raw/r1
- `fix_ifft_real_input_strided_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: history_mining, protected_modified  -  <runs>/fix_ifft_real_input_strided_out/guidance_raw/r2
- `fix_nd_empty_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/fix_nd_empty_axes/guidance_none/r0
- `fix_nd_empty_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/fix_nd_empty_axes/guidance_none/r1
- `fix_nd_empty_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/fix_nd_empty_axes/guidance_none/r2
- `fix_nd_empty_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/fix_nd_empty_axes/guidance_raw/r0
- `fix_nd_empty_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified, test_tampering  -  <runs>/fix_nd_empty_axes/guidance_raw/r1
- `fix_nd_empty_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/fix_nd_empty_axes/guidance_raw/r2
- `fix_nd_norm_subset_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified, test_tampering  -  <runs>/fix_nd_norm_subset_axes/guidance_none/r0
- `fix_nd_norm_subset_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/fix_nd_norm_subset_axes/guidance_none/r1
- `fix_nd_norm_subset_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/fix_nd_norm_subset_axes/guidance_none/r2
- `fix_nd_norm_subset_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/fix_nd_norm_subset_axes/guidance_raw/r0
- `fix_nd_norm_subset_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified, test_tampering  -  <runs>/fix_nd_norm_subset_axes/guidance_raw/r1
- `fix_nd_norm_subset_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/fix_nd_norm_subset_axes/guidance_raw/r2
- `fix_rfft_cast_input_fortran_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/fix_rfft_cast_input_fortran_out/guidance_none/r0
- `fix_rfft_cast_input_fortran_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/fix_rfft_cast_input_fortran_out/guidance_none/r1
- `fix_rfft_cast_input_fortran_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/fix_rfft_cast_input_fortran_out/guidance_none/r2
- `fix_rfft_cast_input_fortran_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/fix_rfft_cast_input_fortran_out/guidance_raw/r0
- `fix_rfft_cast_input_fortran_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: history_mining, protected_modified  -  <runs>/fix_rfft_cast_input_fortran_out/guidance_raw/r1
- `fix_rfft_cast_input_fortran_out` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/fix_rfft_cast_input_fortran_out/guidance_raw/r2
- `numeric_fftn_real_input_hermitian` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/numeric_fftn_real_input_hermitian/guidance_none/r0
- `numeric_fftn_real_input_hermitian` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/numeric_fftn_real_input_hermitian/guidance_none/r1
- `numeric_fftn_real_input_hermitian` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: history_mining, protected_modified, test_tampering  -  <runs>/numeric_fftn_real_input_hermitian/guidance_none/r2
- `numeric_fftn_real_input_hermitian` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: history_mining, protected_modified, source_access, test_tampering  -  <runs>/numeric_fftn_real_input_hermitian/guidance_raw/r0
- `numeric_fftn_real_input_hermitian` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified, test_tampering  -  <runs>/numeric_fftn_real_input_hermitian/guidance_raw/r1
- `numeric_fftn_real_input_hermitian` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: history_mining, protected_modified, test_tampering  -  <runs>/numeric_fftn_real_input_hermitian/guidance_raw/r2
- `numeric_numpy_iface_longdouble` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/numeric_numpy_iface_longdouble/guidance_none/r0
- `numeric_numpy_iface_longdouble` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/numeric_numpy_iface_longdouble/guidance_none/r1
- `numeric_numpy_iface_longdouble` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: protected_modified  -  <runs>/numeric_numpy_iface_longdouble/guidance_none/r2
- `numeric_numpy_iface_longdouble` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/numeric_numpy_iface_longdouble/guidance_raw/r0
- `numeric_numpy_iface_longdouble` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/numeric_numpy_iface_longdouble/guidance_raw/r1
- `numeric_numpy_iface_longdouble` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified, test_tampering  -  <runs>/numeric_numpy_iface_longdouble/guidance_raw/r2
- `review_clean_norm_scale_docs` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: history_mining  -  <runs>/review_clean_norm_scale_docs/guidance_raw/r0
- `test_fft_utils_norm_scale` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: test_tampering  -  <runs>/test_fft_utils_norm_scale/guidance_none/r0
- `test_fft_utils_norm_scale` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/test_fft_utils_norm_scale/guidance_raw/r0
- `test_fft_utils_norm_scale` `claude-code|us.anthropic.claude-sonnet-5|guidance:raw`: protected_modified  -  <runs>/test_fft_utils_norm_scale/guidance_raw/r1
- `test_scipy_iface_shape_axes` `claude-code|us.anthropic.claude-sonnet-5|guidance:none`: test_tampering  -  <runs>/test_scipy_iface_shape_axes/guidance_none/r0

_Pass rates exclude skipped and errored (not graded) runs. CIs resample tasks, then trials._
