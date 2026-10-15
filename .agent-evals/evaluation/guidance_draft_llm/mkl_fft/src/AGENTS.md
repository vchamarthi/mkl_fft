# AGENTS.md — mkl_fft/src/

C backend for FFT internals.

## Scope
- `mklfft.c.src` — template expanded by `_vendored/process_src_template.py` (via `meson.build`) into `build/<tag>/mklfft.c` at build time.
- `mklfft.h`, `multi_iter.h` — hand-written headers, edited directly.

## Guardrails
- Edit `mklfft.c.src`, never the generated `mklfft.c` under `build/`.
- Editable installs rebuild on `import mkl_fft`; rerun the tests after editing.
- Keep template changes tightly scoped and covered by tests.
- Coordinate with `_pydfti.pyx` when changing function signatures or behavior.
