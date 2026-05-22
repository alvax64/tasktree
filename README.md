# tasktree

`tasktree` is a Codex skill for keeping durable task state in plain Markdown files. It is meant for coding agents and humans who need a readable record of what is pending, blocked, done, discovered, or ready to hand off.

The default workflow uses a companion repository named `<source-repo>.tasktree`, so task updates can move independently from source-code branches and pull requests. Local in-repo tracking with `.tasktree/` is available, but it is not the recommended default unless the work is a small personal project.

## What It Provides

- A `SKILL.md` with the operating rules agents should follow.
- Templates for tasktree files, config, status legends, details, journals, completed logs, source repo notes, and session logs.
- Companion-repository guidance for Git sync, multi-agent updates, and conflict handling.
- A small lint script for common tasktree mistakes.

The skill does not require a database, service, or custom task manager. Markdown remains the source of truth.

## Repository Layout

```txt
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── companion-mode.md
│   └── templates.md
└── scripts/
    └── tasktree_lint.py
```

## When To Use It

Use `tasktree` when work is likely to outlive one chat turn or one coding session:

- Multi-step implementation plans
- Audits and investigations
- Refactors with follow-up work
- Bug batches
- Multi-agent or branch-heavy work
- Handoffs where another agent or person needs to continue

Avoid it for trivial one-shot answers. It can also sit alongside Jira, Linear, GitHub Issues, or another source of record; it is not intended to replace those systems unless you explicitly choose that.

## Installing As A Skill

Copy or clone this repository into your Codex skills directory, keeping the folder name as `tasktree`.

Common locations:

```txt
$CODEX_HOME/skills/tasktree
~/.codex/skills/tasktree
```

The required file is `SKILL.md`. The `references/`, `agents/`, and `scripts/` directories are optional support files used by this skill.

## Basic Use

Ask Codex to use the skill:

```txt
Use $tasktree to create task tracking for this repository.
```

By default, the skill should suggest Companion Repository Mode and create or use:

```txt
<source-repo>.tasktree/
├── TASKTREE.md
├── README.md
├── config.md
├── status-legend.md
├── journal.md
├── completed.md
├── sessions/
├── details/
└── source-repo.md
```

Default task metadata is intentionally small:

- Status
- Short description
- Detail path

Other fields, such as owner, branch, verification, risk, PR, source commit, or evidence, are optional.

## Linting

The bundled lint script checks Markdown tasktree files for common coordination issues:

- Duplicate task IDs
- Malformed or unknown status markers
- Broken detail links
- Unresolved Git conflict markers

Run it against a tasktree root:

```bash
python scripts/tasktree_lint.py /path/to/repo.tasktree
```

For local in-repo tracking:

```bash
python scripts/tasktree_lint.py .tasktree
```

The linter is a helper, not a required runtime. Manual Markdown editing is still valid.

## Design Constraints

The skill is deliberately conservative:

- Keep active tasktree files short.
- Move long context into detail files.
- Mark `[x]` only with evidence, verification, or explicit acceptance.
- Never delete incomplete tasks.
- Never delete detail files unless explicitly requested.
- Compact completed child tasks only when every child is complete.
- Prefer Companion Repository Mode unless the user has a small personal project.

For the full behavior, read [SKILL.md](SKILL.md).
