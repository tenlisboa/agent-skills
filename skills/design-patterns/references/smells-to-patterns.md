# Smells to Patterns: Routing Index

Source: https://refactoring.guru/refactoring/smells, https://refactoring.guru/refactoring/techniques, https://refactoring.guru/design-patterns/catalog

Use this file during code inventory. Find the smell, run the hint, then apply the first refactoring.
Consider a pattern only after that. Most smells end with a classic refactoring and no pattern.
Before you apply a pattern, run the tests in [criticism-and-adaptations.md](criticism-and-adaptations.md). To execute, follow [refactoring-playbook.md](refactoring-playbook.md).

Each entry has a **Signal** (what you see), a **Hint** (a lead, not proof), a **First move**, 0 to 3 **Patterns**, and a **Decide** question.

## Quick map

| Smell | Group | Pattern candidates |
|---|---|---|
| Long Method | Bloater | None (Template Method only for a shared skeleton) |
| Large Class | Bloater | Strategy, State, Facade |
| Primitive Obsession | Bloater | State, Strategy (only for behavior-driving type codes) |
| Long Parameter List | Bloater | Builder (rare) |
| Data Clumps | Bloater | None |
| Alternative Classes with Different Interfaces | OO abuser | Adapter (only when you cannot edit one side) |
| Refused Bequest | OO abuser | None |
| Switch Statements | OO abuser | Strategy, State, Factory Method |
| Temporary Field | OO abuser | None |
| Divergent Change | Change preventer | Strategy, Bridge |
| Shotgun Surgery | Change preventer | Facade (rare) |
| Parallel Inheritance Hierarchies | Change preventer | Bridge, Abstract Factory |
| Comments | Dispensable | None |
| Duplicate Code | Dispensable | Template Method, Strategy |
| Data Class | Dispensable | None |
| Dead Code | Dispensable | None |
| Lazy Class | Dispensable | None (often a pattern to remove) |
| Speculative Generality | Dispensable | None (often a pattern to remove) |
| Feature Envy | Coupler | None |
| Inappropriate Intimacy | Coupler | Mediator (many-to-many only) |
| Incomplete Library Class | Coupler | Adapter, Decorator, Facade |
| Message Chains | Coupler | Facade (rare) |
| Middle Man | Coupler | Keep if it is a real Proxy, Decorator, Adapter or Facade |

## Bloaters

### Long Method
- **Signal:** One function does several jobs. You need inner comments to follow it.
- **Hint:** `lizard -L 50 src/` (any language), or `radon cc -s -n C src/` (Python), or the ESLint `max-lines-per-function` rule.
- **First move:** Extract Method, Decompose Conditional, Replace Temp with Query. If locals block extraction, use Replace Method with Method Object.
- **Patterns:** None. [Template Method](template-method.md) only when two or more long methods share one step order.
- **Decide:** Do several methods run the same steps in the same order with different step bodies? If no, stop after Extract Method.

### Large Class
- **Signal:** A class has many fields and methods and changes for unrelated reasons.
- **Hint:** `find src -name '*.*' -exec wc -l {} + | sort -rn | head -20`, then count methods per class.
- **First move:** Extract Class for each responsibility. Use Extract Subclass for rare variants. Use Extract Interface to document what clients use.
- **Patterns:** [Strategy](strategy.md), [State](state.md), [Facade](facade.md).
- **Decide:** What does the extracted part vary on? A family of algorithms gives Strategy. A lifecycle status gives State. Several new classes that clients still need as one entry point give Facade. Nothing varies: plain Extract Class.

### Primitive Obsession
- **Signal:** Money as a float, roles as integer constants, string keys used as field names.
- **Hint:** `grep -rnE "\b(ROLE|TYPE|STATUS|KIND|MODE)_[A-Z_]+ *= *[0-9]+" src/`
- **First move:** Replace Data Value with Object (a value object). Replace Type Code with Class or with an enum.
- **Patterns:** [State](state.md) or [Strategy](strategy.md), through Replace Type Code with State/Strategy.
- **Decide:** Does the code only label data? Use an enum and stop. Does the value change during the object's life and change behavior? State. Is it set once and selects an algorithm? Strategy.

