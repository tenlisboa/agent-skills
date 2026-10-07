# Results

## Round 1 (skill v1.0.0, 2026-10-07)

Model for all runs: Claude Opus 5.5 as a general-purpose subagent. All runs had the global CLAUDE.md of the author (see the confound in `baseline-notes.md`).

### S1: refactor fixture-shop

| Criterion | Baseline (no skill) | With skill |
|---|---|---|
| Refactor Map before any edit, then stop | Fail. It changed code first and wrote questions after the work. | Pass. Six rows, no edit, the turn ended with the choice request. |
| Full, lighter and do-nothing options for each row | Fail. One decision for each area, no options. | Pass. Each row had A, B and C with a line-delta cost. |
| Only the chosen rows applied, one commit per row, tests green | Not applicable | Pass. Choices 1A, 2B, 3A, 4B, 5C, 6C were applied. 1A and 3A were against the recommendation of the agent, and it followed the user. Six commits, tests green after each commit (checked again by the reviewer). |
| No pattern on shipping, `is_weekend`, discounts | Pass | Pass. Shipping went to a lookup table option, discounts to "list of rule functions only if they change". |
| Hidden global cost stated | Fail. "Not an area that grows." | Pass. Row 4 stated the test cost and offered injection with defaults. |
| Bugs pinned, not fixed without consent | Pass (pinned, listed) | Pass. Fixed only bug 2, as the user asked. |

### S2: architecture advice (billing.ts)

| Criterion | Baseline | With skill |
|---|---|---|
| Asks about change pressure, or states an assumption | Fail. No question. | Pass. One question with four concrete guesses. |
| Refactor Map with options for each seam | Fail. One fixed plan. | Pass. Six rows. The answer of the user (Pix, add-ons, NF-e) changed the map: async port for Pix, entitlements table, NF-e as a new row. |
| Sequence, safety net, what the team does not do | Pass | Pass |

### Changes after round 1

- Template: added the slots "Diagnosis", "Bugs found" and "Order". Both agents added these sections on their own.
- Open point: Phase 1 costs one round trip with no content when the inventory is cheap. Kept, because the answer changed three rows of the S2 map.
