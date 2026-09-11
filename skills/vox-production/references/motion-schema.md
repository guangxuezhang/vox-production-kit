# Motion schema
Each shot has `start`, `end`, `narration`, `background`, and ordered `layers`.

Each layer has `id`, `asset`, `z`, `enter`, `hold`, `exit`, and optional `transform` values. `enter` and `exit` are explicit time ranges. Background layers are locked (`locked: true`); people use the highest visual z-index; captions use a separate top-level composition.
