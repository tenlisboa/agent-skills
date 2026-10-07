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
