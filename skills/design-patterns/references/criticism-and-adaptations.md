# Criticism and Adaptations: When Patterns Hurt

Source: https://refactoring.guru/design-patterns/criticism, https://refactoring.guru/design-patterns/what-is-pattern, https://refactoring.guru/design-patterns/classification

A pattern is a description of a solution, not code to paste. Each one costs indirection, files and reading time.
Use this file to decide between three outcomes: apply the full pattern, apply a lighter adaptation, or apply nothing.
For the smell that started the question, see [smells-to-patterns.md](smells-to-patterns.md).

## The three critiques

### 1. Patterns compensate for missing language features
Many GoF patterns come from C++ and early Java, which had no first-class functions, closures or generators.
In a language with those features, the same intent often needs one function, not a class hierarchy.
Example: a Strategy in Python, JavaScript or Kotlin is usually a function you pass as an argument.
Check the language before you choose the classic class structure. Use the table below.

### 2. One-size-fits-all solutions are inefficient
A catalog entry shows one general structure. Teams copy that structure literally, with every role and interface.
The result fits the book, not the project. Adapt the pattern to the size of the problem.
Drop roles that do nothing. An abstract base with one subclass is a role that does nothing.

### 3. Unjustified use (the golden hammer)
A developer who just learned patterns sees them everywhere. Simple code then gets factories, managers and wrappers.
The cost is real: more files, more jumps to follow a call, slower onboarding.
The benefit is speculative: flexibility for a change that never comes.
Speculative Generality and Lazy Class in [smells-to-patterns.md](smells-to-patterns.md) are the usual results.

## Language features that replace patterns

| Language feature | Replaces or shrinks | Keep the full pattern when |
|---|---|---|
| First-class functions, lambdas | [Strategy](strategy.md), [Command](command.md), [Template Method](template-method.md) | Each variant has several methods or its own state |
| Closures | [Command](command.md) | You need undo, serialization, or a queue that outlives the process |
| Generators, `yield`, lazy sequences | [Iterator](iterator.md) | The language has no generators, or traversal needs reset and peek |
| Pattern matching, sum types, sealed classes | [Visitor](visitor.md), some [State](state.md) | The language has no sum types or exhaustive matching |
| Modules, module-level instances | [Singleton](singleton.md), [Facade](facade.md) | You need lazy init with thread safety and no DI is available |
| Language decorators, higher-order functions, middleware | [Decorator](decorator.md), [Proxy](proxy.md) | You stack wrappers per object at runtime |
| Named arguments with defaults, dataclasses, records | [Builder](builder.md) | Assembly is step-wise or validates across fields |
| `copy`, `structuredClone`, `clone()`, record `with` | [Prototype](prototype.md) | Clones need a registry or custom deep-copy rules |
| DI containers | [Factory Method](factory-method.md), [Abstract Factory](abstract-factory.md), [Singleton](singleton.md) | Creation logic depends on runtime data, not on config |
| Event emitters, signals, reactive streams | [Observer](observer.md) | The platform has no event mechanism you can reuse |
| Enums with methods, transition tables | [State](state.md) | Each state has several behaviors and its own data |
| Generic containers, mixins, traits | Some [Adapter](adapter.md) and [Bridge](bridge.md) cases | Implementations come from code you cannot change |

The intent survives even when the structure goes away. A function argument is still a Strategy.
Name it that way in comments or reviews so the team keeps a shared word for it.

## The YAGNI test

Run this test before you introduce any pattern. Stop at the first "no".

1. **Is the variation real today?** Count the concrete variants in the code now. Two or more is real. One is speculative.
2. **Did the user name the next change?** A dated plan ("the second provider ships in Q3") counts. "Maybe one day" does not.
3. **Rule of three.** Tolerate the first copy. Note the second. Abstract at the third.
4. **Is the cost of change high today?** Measure files touched per change (see [refactoring-playbook.md](refactoring-playbook.md)). If a change takes one file, no pattern can improve it.
5. **Can you undo the pattern cheaply?** If removing it later costs more than adding it now, wait.

If the variation is speculative, write the simplest code. Keep it easy to refactor later.
Good tests and small functions keep the door open. You do not need an abstraction for that.

## Cost signals

Check these numbers before and after you apply a pattern. A pattern must improve at least one without making the others much worse.

| Signal | How to measure | Warning sign |
|---|---|---|
| Indirection count | Hops from the call site to the code that does the work | More than 3 hops for a simple operation |
| Files touched per change | Median files per commit for a typical feature in the area | The number goes up after the refactor |
| Types per feature | New classes or interfaces for one new variant | More than 2 for one variant |
| Single-implementation interfaces | Interfaces with exactly one implementer | Any, unless the second one is dated |
| Onboarding cost | Files a new developer must read to explain one flow | The flow crosses more than 5 files |
| Test setup size | Lines of mocks and fixtures per test | Setup is longer than the assertion code |
| Debug path | Can you follow a call in the debugger without framework hooks? | Calls vanish into event buses or reflection |

## The decision ladder

Try each rung in order. Stop at the first rung that removes the pain.

1. **Nothing.** The code is ugly but stable. Nobody changes it. Leave it.
2. **Classic refactoring.** Extract Method, Move Method, Introduce Parameter Object, delete dead code.
3. **Language idiom.** A function argument, a dict of handlers, a generator, a dataclass, pattern matching.
4. **Lighter adaptation.** The pattern intent with fewer roles. One interface and plain functions, no abstract base, no factory.
5. **Full pattern.** All the roles, only when the variants are many, stateful, or owned by different teams.

## Common misuse to flag

- [Singleton](singleton.md) used as global mutable state. It hides dependencies and blocks parallel tests. Prefer injection.
- A factory that creates one type. Inline it.
- [Visitor](visitor.md) on a hierarchy that grows often. Each new node type breaks every visitor.
- [Observer](observer.md) chains where one event triggers others. Flow becomes hard to trace. Keep the graph shallow.
- [Decorator](decorator.md) stacks so deep that order bugs appear. Document the order or compose in one place.
- [Abstract Factory](abstract-factory.md) with one family. Use plain constructors.
- [Chain of Responsibility](chain-of-responsibility.md) where every handler always runs. That is a list of steps.

## How to present the choice to the user

Give the user a short, explicit choice. Do not apply a full pattern without consent when a lighter option exists.
Use this structure:

```text
Diagnosis: <one sentence on the real constraint, for example "each new carrier edits 6 files">.
Option A, no pattern: <classic refactoring>. Cost: <files, hops>. Limit: <what it does not solve>.
Option B, lighter adaptation: <idiom or reduced pattern>. Cost: <...>. Limit: <...>.
Option C, full <Pattern>: <roles to create>. Cost: <...>. Pays off when: <named condition>.
Recommendation: <A, B or C> because <evidence from the code or the user's stated next change>.
Not doing: <what this choice leaves out>.
```

Rules for the recommendation:

- Base it on evidence: counts of variants, churn data, or a change the user named.
- State what you will not do. Every option must have a tradeoff.
- Say how to escalate later. For example: "If a third carrier arrives, move the function map to Strategy classes."
- If the user picks the full pattern against the evidence, apply it, but keep the roles minimal.
