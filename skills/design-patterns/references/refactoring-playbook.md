# Refactoring Playbook: Large Refactors with Patterns

Source: https://refactoring.guru/refactoring, https://refactoring.guru/refactoring/techniques, https://refactoring.guru/refactoring/smells

Use this file to execute a refactor safely. Use [smells-to-patterns.md](smells-to-patterns.md) to choose what to change.
Use [criticism-and-adaptations.md](criticism-and-adaptations.md) to decide if a pattern is worth its cost.

## Core rules

1. Do not change behavior and structure in the same step.
2. Keep tests green after every step. If a step turns them red, revert the step. Do not debug forward.
3. Apply one pattern per commit, and ideally one per pull request.
4. Prefer many small reversible steps to one large rewrite.
5. Start where change pressure is real. Ugly code that nobody touches can wait.

## Step 1: Find the hotspots

A hotspot is a file that changes often and is hard to read. Churn multiplied by complexity ranks the work.

Replace `<src-dir>` with the source root of the project (for example `src`, `lib`, `app`).
On Windows, run these commands in Git Bash or WSL.

Churn per source file over the last 12 months, without tests:

```bash
git log --since=12.months --no-merges --format= --name-only -- <src-dir> \
  | grep -v '^$' | grep -vE '(^|/)(tests?|__tests__|specs?)/|[._](test|spec)\.|(^|/)test_' \
  | sort | uniq -c | sort -rn | head -30
```

Hotspot score (churn times line count) for source files that still exist, without tests:

```bash
git log --since=12.months --no-merges --format= --name-only -- <src-dir> \
  | grep -v '^$' | grep -vE '(^|/)(tests?|__tests__|specs?)/|[._](test|spec)\.|(^|/)test_' \
  | sort | uniq -c | sort -rn | head -100 \
  | while read -r n f; do
      [ -f "$f" ] && printf '%s\t%s\t%s\n' "$((n * $(wc -l < "$f")))" "$n" "$f"
    done | sort -rn | head -20
```

Cyclomatic complexity per function, any language. Ask the user before you install a tool.

```bash
uvx lizard -w -C 10 -L 60 --sort cyclomatic_complexity <src-dir> | head -40
```

If `uvx` is not available, use `pipx run lizard` with the same arguments.
The `-w` flag prints only the functions over the limits (complexity 10, length 60).

Type-code switches, which are the main lead for [Strategy](strategy.md) and [State](state.md).
The result is a lead, not a measure. Read each match before you act.

```bash
grep -rnE --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist \
  --exclude-dir=build --exclude-dir=vendor \
  --include='*.py' --include='*.js' --include='*.mjs' --include='*.cjs' --include='*.jsx' \
  --include='*.ts' --include='*.tsx' --include='*.java' --include='*.kt' --include='*.go' \
  --include='*.rb' --include='*.cs' --include='*.php' --include='*.swift' --include='*.rs' \
  "(switch *\(|case |elif |else if ).*((^|[^A-Za-z0-9])(type|kind|status|state|mode)|[a-z](Type|Kind|Status|State|Mode))\b" <src-dir> \
  | cut -d: -f1 | sort | uniq -c | sort -rn | head -20
```

Files that change together with a target file (a lead for Shotgun Surgery):

```bash
git log --no-merges --format=%H -- <path/to/file> \
  | xargs -I{} git show --name-only --format= {} \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -15
```

Cross the lists. A file that is high on churn, complexity and type-code switches is the first target.

## Step 2: Pin current behavior with characterization tests

Legacy code often has no tests. Write tests that record what the code does now, not what it should do.

1. Choose the entry point you will refactor behind (a function, an endpoint, a CLI command).
2. Collect real inputs: production samples, fixtures, logs. Cover each branch of the hotspot.
3. Run the code and save the outputs as a golden master (approved snapshot files).
4. Write a test that replays the inputs and compares outputs to the golden master.
5. Remove non-determinism first: fix the clock, seed random values, sort unordered output.
6. Check coverage on the hotspot. Add inputs until each branch you will touch runs at least once.

Tools: ApprovalTests (many languages), `syrupy` (Python), Jest or Vitest snapshots (JavaScript), `insta` (Rust), Verify (.NET).
If an output is wrong today, keep it in the golden master. Pin the bug with a test, list it, and ask the user before you fix it.

## Step 3: Find or make seams

A seam is a place where you can change behavior without editing the code at that place. You need one to test and to swap.

