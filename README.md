# Agent Skills

A collection of skills for AI coding agents. A skill is a packaged set of instructions and references that an agent loads when a task needs it.

Skills follow the [Agent Skills](https://agentskills.io/) format. They work in Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI and other agents that the [skills](https://github.com/vercel-labs/skills) CLI supports.

[![skills.sh](https://skills.sh/b/tenlisboa/agent-skills)](https://skills.sh/tenlisboa/agent-skills)

## Installation

```bash
npx skills add tenlisboa/agent-skills
```

To install one skill only:

```bash
npx skills add tenlisboa/agent-skills --skill design-patterns
```

## Available Skills

### design-patterns

Refactors code and restructures architectures with 22 of the 23 Gang of Four design patterns, without dogma. The agent finds the places where change hurts and builds a **Refactor Map**. For each place, the map offers a full pattern, a lighter adaptation and a do-nothing option, with the cost of each one. The user chooses, and the agent applies the choices in small steps that keep the tests green.

**Use when:**

- "Refactor this module with design patterns"
- "This class is a god class" or "this switch keeps growing"
- "We will add more payment providers (or formats, or states) next quarter"
- "Which pattern fits here?" or "Is a Strategy overkill for this?"
- "Restructure this monolith" or "put this vendor SDK behind an interface"
- "Remove this Singleton"

**What it covers:**

- Three modes: answer a question, refactor one place, or map a whole module or architecture
- A decision ladder from "leave it" to the full pattern, with the lighter form preferred in languages with first-class functions
- One reference file for each of the 22 patterns. Each file has signals in code, counter-signals and a safe refactoring path with a stop point. It also has adaptations per language, the architecture-scale form, neighbors and a TypeScript example
- A routing index from 23 code smells to the first refactoring and the pattern candidates
- A playbook for large refactors: hotspots from churn and complexity, characterization tests, branch by abstraction, strangler fig, parallel change and metrics

**Example of a map row:**

```markdown
### 1. Payment dispatch (`shop/orders.py:59`)
- **Signal:** a 4-branch if/elif on `order.payment_method`. More methods are planned.
- **Options:**
  - **A. Full pattern:** Strategy with one class per method. Cost: about +60 lines, 4 classes.
  - **B. Lighter:** a dict of payment functions. Cost: about +25 lines.
  - **C. Leave it:** fine if only one or two methods come.
- **Recommendation:** B, because the methods hold no state.
- **Question:** Will a new method need inputs other than the card token?
```

## Skill Structure

```
skills/
  design-patterns/
    SKILL.md          # Workflow: modes, Refactor Map, phases
    metadata.json     # Version and sources
    references/       # One file per pattern, plus smells, criticism and playbook
evals/
  design-patterns/    # Scenarios, fixture code and results of the skill tests
```

## Testing

Each skill has test scenarios in `evals/<skill-name>/`. The scenarios ran with and without the skill, and `results.md` records the difference. See [AGENTS.md](AGENTS.md) to add a skill.

## Credits

The pattern catalog follows [Refactoring Guru](https://refactoring.guru/design-patterns) by Alexander Shvets. The text in this repository is original. Each reference file links to its source page, under the site's [content usage policy](https://refactoring.guru/content-usage-policy).

## License

MIT
