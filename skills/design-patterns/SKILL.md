---
name: design-patterns
description: Refactors code and restructures architectures with the 22 Gang of Four design patterns, and shows the user a map of options before any edit. Use when code shows god classes, long switch or if/else chains on a type, duplicated variants, tight coupling to a vendor SDK, hidden globals, over-engineered abstractions, or legacy modules that resist change. Also use when the user asks which pattern fits, whether a pattern is overkill, or how to apply a pattern such as Strategy, Factory Method, Adapter, Observer, State or Decorator.
license: MIT
metadata:
  author: tenlisboa
  version: "1.1.0"
---

# Design Patterns for Refactoring

A pattern is an option, not a goal. Find the places where change hurts. For each place, offer a full pattern, a lighter adaptation and a do-nothing option, and let the user choose. Then apply the choices in small steps that keep the tests green.

The catalog follows the 22 patterns of [Refactoring Guru](https://refactoring.guru/design-patterns). Each pattern has one reference file. The files add signals in code, counter-signals, a refactoring path, adaptations per language and the form of the pattern at architecture scale.

**An informed choice of the user wins.** A choice is informed when the user saw the options and their costs. A pattern named in the first request is not an informed choice yet. Show the options first. After the user confirms, the choice wins over your recommendation, over a "Do not use when" section and over a "stop point".

## Choose the mode

Select the mode from the request before you read any code.

| The request | Mode | What to do |
|---|---|---|
| Asks what a pattern is, compares patterns, or asks which pattern fits | **Answer** | Read the file of each pattern in the question. Answer, and name the lighter form from the "Adaptations" section. No map. |
| Names one location and one pattern ("make this a Strategy") | **Targeted** | Read the pattern file. Then follow the Targeted steps below. |
| Names one location but no pattern ("clean up this function") | **Targeted** | Find the signal in [smells-to-patterns.md](references/smells-to-patterns.md). Present a Refactor Map with one row and end the turn. If the smell routes to no pattern, offer the classic refactoring as option B. |
| Asks to refactor a module, a codebase or an architecture | **Map** | Follow the five phases below. |

### Targeted steps

1. Compare the code with the "Do not use when" section of the pattern file.
2. If a counter-signal matches, stop before you edit. Do this also when the request names the pattern and its form ("one class per type"). Name the counter-signal, show the lighter form in a short sketch (10 lines maximum), and ask which one the user wants.
3. If no counter-signal matches, or the user confirms the pattern, follow the "Refactoring path" of the file. Use Phase 5 below for tests and commits.

## Map mode

### Phase 1: Get the change pressure

The right pattern depends on what will change next. Patterns pay off only where variation is real.

- If the request says what will change ("more payment methods next quarter"), use that and go to Phase 2.
- If the code shows that a stated need is already met, keep the need and mark your doubt "to confirm" in the map.
- If the request does not say what will change, ask one question before the inventory. Give two or three concrete guesses from the file names.
- If you run without a user, write your assumption at the top of the map and mark it "to confirm". You run without a user when the user said not to ask, or in CI or headless mode.

### Phase 2: Inventory (read only)

Do not edit files in this phase.

1. Set the scope. For more than about 2,000 lines or 20 files, find hotspots first with Step 1 of [refactoring-playbook.md](references/refactoring-playbook.md).
2. If you cannot run git or a shell, rank files by size and by the description of the user.
3. Keep a maximum of 7 hotspots for this map. Put the others in "Later waves".
4. For each hotspot, write the observed signal with `path:line`. Route it with [smells-to-patterns.md](references/smells-to-patterns.md).
5. In the commands of the references, replace each placeholder in angle brackets with a real value of the project. Examples are `<src-dir>`, `<test-dir>`, `<area-dir>`, `<path/to/file>`, `<files>`, `<vendor>` and `<test command>`.
6. Note the safety net: the tests that exist, and the characterization tests that are necessary before a change.
7. If the project has no test runner, plan a script that prints the outputs of the entry points for fixed inputs. Diff its output before and after each change. Ask before you add a test framework.

### Phase 3: Decide each hotspot

Use the decision ladder from [criticism-and-adaptations.md](references/criticism-and-adaptations.md) to find the recommendation. The lowest rung that removes the pain is the recommendation. Fill options A, B and C in the map in all cases.

1. **Nothing:** leave the code as it is.
2. **Classic refactoring:** Extract Method, Move Method, Introduce Parameter Object, a lookup table.
3. **Language idiom:** a function, a dict of functions, a closure, a generator, a discriminated union, a module.
4. **Lighter adaptation:** the intent of the pattern with fewer roles.
5. **Full pattern:** all the roles.

In the map, rung 1 is option C, the best of rungs 2 to 4 is option B, and rung 5 is option A. Before you recommend rung 3, 4 or 5, read the pattern file. Check its "Do not use when" section against the code. Check its "Adaptations" section for the language of the project.

In Python, JavaScript, TypeScript, Go, Ruby and Kotlin, a function or a map of functions is usually the default for Strategy, Command and Template Method. If the language has no classes (C, Elixir, shell, SQL), option A is the idiomatic full form. Examples are a struct of function pointers in C or a behaviour in Elixir. If no such form exists, write option A as "none" and give the reason.

### Phase 4: Present the Refactor Map, then stop

The Refactor Map is the required output of Map mode. Produce it before any edit. Fill every slot. Line deltas are estimates: write them with "about".

````markdown
## Refactor Map: <scope>

**Diagnosis:** <one or two sentences: why change is hard here today>
**Change pressure:** <what the user said, or your assumption marked "to confirm">
**Constraints:** <limits for all rows: public API, upstream merges in a fork, security rules, deadlines, or "none">
**Safety net:** <tests that exist> / <characterization tests to add first>

### 1. <hotspot name> (`<path/to/file>:<line>`, or "new" for a component that does not exist yet)
- **Signal:** <what you saw in the code>
- **Options:**
  - **A. Full pattern:** <Pattern> applied here as <short description>. Cost: <new files, about +N lines, extra indirection>.
  - **B. Lighter:** <adaptation>. Cost: <...>.
  - **C. Leave it:** <the condition under which the current code is fine>.
- **Recommendation:** <A, B or C>, because <reason tied to the change pressure>.
- **Question:** <one question that only the user can answer, or "none">

### 2. ...

### Not touching
- `<path>`: <signal that needs no pattern, or hotspot off the path of the change pressure>, because <reason>. No change in this round.

### Bugs found
- `<path:line>`: <behavior>. I will pin it with a test and not fix it, unless you say so. (Write "none" if none.)

### Later waves
- <hotspots outside this map, if any>

**Order:** <the sequence of rows and the reason, for example the row that removes a live risk first>

**Reply with a choice for each row (for example "1A, 2B, 3C") or "apply the recommendations".**
````

After the map, end your turn. Wait for the choice of the user.

When the reply comes:

- If the reply has a choice for each row, apply it.
- If the reply is partial, or has a choice that is not in the list, restate your reading of each row. A row with no choice is C. Confirm before you edit.

If you run without a user, follow these steps:

1. Write the map to `REFACTOR_MAP.md`. If commits are allowed, commit it alone.
2. Apply only recommendations at rungs 1 to 4. A full pattern (rung 5) waits for the confirmation of the user.
3. List the open questions at the end of your report.

At architecture scale, a row is a seam between modules or services, not a function. Take the options from the "At architecture scale" section of each pattern file. Examples: an anti-corruption layer (Adapter), domain events with an outbox (Observer), a module facade for a strangler migration (Facade).

### Phase 5: Apply the chosen rows

Follow [refactoring-playbook.md](references/refactoring-playbook.md). For each chosen row:

1. Add the characterization tests first if the safety net needs them. Commit them alone.
2. Follow the "Refactoring path" of the pattern file. Run the tests after each step.
3. If the path reaches its "stop point" and the pain is gone, tell the user. Continue only if the user chose the full form.
4. Make one or more commits for each row. Do not mix two rows in one commit. Tests for a new seam go in the commit of their row.
5. Keep the behavior. If you find a bug, pin it with a test, list it, and ask before you fix it.

Commit only when the user or the instructions of the repository allow it. If commits are not allowed, stop after each row and show the diff summary and the test result.

After all rows, report: what changed for each row, the line delta, the test result, and the next wave.

## Pattern index

Read only the files that the inventory points to.

| Pattern | Pick it when | File |
|---|---|---|
| Factory Method | Callers use `new` on a concrete type that varies by context | [factory-method.md](references/factory-method.md) |
| Abstract Factory | Families of related objects must match each other (per vendor, per platform) | [abstract-factory.md](references/abstract-factory.md) |
| Builder | Construction has many optional parts or steps, and named arguments do not fix it | [builder.md](references/builder.md) |
| Prototype | Copies of configured objects are cheaper than building them again | [prototype.md](references/prototype.md) |
| Singleton | Usually never. Read it to remove one, or to replace it with injection | [singleton.md](references/singleton.md) |
| Adapter | A third-party or legacy interface does not fit your code | [adapter.md](references/adapter.md) |
| Bridge | Two dimensions vary on their own and subclasses multiply (N x M) | [bridge.md](references/bridge.md) |
| Composite | Clients treat a tree of items and a single item the same way | [composite.md](references/composite.md) |
| Decorator | Cross-cutting behavior (retry, logging, timing, metrics) wraps a call in combinations | [decorator.md](references/decorator.md) |
| Facade | Callers repeat the same sequence of calls into a complex subsystem | [facade.md](references/facade.md) |
| Flyweight | Memory grows with many objects that share most of their state | [flyweight.md](references/flyweight.md) |
| Proxy | Access to an object needs lazy loading, caching, access control or a remote hop | [proxy.md](references/proxy.md) |
| Chain of Responsibility | A request passes through an ordered list of handlers that can stop it | [chain-of-responsibility.md](references/chain-of-responsibility.md) |
| Command | Actions must be queued, logged, retried or undone | [command.md](references/command.md) |
| Iterator | Traversal of a custom collection leaks its internal structure | [iterator.md](references/iterator.md) |
| Mediator | Many components call each other directly after events | [mediator.md](references/mediator.md) |
| Memento | State must be saved and restored without exposing internals | [memento.md](references/memento.md) |
| Observer | One change must notify a list of dependents that grows | [observer.md](references/observer.md) |
| State | Behavior depends on a status, and transitions are spread in `if` chains | [state.md](references/state.md) |
| Strategy | A `switch` selects one variant of an algorithm, and variants grow | [strategy.md](references/strategy.md) |
| Template Method | Variants share a fixed sequence of steps and differ in some steps | [template-method.md](references/template-method.md) |
| Visitor | Many operations run over a stable set of node types | [visitor.md](references/visitor.md) |

Cross-cutting references:

- [smells-to-patterns.md](references/smells-to-patterns.md): 23 code smells with the first refactoring, the pattern candidates and the question that decides. It also has a "change pressure to pattern" table.
- [criticism-and-adaptations.md](references/criticism-and-adaptations.md): when patterns hurt, language features that replace patterns, the YAGNI test and the decision ladder.
- [refactoring-playbook.md](references/refactoring-playbook.md): hotspots, characterization tests, seams, branch by abstraction, strangler fig, parallel change and metrics.

## Common mistakes

| Mistake | Correct action |
|---|---|
| Edit code before the user saw the options | Produce the Refactor Map and end the turn. |
| One class for each variant in Python or TypeScript, with no other option shown | Offer a function or a dict of functions as option B. |
| A pattern on data that only varies by value (rates, prices, labels) | Use a lookup table. List it under "Not touching". |
| A hidden global (Singleton, module state) left out with no comment | State its test cost in the map. Offer explicit injection as an option. |
| A large line increase done before the user weighed it | Put the approximate line delta in the "Cost" slot of each option. |
| A pattern name chosen first, then a place to use it | Start from the signal and the change pressure. Patterns come last. |
| A map with 20 rows for a large codebase | Keep 7 hotspots at most. Put the rest in "Later waves". |
| Bugs fixed during the refactor | Pin the bug with a test, list it and ask. A refactor keeps behavior. |
| A full rewrite of a module in one commit | Use one commit per row and branch by abstraction for big moves. |
