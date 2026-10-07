#!/usr/bin/env python3
"""Structural checks for every skill in skills/. Exit code 1 on any error.

Run from the repository root: python3 scripts/check.py
Use --ts to also type-check the TypeScript examples (needs npx).
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERN_SECTIONS = [
    "Intent", "Signals in code", "Do not use when", "Shape", "Refactoring path",
    "Adaptations", "At architecture scale", "Trade-offs", "Neighbors", "Minimal example",
]
errors = []


def err(path, msg):
    errors.append(f"{os.path.relpath(path, ROOT)}: {msg}")


def prose_lines(text):
    """Yield (line number, line) outside code fences, tables and headings."""
    in_code = False
    for n, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.startswith("|") or line.startswith("#"):
            continue
        yield n, re.sub(r"`[^`]*`", "", line)


def check_skill(skill_dir):
    name = os.path.basename(skill_dir)
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        err(skill_dir, "missing SKILL.md")
        return
    text = open(skill_md).read()
    fm = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not fm:
        err(skill_md, "missing frontmatter")
        return
    m = re.search(r"^name: (.+)$", fm.group(1), re.M)
    if not m or m.group(1).strip() != name:
        err(skill_md, f"name must be '{name}'")
    d = re.search(r"^description: (.+)$", fm.group(1), re.M)
    if not d:
        err(skill_md, "missing description")
    elif len(d.group(1)) > 1024:
        err(skill_md, "description over 1024 characters")
    if len(text.split("\n")) > 500:
        err(skill_md, "SKILL.md over 500 lines")

    for md in [skill_md] + sorted(glob.glob(os.path.join(skill_dir, "references", "*.md"))):
        body = open(md).read()
        # Relative links resolve.
        no_code = re.sub(r"`[^`\n]*`", "", re.sub(r"```.*?```", "", body, flags=re.S))
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", no_code):
            if re.match(r"[a-z]+:", target):
                continue
            if not os.path.exists(os.path.join(os.path.dirname(md), target)):
                err(md, f"broken link {target}")
        # Commands: a placeholder must not repeat, and uniq must not read a placeholder as a file.
        for n, line in enumerate(body.split("\n"), 1):
            if re.search(r"(<[a-z/ -]+>) \1", line) or re.search(r"uniq -c <", line):
                err(md, f"line {n}: broken command placeholder")
        # Punctuation rules of the writing style, in prose only.
        for n, line in prose_lines(body):
            if ";" in line:
                err(md, f"line {n}: semicolon in prose")
            if "—" in line or " - " in line.strip()[2:]:
                err(md, f"line {n}: dash used as punctuation")

    for md in sorted(glob.glob(os.path.join(skill_dir, "references", "*.md"))):
        body = open(md).read()
        if "## Intent" not in body:
            continue  # cross-cutting reference, not a pattern file
        found = re.findall(r"^## (.+)$", body, re.M)
        if found != PATTERN_SECTIONS:
            err(md, f"sections {found} differ from the template")
        if "**Source:** https://refactoring.guru/" not in body:
            err(md, "missing Source line")


def check_ts(skill_dir):
    tmp = tempfile.mkdtemp()
    files = []
    for md in sorted(glob.glob(os.path.join(skill_dir, "references", "*.md"))):
        body = open(md).read()
        section = body.split("## Minimal example", 1)
        if len(section) < 2:
            continue
        for i, block in enumerate(re.findall(r"```(?:typescript|ts)\n(.*?)```", section[1], re.S)):
            path = os.path.join(tmp, f"{os.path.basename(md)[:-3]}-{i}.ts")
            open(path, "w").write(block + "\nexport {}\n")
            files.append(path)
    for path in files:
        r = subprocess.run(
            ["npx", "-y", "-p", "typescript", "tsc", "--strict", "--noEmit",
             "--target", "es2022", "--lib", "es2022,dom", path],
            capture_output=True, text=True)
        if r.returncode != 0:
            err(path, "tsc failed: " + r.stdout.strip().split("\n")[0])


for skill_dir in sorted(glob.glob(os.path.join(ROOT, "skills", "*"))):
    if os.path.isdir(skill_dir):
        check_skill(skill_dir)
        if "--ts" in sys.argv:
            check_ts(skill_dir)

if errors:
    print("\n".join(errors))
    print(f"{len(errors)} error(s)")
    sys.exit(1)
print("all checks passed")
