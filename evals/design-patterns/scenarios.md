# Scenarios for the design-patterns skill

Run each scenario two times: one time without the skill (baseline) and one time with the skill. Copy `fixture-shop/` to a temporary folder before a run. Run its tests with `python3 -m unittest` (Python 3.9 or later, standard library only).

## S1: refactor a small codebase (fixture-shop)

Prompt:

> Refactor the code in `<copy of fixture-shop>` using design patterns. It is getting hard to maintain and we will add more payment methods and more order statuses next quarter.

The fixture contains these signals on purpose:

| Location | Signal | Expected judgment |
|---|---|---|
| `process_order` payment branch | `if/elif` on payment method, growth announced | Strategy, light form (functions or small classes in a dict) |
| `legacy_pay.py` | third-party SDK with a different interface, "do not edit" | Adapter |
| `advance` | nested `if` on status and action, growth announced | transition table first, State classes only if behavior per state grows |
| shipping branch | values only | lookup table, no pattern |
| discounts | four additive rules, no growth announced | leave or extract functions, no Chain of Responsibility |
| notifications | three inline side effects | ask the user, Observer only if channels grow |
| `Config` singleton | hidden global, test cost | state the cost, offer explicit injection, user decides |
| `is_weekend` | trivial | no pattern |

Pass criteria with the skill:

1. The agent shows a Refactor Map before it changes code, and it stops for the choice of the user.
2. Each row offers a full pattern, a lighter adaptation and a do-nothing option, with a recommendation.
3. After the user answers, the agent changes only the chosen rows, one commit for each row, with green tests after each commit.
4. The agent does not apply a pattern to the shipping table, `is_weekend` or the discounts.

## S2: architecture advice (no files)

Prompt:

> We have a 120k-line Node/TypeScript monolith (Express + Prisma). One `services/billing.ts` file has 4,000 lines: it calls Stripe, Adyen and an in-house bank API directly, each with its own if/else branches; it sends emails, Slack alerts and writes audit logs inline after each charge; invoices are built with a 300-line function that has 15 optional parameters; and there are `if (tenant.plan === 'enterprise')` checks spread across 60 files. Team of 6. We want to restructure it with design patterns. What should we do?

Pass criteria with the skill:

1. The agent asks about change pressure, or states its assumption about it and asks the user to confirm.
2. The answer is a Refactor Map with options per seam, not a single fixed plan.
3. The agent recommends a sequence and a safety net, and it names what the team will not do.

## S3: Targeted, named pattern with a counter-signal

Prompt:

> In `<copy of fixture-shop>`, make the shipping cost calculation in shop/orders.py use the Strategy pattern, with one class per shipping type.

Pass criteria with the skill:

1. The agent makes no edit in the first turn.
2. It names the "Do not use when" match: the shipping types differ only in numbers.
3. It shows the lighter option as a short sketch, gives the cost of each option and asks.
4. If the user then insists with a reason, the agent builds the classes with no further argument, tests first.

## S4: Answer mode

Prompt:

> What's the difference between State and Strategy? In our TypeScript app we have a `Subscription` with status trialing/active/past_due/canceled and each status changes what `renew()`, `cancel()` and `charge()` do. Which one should we use?

Pass criteria with the skill:

1. The agent explains who picks the variant in each pattern and recommends State for this case.
2. It gives the lighter form first (union type, transition table).
3. It makes no map.

## S5: run without a user

Prompt:

> Clean up `<copy of fixture-shop>` with whatever design patterns make sense. I'm going offline for the day, don't ask me anything, just do it, commit as you go, and leave me a report.

Tell the agent that the user will not answer any question.

Pass criteria with the skill:

1. The agent writes `REFACTOR_MAP.md` and commits it first, with its assumption about change pressure marked "to confirm".
2. It applies only rungs 1 to 4 of the decision ladder, never a full pattern.
3. Characterization tests come first in their own commit. Tests pass after each commit.
4. It pins bugs with tests and does not fix them. It lists the open questions at the end of the report.

## S6: large real repository (axios fork)

Setup: a shallow clone of [axios](https://github.com/axios/axios). The agent must not edit the repository.

Prompt:

> I maintain a fork of axios at `<clone>`. We want to add two new transport adapters (one for Deno's native fetch with streaming, one for a custom IPC transport in Electron) and a pluggable retry/caching layer next quarter. Restructure the codebase with design patterns so that this is easy. Where do we start?

Pass criteria with the skill:

1. The agent runs the inventory commands of the playbook and ranks hotspots by churn and complexity.
2. It keeps only the hotspots on the path of the named changes, at most seven.
3. It names a safety net that does not exist yet, for example contract tests for all adapters.
4. It questions a premise that the code contradicts, and it does not edit files.

## S7: Targeted, no pattern named

Prompt:

> The `advance` method in `<copy of fixture-shop>`/shop/orders.py is a mess. Clean it up.

Pass criteria with the skill:

1. The agent shows a one-row Refactor Map with options A, B and C and a recommendation.
2. It recommends the transition table, not State classes, because the states differ only in their allowed transitions.
3. It makes no edit before the choice of the user.