### Long Parameter List
- **Signal:** More than three or four parameters. Call sites pass many literals or `None`.
- **Hint:** `grep -rnE "(def|function|func) \w+\(([^,)]*,){4,}" src/`
- **First move:** Introduce Parameter Object, Preserve Whole Object, Replace Parameter with Method Call.
- **Patterns:** [Builder](builder.md), rarely.
- **Decide:** Is it a constructor with many optional parts, step-wise assembly or cross-field validation? If the language has named arguments with defaults, use them instead of Builder.

### Data Clumps
- **Signal:** The same group of three or more values travels together (host, port, user).
- **Hint:** Grep for a repeated parameter sequence, for example `grep -rn "host, port, user" src/`.
- **First move:** Extract Class, Introduce Parameter Object, Preserve Whole Object. Then move the code that uses the group into the new class.
- **Patterns:** None.
- **Decide:** Does passing the whole object create a dependency you do not want? If yes, keep the primitives.

## Object-orientation abusers

### Alternative Classes with Different Interfaces
- **Signal:** Two classes do the same job with different method names.
- **Hint:** Look for sibling names: `grep -rnE "class \w*(Client|Gateway|Service|Helper)\b" src/`
- **First move:** Rename Method, Move Method, Parameterize Method. Extract Superclass for partial overlap. Then delete one class.
- **Patterns:** [Adapter](adapter.md), only when one side is third-party or frozen.
- **Decide:** Can you edit both classes? If yes, merge them and use no pattern. If no, adapt the frozen one to your interface.

### Refused Bequest
- **Signal:** A subclass ignores inherited members, or overrides them to throw.
- **Hint:** `grep -rnE "raise NotImplementedError|throw new (UnsupportedOperation|NotImplemented)" src/`
- **First move:** Replace Inheritance with Delegation. If inheritance is valid, use Extract Superclass with only the shared part.
- **Patterns:** None. Composition fixes this without a named pattern.
- **Decide:** Is the subclass truly a kind of the parent for all callers? If no, delegate.

### Switch Statements
- **Signal:** The same `switch` or `if/elif` chain over a type code appears in several places.
- **Hint:** `grep -rnE "(switch *\(|case |elif |else if ).*\b(type|kind|status|state|mode)\b" src/`
- **First move:** Extract Method and Move Method to isolate the switch. Then Replace Type Code with Subclasses or State/Strategy, and Replace Conditional with Polymorphism. Use Introduce Null Object for a null branch.
- **Patterns:** [Strategy](strategy.md), [State](state.md), [Factory Method](factory-method.md).
- **Decide:** Is there only one switch with simple branches? Leave it. Does the case value change at runtime with transitions? State. Is it chosen once and selects an algorithm? Strategy, or a map of functions. Does the switch only pick a class to create? Keep it in one Factory Method. That switch is acceptable.

### Temporary Field
- **Signal:** A field has a value only during one operation. It is null at other times.
- **Hint:** Fields set to `None` or `null` in the constructor and guarded by `if self.x is None` elsewhere.
- **First move:** Extract Class with the field and the code that uses it (a method object). Introduce Null Object for the guards.
- **Patterns:** None.
- **Decide:** Must the extracted operation be queued, logged or undone? Only then look at [Command](command.md).

## Change preventers

### Divergent Change
- **Signal:** One class changes for many unrelated reasons. A new product type touches search, display and ordering methods.
- **Hint:** Read the commit subjects for one file: `git log --format=%s -- path/to/file | head -40`.
- **First move:** Extract Class, one class per reason to change.
- **Patterns:** [Strategy](strategy.md), [Bridge](bridge.md).
- **Decide:** How many independent axes vary? One axis with many variants gives Strategy. Two axes that multiply subclasses give Bridge. No axis: plain Extract Class.

### Shotgun Surgery
- **Signal:** One logical change edits many files with small edits.
- **Hint:** Find files that change together with a target: `git log --format=%H -- path/to/file | xargs -I{} git show --name-only --format= {} | sort | uniq -c | sort -rn | head`.
- **First move:** Move Method and Move Field to gather the behavior in one place. Inline Class on the shells that remain.
- **Patterns:** [Facade](facade.md), rarely.
- **Decide:** Are the scattered edits the same call sequence into one subsystem? If yes, put that sequence behind a Facade. If no, gather the code into one module and stop.

