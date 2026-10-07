# AGENTS.md

This file gives instructions to AI coding agents (Claude Code, Codex, Cursor, Copilot, and others) that work in this repository.

## Repository purpose

This repository is a collection of agent skills. The [skills](https://github.com/vercel-labs/skills) CLI installs them, and [skills.sh](https://skills.sh) lists them.

## Layout

```
skills/
  <skill-name>/          # kebab-case, equal to the `name` field in SKILL.md
    SKILL.md             # Required. Frontmatter + workflow. Keep it under 500 lines.
    metadata.json        # Version, date, abstract and source links.
    references/          # Optional. Files that the agent reads on demand.
    scripts/             # Optional. Executable helpers.
                         # Test scenarios live in evals/<skill-name>/ at the repository root.
```

## Rules for a new skill

1. Put the skill in `skills/<skill-name>/`. The directory name must be equal to the `name` field.
2. Write a `description` that states when to use the skill. Include the words that a user types.
3. Keep `SKILL.md` short. Move catalogs, tables and long examples to `references/`. A short index table that routes to reference files can stay in `SKILL.md`.
4. Link each reference file directly from `SKILL.md`. Do not chain links more than one level deep.
5. Run the baseline test before you write the skill. Record what an agent does without the skill.
6. Run the same scenarios with the skill. Record the result in `evals/<skill-name>/`. Keep evals out of the skill folder, because the CLI installs that whole folder.
7. Run the checks before a commit. CI runs the same commands.

```bash
python3 scripts/check.py --ts
npx skills add . --list
```

## Writing style

Write skill text in Simplified Technical English (ASD-STE100). Use the imperative for instructions. Use short sentences and the active voice.

## Third-party content

Do not copy text or code from third-party sites. Write original text and link the source. The `design-patterns` skill links each pattern to its page on [Refactoring Guru](https://refactoring.guru/design-patterns), under the site's [content usage policy](https://refactoring.guru/content-usage-policy).
