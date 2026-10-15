# Guidance experiment (repoevals `guidance suggest` / `verify`)

- Evidence: 16 runs of Claude Code on 4 tasks (`review_replay_319`, `review_seeded_interfaces_half`,
  `fix_fft_empty_axes_identity`, `fix_nd_norm_scaling`), with and without the repository's guidance (`evidence.md`).
- `draft/`: files proposed by Claude Code from that evidence (minimal edits: dev commands, a macOS `timeout` note, a
  file map for `mkl_fft/` and `mkl_fft/tests/`, a `CLAUDE.md` importing `AGENTS.md`). Copy over the repository files to try.
- Verification on the 5 other tasks (`verify.md`, 30 attempts, 0 errors): draft 11/15 vs current guidance 9/15,
  Δ pass rate +0.133 (95% CI −0.000 to +0.267): no clear difference with this few tasks.
- Agent: Claude Code through an x86-64 container (`.agent-evals/Dockerfile`, `repoevals.local.toml`).
