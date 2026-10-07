---
name: design-patterns
description: Use when refactoring or restructuring code or architecture with design patterns, or when code shows god classes, long switch or if/else chains on a type, duplicated variants, tight coupling to a vendor SDK, hidden globals, or legacy modules that resist change. Also use when the user asks which pattern fits, whether a pattern is overkill, or how to apply a Gang of Four pattern such as Strategy, Factory, Adapter, Observer, State or Decorator.
license: MIT
metadata:
  author: tenlisboa
  version: "1.0.0"
---

# Design Patterns for Refactoring

A pattern is an option, not a goal. Find the places where change hurts, offer the user a full pattern, a lighter adaptation and a do-nothing option for each place, and let the user choose. Then apply the choices in small steps that keep the tests green.

The catalog follows the 22 patterns of [Refactoring Guru](https://refactoring.guru/design-patterns). Each pattern has one reference file. The files add signals in code, counter-signals, a refactoring path, adaptations per language and the form of the pattern at architecture scale.

## Choose the mode

Select the mode from the request before you read any code.

| The request | Mode | What to do |
|---|---|---|
| Asks what a pattern is, or which pattern fits a snippet | **Answer** | Read the pattern file. Answer, and name the lighter adaptation from its "Adaptations" section. No map. |
| Names one location and one pattern ("make this a Strategy") | **Targeted** | Read the pattern file. If its "Do not use when" section matches the code, say so in one line and ask. Else follow its "Refactoring path". |
| Asks to refactor a module, a codebase or an architecture | **Map** | Follow the five phases below. |

## Map mode

### Phase 1: Get the change pressure

The right pattern depends on what will change next. Patterns pay off only where variation is real.

- If the request says what will change ("more payment methods next quarter"), use that and go to Phase 2.
- If the request does not say it, ask one question before the inventory: "What do you expect to add or change in this code in the next months?" Give two or three concrete guesses from the file names.
- If the user is not available, write your assumption at the top of the map and mark it "to confirm".

### Phase 2: Inventory (read only)

Do not edit files in this phase.

1. Set the scope. If the scope has more than about 2,000 lines or 20 files, find hotspots first. Run the churn and complexity commands in [refactoring-playbook.md](references/refactoring-playbook.md) (Step 1).
2. Keep a maximum of 7 hotspots for this map. Put the others in a "Later waves" list.
3. For each hotspot, write the observed signal with `path:line`. Route it with [smells-to-patterns.md](references/smells-to-patterns.md).
4. Note the safety net: which tests exist, and which characterization tests are necessary before a change.

### Phase 3: Decide each hotspot

Climb the decision ladder from [criticism-and-adaptations.md](references/criticism-and-adaptations.md). Stop at the first step that removes the pain.

1. **Nothing:** leave the code as it is.
2. **Classic refactoring:** Extract Method, Move Method, Introduce Parameter Object, a lookup table.
3. **Language idiom:** a function, a dict of functions, a closure, a generator, a discriminated union, a module.
4. **Lighter adaptation:** the intent of the pattern with fewer roles.
5. **Full pattern:** all the roles.

In the map, rung 1 is option C, the best of rungs 2 to 4 is option B, and rung 5 is option A. Before you recommend rung 3, 4 or 5, read the pattern file. Check its "Do not use when" section against the code. Check its "Adaptations" section for the language of the project. In Python, JavaScript, TypeScript, Go, Ruby and Kotlin, a function or a map of functions is usually the default for Strategy, Command and Template Method.

### Phase 4: Present the Refactor Map, then stop

The Refactor Map is the required output of Map mode. Produce it before any edit. Fill every slot.

````markdown
## Refactor Map: <scope>

**Diagnosis:** <one or two sentences: why change is hard here today>
**Change pressure:** <what the user said, or your assumption marked "to confirm">
**Safety net:** <tests that exist> / <characterization tests to add first>

### 1. <hotspot name> (`path/to/file:line`)
- **Signal:** <what you saw in the code>
- **Options:**
  - **A. Full pattern:** <Pattern> applied here as <short description>. Cost: <new files, approximate line delta, extra indirection>.
  - **B. Lighter:** <adaptation>. Cost: <...>.
  - **C. Leave it:** <the condition under which the current code is fine>.
- **Recommendation:** <A, B or C>, because <reason tied to the change pressure>.
- **Question:** <one question that only the user can answer, or "none">

### 2. ...

### Not touching
- `<path>`: <signal> needs no pattern, because <reason>.

### Bugs found
- `<path:line>`: <behavior>. I will pin it with a test and not fix it, unless you say so. (Write "none" if none.)

### Later waves
- <hotspots outside this map, if any>

**Order:** <the sequence of rows and the reason, for example the row that removes a live risk first>

**Reply with a choice for each row (for example "1A, 2B, 3C") or "apply the recommendations".**
````

After the map, end your turn. Wait for the choice of the user.

If the user said to work without questions, write the map to `REFACTOR_MAP.md`. Apply only the recommended options. List the open questions at the end of your report.

At architecture scale, a row is a seam between modules or services, not a function. Take the options from the "At architecture scale" section of each pattern file. Examples: an anti-corruption layer (Adapter), domain events with an outbox (Observer), a module facade for a strangler migration (Facade).

### Phase 5: Apply the chosen rows

Follow [refactoring-playbook.md](references/refactoring-playbook.md). For each chosen row:

1. Add the characterization tests first if the safety net needs them. Commit them alone.
2. Follow the "Refactoring path" of the pattern file. Run the tests after each step.
3. Stop at the "stop point" of the path if it already removes the pain. Tell the user.
4. Make one commit for each row. Do not mix two patterns in one commit.
5. Keep the behavior. If you find a bug, pin it with a test, list it, and ask before you fix it.

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
| Decorator | Cross-cutting behavior (retry, cache, logging) wraps a call in combinations | [decorator.md](references/decorator.md) |
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
