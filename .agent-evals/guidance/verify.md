# repoevals report

## Configurations

| configuration | tasks | runs | pass rate | 95% CI | median agent time (s) | cost $ | tokens | status |
|---|---|---|---|---|---|---|---|---|
| `claude-code|claude-haiku-5-5|guidance:overlay=/Users/denniscvsg/.cache/repoevals/runs/mklfft-guidance/draft` | 5 | 15 | 0.7333 | 0.4–1.0 | 104.4 | 0.33 | 176167 | {'pass': 11, 'fail': 4} |
| `claude-code|claude-haiku-5-5|guidance:raw` | 5 | 15 | 0.6 | 0.2–1.0 | 101.0 | 0.33 | 168072 | {'pass': 9, 'fail': 6} |

## By family

| configuration | family | tasks | pass rate | 95% CI |
|---|---|---|---|---|
| `claude-code|claude-haiku-5-5|guidance:overlay=/Users/denniscvsg/.cache/repoevals/runs/mklfft-guidance/draft` | fix | 1 | 1.0 | 1.0–1.0 |
| `claude-code|claude-haiku-5-5|guidance:overlay=/Users/denniscvsg/.cache/repoevals/runs/mklfft-guidance/draft` | numeric | 1 | 1.0 | 1.0–1.0 |
| `claude-code|claude-haiku-5-5|guidance:overlay=/Users/denniscvsg/.cache/repoevals/runs/mklfft-guidance/draft` | review | 2 | 0.3333 | 0.0–0.6667 |
| `claude-code|claude-haiku-5-5|guidance:overlay=/Users/denniscvsg/.cache/repoevals/runs/mklfft-guidance/draft` | test | 1 | 1.0 | 1.0–1.0 |
| `claude-code|claude-haiku-5-5|guidance:raw` | fix | 1 | 1.0 | 1.0–1.0 |
| `claude-code|claude-haiku-5-5|guidance:raw` | numeric | 1 | 1.0 | 1.0–1.0 |
| `claude-code|claude-haiku-5-5|guidance:raw` | review | 2 | 0.0 | 0.0–0.0 |
| `claude-code|claude-haiku-5-5|guidance:raw` | test | 1 | 1.0 | 1.0–1.0 |

## Paired comparisons (b − a, same tasks)

| a | b | tasks | Δ pass rate | 95% CI | p (sign-flip) | better / worse |
|---|---|---|---|---|---|---|
| `claude-code|claude-haiku-5-5|guidance:overlay=/Users/denniscvsg/.cache/repoevals/runs/mklfft-guidance/draft` | `claude-code|claude-haiku-5-5|guidance:raw` | 5 | -0.1333 | -0.2667–0.0 | 0.5 | 0 / 2 |

## Tasks — `claude-code|claude-haiku-5-5|guidance:overlay=/Users/denniscvsg/.cache/repoevals/runs/mklfft-guidance/draft`

| task | runs | passed | pass@1 | pass@3 | pass^3 |
|---|---|---|---|---|---|
| fix_fft_empty_axes_typeerror | 3 | 3 | 1.0 | 1.0 | 1.0 |
| numeric_irfft_norm | 3 | 3 | 1.0 | 1.0 | 1.0 |
| review_clean_interfaces_hfft | 3 | 1 | 0.333 | 1.0 | 0.0 |
| review_replay_370 | 3 | 1 | 0.333 | 1.0 | 0.0 |
| test_remove_axis | 3 | 3 | 1.0 | 1.0 | 1.0 |

## Tasks — `claude-code|claude-haiku-5-5|guidance:raw`

| task | runs | passed | pass@1 | pass@3 | pass^3 |
|---|---|---|---|---|---|
| fix_fft_empty_axes_typeerror | 3 | 3 | 1.0 | 1.0 | 1.0 |
| numeric_irfft_norm | 3 | 3 | 1.0 | 1.0 | 1.0 |
| review_clean_interfaces_hfft | 3 | 0 | 0.0 | 0.0 | 0.0 |
| review_replay_370 | 3 | 0 | 0.0 | 0.0 | 0.0 |
| test_remove_axis | 3 | 3 | 1.0 | 1.0 | 1.0 |

## Scores — `claude-code|claude-haiku-5-5|guidance:overlay=/Users/denniscvsg/.cache/repoevals/runs/mklfft-guidance/draft`

| task:metric | mean |
|---|---|
| numeric_irfft_norm:case_pass_rate | 1.0 |
| review_clean_interfaces_hfft:precision | 0.0 |
| review_replay_370:f1 | 0.274 |
| review_replay_370:precision | 0.2833 |
| review_replay_370:recall | 0.2667 |
| test_remove_axis:kill_rate | 1.0 |

## Scores — `claude-code|claude-haiku-5-5|guidance:raw`

| task:metric | mean |
|---|---|
| numeric_irfft_norm:case_pass_rate | 1.0 |
| review_clean_interfaces_hfft:precision | 0.0 |
| review_replay_370:f1 | 0.2453 |
| review_replay_370:precision | 0.2517 |
| review_replay_370:recall | 0.2667 |
| test_remove_axis:kill_rate | 1.0 |

## Task health

- `fix_fft_empty_axes_typeerror`: passes in every configuration
- `numeric_irfft_norm`: passes in every configuration
- `test_remove_axis`: passes in every configuration

## Integrity flags (read these transcripts)

- `fix_fft_empty_axes_typeerror` `claude-code|claude-haiku-5-5|guidance:overlay=/Users/denniscvsg/.cache/repoevals/runs/mklfft-guidance/draft`: test_tampering — /Users/denniscvsg/.cache/repoevals/runs/mklfft-verify/fix_fft_empty_axes_typeerror/guidance_overlay__Users_denniscvsg_.cache_repoevals_runs_mklfft-guidance_draft/r0
- `fix_fft_empty_axes_typeerror` `claude-code|claude-haiku-5-5|guidance:raw`: test_tampering — /Users/denniscvsg/.cache/repoevals/runs/mklfft-verify/fix_fft_empty_axes_typeerror/guidance_raw/r1
- `fix_fft_empty_axes_typeerror` `claude-code|claude-haiku-5-5|guidance:raw`: history_mining, test_tampering — /Users/denniscvsg/.cache/repoevals/runs/mklfft-verify/fix_fft_empty_axes_typeerror/guidance_raw/r2
- `numeric_irfft_norm` `claude-code|claude-haiku-5-5|guidance:raw`: test_tampering — /Users/denniscvsg/.cache/repoevals/runs/mklfft-verify/numeric_irfft_norm/guidance_raw/r0

_Pass rates exclude skipped and errored (not graded) runs. CIs resample tasks, then trials._
