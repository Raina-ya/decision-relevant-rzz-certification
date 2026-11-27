# Rules for every agent working in this repository

The owner is Zhen-Jun Liu. Only the owner approves locks, hardware runs,
preregistration, and owner decisions.

## Non-negotiable rules

1. Do not submit an IBM Quantum hardware job without a written approval in
   `docs/decisions/` naming the exact locked commit and script.
2. Never edit a locked or frozen file. Corrections are new append-only files in
   `errata/`.
3. Do not cite a reference until it is verified and entered in
   `docs/literature/library.csv`; mark abstract-only reading explicitly.
4. Do not use machine learning, pulse control, or unapproved dynamic circuits.
5. Do not amend or force-push. The owner pushes.
6. Do not make result-dependent changes after a lock.

## Evidence labels

Use `[theory, draft]`, `[theory, owner-reviewed]`, `[exact]`, `[sim]`,
`[fake-backend]`, `[hardware-locked]`, `[post-lock]`, or `[literature]` for
every reported number or result.

## Work discipline

- Respect work-package path ownership in `plan/ch4_plan_v1.md`.
- Use branches named `wp-<id>-<short-name>`.
- Do not merge into `main` without the owner-designated integrator.
- Finish a work package with `plan/handoffs/WP-<id>.md`.
- Run `python -m unittest discover -s tests` before each commit.
- Use author `Zhen-Jun Liu <329023927+Raina-ya@users.noreply.github.com>`.

## Required wording

- Before an OSF timestamp, say "prespecified under an internal lock", not
  "preregistered".
- For our recomputation, say "internal recomputation", not "validation".
- Limit conclusions to the tested instance, budget, backend, pair, and time.
- Label untested physical explanations as possible causes or hypotheses.
- Do not claim novelty before the literature gate passes.
- Report inconclusive outcomes as inconclusive.

