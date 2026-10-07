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

## Round 1, extra scenarios (skill v1.0.0 with the round 1 reference fixes, 2026-10-07)

Same model and the same confound as round 1. These runs tested the modes that S1 and S2 do not reach.

| Scenario | Result | Evidence |
|---|---|---|
| S3: Targeted, named pattern with a counter-signal | Pass | No edit. The agent named the "Do not use when" match (variants differ only in numbers), showed a lookup table sketch and asked. |
| S4: Answer, State or Strategy | Pass | It chose State, gave the lighter form first (union type, transition table) and named two cases where classes do not fit. |
| S5: run without a user | Pass | `REFACTOR_MAP.md` written. Only option B applied in each row. 39 tests pass and 7 commits (checked again by the orchestrator). 6 bugs pinned, none fixed. |
| S6: large real repository (axios fork) | Pass | It found that a new transport is already cheap, and that the real cost is shared rules copied into each adapter. It recommended contract tests first and questioned the premise of the Deno adapter. |

Gaps from the self-reports, applied before round 2: a slot for constraints that apply to the whole map, line deltas marked as estimates, a row for a component that does not exist yet, "Not touching" for hotspots off the path, the lighter option as a sketch in Targeted mode, and reading all compared pattern files in Answer mode.

## Round 2 (skill v1.1.0, 2026-10-07)

Goal: find regressions after the round 1 fixes.

| Scenario | Result | Evidence |
|---|---|---|
| S1: refactor fixture-shop | Pass on the map criteria | Four rows with A, B and C, a recommended order, 4 bugs to pin, and a stop before any edit. The execution step was not run again. |
| S3: Targeted, named pattern with a counter-signal | Fail (regression) | The agent built the classes and named the cost only after the change. |

Cause of the S3 regression: the new rule "the explicit choice of the user wins" let the agent read the first request as the choice. Then it skipped the counter-signal check. Fix in `24977bb`: only a choice that the user makes after the user sees the options counts.

After the fix:

| Run | Result |
|---|---|
| S3 run A | Pass. No edit, options A, B and C with cost, test gaps named. |
| S3 run B | Pass. No edit, lookup table sketch, question. |
| S3 run C | Pass. No edit, lookup table sketch, question. |
| S3 run B, the user insists ("express gets carrier API quotes next month") | Pass. The agent built one class per type with no further argument. Tests first in their own commit, 8 tests pass. It used the reason of the user to add an injection seam. |

An independent reviewer read the whole repository. It found 3 blocking items, for example grep hints that got a second path from a script. The fixes are in `b73b38b`, together with `scripts/check.py` and the CI workflow.

## Round 3 (skill v1.1.0 with the round 2 fixes, 2026-10-07)

| Scenario | Result | Evidence |
|---|---|---|
| S7: Targeted, no pattern named | Pass | A one-row map for `advance` with A (State), B (transition table, recommended) and C. No edit. One bug to pin. |
| S2: architecture advice | Pass | It asked about change pressure first, with three concrete guesses. No map before the answer. |
| S5: run without a user | Pass | The agent reported: map committed first and alone, only rungs 1 to 4, 33 tests pass, 7 commits, 6 bugs pinned and not fixed. |

A third reviewer found 2 blocking rule conflicts and one defect in Flyweight step 4. The fixes are in `a0d98af`.

Gaps from the S5 self-report, closed in `10bc238`:

- The map line "Reply with a choice" had no meaning in a run without a user. `REFACTOR_MAP.md` now lists the applied options in its place.
- "Use a lookup table, list it under Not touching" had two readings. The table is now option B, and it goes under "Not touching" only when the change pressure does not reach it.
- The Strategy stop point had an edge case at exactly four variants. It now stops at three variants or fewer with no planned growth.
- A change in the order of float operations can change the last digit of a total. The playbook now tells the agent to keep the order.

Open gap: SKILL.md does not define the shape of the final report in a run without a user.

## Known limits

- All runs used Claude Opus 5.5 with the global CLAUDE.md of the author. No run used Codex, Cursor or another agent. This is future work.
- Each scenario ran one time per round, except S3 after the fix (three runs).
