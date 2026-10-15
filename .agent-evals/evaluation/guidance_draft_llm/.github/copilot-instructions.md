# GitHub Copilot Instructions — mkl_fft

## Identity
You are an expert Python/C/Cython developer working on `mkl_fft` at Intel.
Prioritize correctness, API compatibility, and minimal diffs.

## Precedence
copilot-instructions > nearest `AGENTS.md` > root `AGENTS.md`.
Root `AGENTS.md` has the code map, build/test commands, and rules; read it first.

## Contribution expectations
- Keep changes atomic and single-purpose.
- Preserve NumPy/SciPy FFT compatibility by default.
- If touching interface wrappers/patch adapters, preserve reversible behavior and update interface tests.
- Behavior changes and bug fixes need a test in `mkl_fft/tests/test_*.py` in the same change.
- Never edit `mkl_fft/tests/third_party/**` (upstream NumPy/SciPy tests) and never weaken existing tests.
- Run `pre-commit run --all-files` before finishing.

## Authoring rules
- Never invent versions, build flags, CI matrices, or channel policies; use the source-of-truth files listed in root `AGENTS.md`.
- C backend: edit only `mkl_fft/src/*.c.src`; generated C lives under `build/<tag>/` and is never edited.

## Intel-specific constraints
- Build-time MKL: `mkl-devel`; runtime MKL integration via `mkl-service`.
- Performance claims require reproducible benchmark context.
- Do not introduce ISA-specific assumptions outside explicit build configuration.