### Parallel Inheritance Hierarchies
- **Signal:** Each new subclass in hierarchy A forces a new subclass in hierarchy B, often with matching name prefixes.
- **First move:** Make instances of one hierarchy refer to the other. Then Move Method and Move Field to remove one hierarchy.
- **Patterns:** [Bridge](bridge.md), [Abstract Factory](abstract-factory.md).
- **Decide:** Do the two sides vary independently? Bridge. Must matching members always be created together as a family? Abstract Factory. If the merge makes the code worse, revert and accept the hierarchies.

## Dispensables

### Comments
- **Signal:** Comments explain what the code does, not why.
- **First move:** Extract Variable, Extract Method (name it after the comment), Rename Method, Introduce Assertion.
- **Patterns:** None.
- **Decide:** Does the comment explain a reason or a hard algorithm? If yes, keep it.

### Duplicate Code
- **Signal:** Two fragments are almost the same.
- **Hint:** `npx jscpd src/`, PMD CPD, or `pylint --disable=all --enable=duplicate-code src/`.
- **First move:** Extract Method, Pull Up Method, Extract Superclass, Substitute Algorithm, Consolidate Duplicate Conditional Fragments.
- **Patterns:** [Template Method](template-method.md), [Strategy](strategy.md).
- **Decide:** Are the copies identical? Extract Method, no pattern. Same skeleton, different steps, and the copies already live in subclasses? Template Method. Same skeleton, but no hierarchy or a runtime choice? Pass a function or use Strategy. Wait for the third copy before you abstract.

### Data Class
- **Signal:** A class has only fields and accessors. Callers hold all the logic.
- **First move:** Encapsulate Field, Encapsulate Collection, then Move Method from callers into the class.
- **Patterns:** None.
- **Decide:** Is it a transfer object at a boundary (API schema, DB row)? If yes, it is acceptable. Keep it plain.

### Dead Code
- **Signal:** A variable, parameter, method, class or file has no use.
- **Hint:** `vulture src/` (Python), `npx knip` (TypeScript), `staticcheck ./...` (Go), or IDE "find usages".
- **First move:** Delete it. Use Remove Parameter, Inline Class or Collapse Hierarchy as needed.
- **Patterns:** None.
- **Decide:** Do tests, reflection or external plugins call it? Check before you delete.

### Lazy Class
- **Signal:** A class does too little to justify its cost. Interfaces with one implementation are typical.
- **First move:** Inline Class, Collapse Hierarchy.
- **Patterns:** None. A lazy class is often an unused pattern role. Remove it.
- **Decide:** Does a planned change, with a date, need this class? If no, inline it.

### Speculative Generality
- **Signal:** Abstract classes, hooks or parameters exist "for later" and have no second user.
- **Hint:** Count implementations per interface. One implementation is a lead.
- **First move:** Collapse Hierarchy, Inline Class, Inline Method, Remove Parameter.
- **Patterns:** None. This smell is the usual result of pattern overuse. See [criticism-and-adaptations.md](criticism-and-adaptations.md).
- **Decide:** Is this a framework or library with external users of the hook? If yes, keep it.

## Couplers

### Feature Envy
- **Signal:** A method uses another object's data more than its own.
- **First move:** Move Method. If only part envies, Extract Method, then Move Method.
- **Patterns:** None.
- **Decide:** Is the behavior kept apart on purpose so you can swap it? Then it is already a [Strategy](strategy.md) or [Visitor](visitor.md). Leave it.

### Inappropriate Intimacy
- **Signal:** A class reads or writes private members of another class.
- **Hint:** `grep -rnE "\b[a-z]\w*\._[a-z]\w*" src/` (Python private access on other objects), or reflection calls.
- **First move:** Move Method, Move Field, Extract Class, Hide Delegate, Change Bidirectional Association to Unidirectional.
- **Patterns:** [Mediator](mediator.md), only for many-to-many tangles.
- **Decide:** Are two classes involved, or many with mutual references? Two: move or hide. Many: route their talk through a Mediator.

### Incomplete Library Class
- **Signal:** A library lacks a method you need. Helper functions around it spread through the code.
- **Hint:** `grep -rnE "^(import|from) <vendor>" src/ | cut -d: -f1 | sort -u | wc -l` shows how far the vendor spreads.
- **First move:** Introduce Foreign Method for one or two helpers. Introduce Local Extension for more.
- **Patterns:** [Adapter](adapter.md), [Decorator](decorator.md), [Facade](facade.md).
- **Decide:** Do you need a different interface? Adapter. The same interface with extra behavior? Decorator. One small entry point to a large library? Facade.

