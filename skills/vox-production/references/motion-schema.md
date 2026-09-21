# Motion schema
Each shot has `start`, `end`, `narration`, `background`, `focus`, `handoff`, and ordered `layers`. For new episodes, use the validated [director plan](director-plan.md); generic entrance order alone is not a motion design.

Each layer has `id`, `asset`, `cueText`, `cueTimeSeconds`, `purpose`, `action`, `z`, `enter`, `hold`, `exit`, and optional `transform` values. `enter` and `exit` are explicit time ranges. Background layers are locked (`locked: true`); people use the highest visual z-index; captions use a separate top-level composition.
