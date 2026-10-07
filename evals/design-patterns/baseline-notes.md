# Baseline (no skill)
## B: architecture question (billing.ts 4k lines)
Strong: diagnosis by reasons to change; characterization tests first; Adapter+map not Abstract Factory; outbox not in-process emitter; discriminated union not Builder; entitlements + lint rule; strangler; explicit "not doing".
Gaps:
- Zero questions to the user. Decides alone ("Pick a metric", order "follows the pain" but does not ask which pain).
- No option menu (full pattern vs light adaptation vs nothing) per seam for the user to choose.
- No pattern reference/links; pattern names used loosely ("This is the Observer pattern").
- Note: subagent inherits the user's global CLAUDE.md (Lean/Rumelt), so baseline is inflated vs a stranger's environment.

## A: refactor fixture-shop (user unavailable, questions to QUESTIONS.md)
Strong: characterization tests first (19), tests green after each commit, Strategy for payments (classes + dict), Adapter for legacy SDK, table-driven state (not State classes), left discounts/shipping alone, pinned bugs instead of fixing, listed questions.
Gaps:
- Chose scope alone: no proposal/plan shown before code. Questions only after the work. A real user never saw the options.
- Payment as one class per method in Python, no mention that functions would do. No alternatives offered.
- Config singleton left as hidden global with the reason "not an area that grows"; testability cost not surfaced.
- Notifications: decided "later" alone; no option presented (event hooks vs direct calls).
- LOC 128 -> 222 (+73%). Cost stated, but not weighed with the user before doing it.
- No pattern-level justification table (signal -> pattern -> why -> alternative rejected).
Conclusion: with a strong model the knowledge gap is small. The skill must add: (1) a consult-before-change checkpoint with a refactor map and options per hotspot, (2) explicit "lighter adaptation" choice per language, (3) a consistent inventory method for large repos, (4) accurate pattern references for the edge cases.

## Confound
Both baseline agents ran with the author's global CLAUDE.md (diagnosis first, small batches, vanity metrics, fix the class). This inflates their diagnosis quality. It does not explain the clean gap: nothing in that file says "consult the user before you change code", and neither agent did. Compare GREEN runs only on that gap.