| Seam type | How to create it | Typical next pattern |
|---|---|---|
| Parameter seam | Pass the dependency as an argument with a default | [Strategy](strategy.md) |
| Object seam | Extract an interface and inject the implementation | [Adapter](adapter.md), [Proxy](proxy.md) |
| Module seam | Move all imports of a vendor into one module | [Facade](facade.md), [Adapter](adapter.md) |
| Config seam | Choose the implementation from config or a flag | [Abstract Factory](abstract-factory.md), branch by abstraction |
| Event seam | Emit an event instead of a direct call | [Observer](observer.md) |

Create the seam in its own commit, with no behavior change. The golden master must stay green.

## Step 4: The small-step loop

Repeat this loop for each change:

1. Run the tests. They must be green.
2. Apply one named refactoring (Extract Method, Move Method, Replace Conditional with Polymorphism).
3. Run the tests.
4. Commit with the refactoring name in the message, for example "Extract Method: computeShipping".
5. If the tests fail, take a smaller step. Revert only the files of this step: `git restore -- <files>`.
   Do not run `git reset --hard` without the consent of the user.

Each commit must build and pass. Then you can bisect, revert or stop at any commit.

## Step 5: One pattern per commit or pull request

- Put the classic refactorings that prepare the pattern in earlier commits.
- Introduce the pattern roles in one commit. Migrate callers in the next commits.
- Write the pattern name and the reason in the pull request: "Strategy for carriers. Third carrier ships next sprint."
- Do not mix a pattern with a feature. Ship the refactor first, then the feature on top.

## Step 6: Big moves without a long-lived branch

### Branch by abstraction
Use it to replace a component inside the codebase while you keep shipping from the main branch.

1. Create an abstraction (interface or module) in front of the old component.
2. Move all callers to the abstraction. Ship.
3. Build the new implementation behind the same abstraction. Ship it switched off.
4. Switch callers to the new implementation in small groups, with a flag.
5. Delete the old implementation. Remove the abstraction if it has no other use.

### Strangler fig
Use it to replace a whole subsystem or service at the edge.

1. Put a routing layer (proxy, gateway, [Facade](facade.md)) in front of the old system.
2. Implement one route or use case in the new system.
3. Route that slice to the new system. Compare results in shadow mode when possible.
4. Repeat slice by slice. Remove the old system when it serves no route.

### Parallel change (expand, migrate, contract)
Use it to change a public interface that other code or other teams call.

1. **Expand:** add the new method or field next to the old one. Old callers still work.
2. **Migrate:** move callers one by one. Mark the old interface as deprecated.
3. **Contract:** remove the old interface when no caller uses it. Grep and check logs first.

### Feature flags
- Put the new path behind a flag so you can switch it off without a deploy.
- Give each flag an owner and a removal date. A stale flag is a new Switch Statements smell.
- Remove the flag and the old path in a dedicated commit after rollout.

## Step 7: Sequence many smells in a large codebase

Work on hotspots only. In each hotspot, use this order:

1. Delete dead code and Speculative Generality. Less code means less to move.
2. Compose methods: Extract Method, Decompose Conditional, Rename. Make the structure visible.
3. Move features: Move Method, Extract Class. Put data and behavior together.
4. Organize data: value objects, parameter objects, enums for type codes.
5. Only now, consider patterns where variation is real and change pressure is named.

Do not refactor the whole codebase to one style. Leave stable, cold code as it is.

## Step 8: Measure before and after

Record a baseline before the first commit. Measure again after the refactor and after the next feature in that area.

| Metric | How to measure | Good result |
|---|---|---|
| Files touched per typical change | Median of all files per commit, over the last 20 commits that touch the area | Goes down |
| Cyclomatic complexity | `lizard` average and maximum for the hotspot | Maximum goes down |
| Lines in the hotspot file | `wc -l` | Goes down or spreads to cohesive files |
| Test run time | `time <test command>` | Same or faster |
| Lead time of the next feature | Time from first commit to merge | Goes down |

Median files per commit for an area. The `--full-diff` flag counts all files of each commit, not only the files in `<area-dir>`.

```bash
git log --no-merges --full-diff -n 20 --format='tformat:@' --name-only -- <area-dir> \
  | awk '/^@/{if(c)print c; c=0; next} NF{c++} END{if(c)print c}' \
  | sort -n | awk '{a[NR]=$1} END{print "median files per commit:", a[int((NR+1)/2)]}'
```

Do not report line count or commit count as success by itself. They are vanity metrics without the change cost.

## Step 9: Know when to stop

Stop when one of these is true:

- The change that motivated the refactor now takes one or two files.
- The next step adds indirection and no metric in Step 8 improves.
- The remaining smells are in cold code that nobody plans to change.
- The time budget the user agreed to is spent. Stop at a green commit and report what remains.

At the end, report to the user: what changed, the before and after metrics, what you did not do, and why.
