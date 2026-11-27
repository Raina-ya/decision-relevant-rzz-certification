# WP-1 handoff

- Agent / date: Codex (first passes) and Claude (expansion), 2026-11-27
- Branch and last commit: `wp-1-literature-audit` @ 0c7131b,
  `wp-1-systematic-review` @ 7f8bf6d, `wp-1-library-expansion` @ 67ecf4f
  (all merged into main)
- What was done (files): `docs/literature/library.csv` (142 sources),
  `references.bib` (generated), `search_log.csv` (S001-S027),
  `topic_map.csv` (themes and core/adjacent/background tier), `gap_map.md`,
  `novelty_memo.md` (reclassification table), 19 papers classified as read at
  relevant-section level or deeper, including
  CHAI2026 and DENG2026.
- Acceptance criteria:
  - every entry has a DOI or arXiv ID and a reading level: met (tests).
  - novelty memo answers each of C1-C6: met, plus new candidate C7.
  - systematic search reproducible: partially met; queries and dates logged,
    but counts are screened results, not database exports.
- Open questions for the owner: whether to adopt the twirl-free,
  decision-induced framing in `gap_map.md` Section 3 as the chapter thesis.
- What the next WP needs to know: the probe principle (CHAI2026) and the
  three-outcome mechanics (DENG2026) are prior art; do not describe them as
  contributions. Of 142 entries, 108 are abstract-only and 12 are
  bibliographic-only. Three additional entries are reviewed IBM documentation.
- Anything I was unsure about or could not verify: RYBOTYCKI2025's full-text
  RZZ statement; ARUTE2019SUPP calibration details; arXiv:2611.20613 could not
  be read (rate limiting). Forward-citation passes on RUDINGER2025, CHAI2026
  and DENG2026 are still required before G1.
- Literature-pruning candidates are documented separately in
  `docs/literature/redundancy_candidates.md`; no source has been deleted.