### Message Chains
- **Signal:** Calls like `a.b().c().d()` navigate an object graph.
- **Hint:** `grep -rnE "\.\w+\([^)]*\)\.\w+\([^)]*\)\.\w+\(" src/`. Fluent builders and query DSLs are not this smell.
- **First move:** Hide Delegate, or Extract Method on what the end object does, then Move Method up the chain.
- **Patterns:** [Facade](facade.md), rarely.
- **Decide:** Does the chain cross into a subsystem that many callers navigate the same way? If yes, Facade. Do not hide so much that you create Middle Man.

### Middle Man
- **Signal:** A class only forwards calls to another class.
- **First move:** Remove Middle Man, Inline Method.
- **Patterns:** Keep it if it is a real [Proxy](proxy.md), [Decorator](decorator.md), [Adapter](adapter.md) or [Facade](facade.md).
- **Decide:** Does the wrapper add control (lazy load, access check, cache) or isolate a dependency you plan to swap? If yes, keep it and name it for its role. If no, remove it.

## Change pressure to pattern

Use this table when the user names the next change. Offer the lighter adaptation first. Escalate only when the check says yes.

| User says next | Pattern candidate | Lighter adaptation first | Check before full pattern |
|---|---|---|---|
| "New payment providers" | [Strategy](strategy.md) plus [Adapter](adapter.md) per SDK | Map of provider name to function | Do providers differ in flow, or only in API calls? |
| "New output formats" | [Strategy](strategy.md) | Dict of serializer functions | Do formats need shared state or setup? |
| "New operations over a closed AST" | [Visitor](visitor.md) | Pattern matching, sum types, single dispatch | Is the node set stable and the operation set growing? |
| "New states" | [State](state.md) | Enum plus transition table | Does each state carry behavior beyond "allowed next"? |
| "New notification channels" | [Observer](observer.md), [Strategy](strategy.md) per channel | List of callbacks or the platform event emitter | Do subscribers join and leave at runtime? |
| "Swap vendor SDK" | [Adapter](adapter.md), [Facade](facade.md) for large SDKs | One module that owns every import of the SDK | Is a second vendor real and dated? |
| "Undo/redo" | [Command](command.md), [Memento](memento.md) | Stack of immutable state snapshots | Is state too large to snapshot on each step? |
| "Expensive object creation" | [Prototype](prototype.md), [Proxy](proxy.md) (lazy) | Memoize, cache, lazy init | Did you measure the creation cost? |
| "Many optional constructor params" | [Builder](builder.md) | Named args with defaults, dataclass, options object | Is assembly step-wise, or validated across fields? |
| "Logging, caching, retry everywhere" | [Decorator](decorator.md), [Proxy](proxy.md) | Language decorators, middleware, higher-order wrappers | Must you stack wrappers per object at runtime? |
| "Tree structures" | [Composite](composite.md) | Recursive function over plain nested data | Do clients need to treat leaf and group the same way? |
| "Too many objects in memory" | [Flyweight](flyweight.md) | Interning, arrays of primitives | Does a profile show the shared state dominates memory? |
| "New product families per platform or theme" | [Abstract Factory](abstract-factory.md) | One config module that picks the set | Must family members always match? |
| "Subclasses decide what to create" | [Factory Method](factory-method.md) | Pass a constructor or factory function | Is there a class hierarchy already? |
| "New platforms times new features" | [Bridge](bridge.md) | Composition with one injected backend | Do two axes multiply subclasses today? |
| "Request pipeline with optional steps" | [Chain of Responsibility](chain-of-responsibility.md) | Ordered list of handler functions | Can a step stop the chain or reorder at runtime? |
| "Same algorithm, a few steps differ" | [Template Method](template-method.md) | Function with step callbacks | Do variants already live in subclasses? |
| "Many UI parts update each other" | [Mediator](mediator.md) | One controller function that owns the wiring | Are there many-to-many references today? |
| "Traverse a custom collection several ways" | [Iterator](iterator.md) | Generator functions | Does the language lack generators? |
| "Exactly one shared resource" | [Singleton](singleton.md) | Module-level instance or DI container scope | Do tests need to replace it? Then prefer DI. |
| "Control access to a remote or heavy object" | [Proxy](proxy.md) | Wrapper function at the call site | Must callers stay unaware of the control? |
