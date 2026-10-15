# Audit execution failures

- **Principal source drift:** proposed v9 at `fb822a95` cannot be loaded against
  the later `10dd7284` business-tax item bytes. The coverage principal-source
  guard blocks it. Resolution: use the exact proposed case commit; preserve
  the guard. Regression check: reproduce both published central endpoints and
  the complete existing school companion before computing a new sensitivity.
- **CWIFT text encoding:** pandas' UTF-8 default rejected byte `f1` in the
  official LEA member. Read its names as Latin-1, keep IDs as text, and fail on
  an unexpected header, duplicate ID or nonpositive index. Regression:
  `test_wage_check.py` tests the accented name, leading zero and invalid schema.
- **Clean-export missing inputs:** Git exports omit the ignored base model,
  scaling check and two union-completion line caches. The reproduction wrapper
  copies exactly these four inputs after fixed-hash validation, and stops for
  missing or altered bytes. `test_reproduce.py` tests both failures and exact
  copying; the full clean-export rerun checks the complete call path. The fiscal
  receipt canonicalizes the case path (macOS `/var` resolves to `/private/var`)
  and records the generator separately so dependency coverage is invariant to
  the export location.
- **Clean-export missing history:** the frozen evaluator uses `git show` for
  pinned pension and engine objects. The temporary export now has its own Git
  index and detached HEAD at the frozen commit, reading the original object
  store through alternates. No source refs/index are changed and no branch is
  created. Its end-to-end checks require the original central and companion
  outputs; any failed Git command stops the reproduction.
