# tasktree

`tasktree` is a small operating system for work-in-progress task state. It gives coding agents and humans a shared, plain-text place to record what is pending, blocked, done, discovered, verified, and ready to hand off.

## 5-Minute Start

1. Say to your agent:

   ```txt
   Install the skill from https://github.com/alvax64/tasktree/tree/main
   ```

2. Open the source repository you want to track.
3. Ask your agent to initialize task tracking for this repository.
4. Accept the default Companion Repository Mode unless this is a small personal project.
5. Continue work normally. The agent should update task status, blockers, evidence, and handoff notes as meaningful work changes.

Example initialization prompt:

```txt
Use the tasktree skill to initialize task tracking for this repository.
```

If your agent does not support installing directly from a GitHub URL, install manually into that agent's skills directory.

NPM installer:

```bash
npx @alvax64/tasktree install
```

Update later:

```bash
npx @alvax64/tasktree update
```

### Codex

Install from the GitHub repository path:

```txt
Install the skill from https://github.com/alvax64/tasktree/tree/main
```

Manual install:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/alvax64/tasktree ~/.codex/skills/tasktree
```

NPM install:

```bash
npx @alvax64/tasktree install --agent=codex
```

Update later:

```bash
cd ~/.codex/skills/tasktree
git pull
```

Tasktree files are plain Markdown. Updating the skill does not rewrite existing tasktree repositories automatically.

### Claude Code

User-level install:

```bash
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash -s -- --agent=claude
```

NPM user-level install:

```bash
npx @alvax64/tasktree install --agent=claude
```

Project-level install, run from the target project:

```bash
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash -s -- --agent=claude-project
```

NPM project-level install, run from the target project:

```bash
npx @alvax64/tasktree install --agent=claude-project
```

### Other agents

Use a custom destination matching your agent's skills directory:

```bash
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash -s -- --dest "$HOME/.your-agent/skills/tasktree"
```

Or with npm:

```bash
npx @alvax64/tasktree install --dest "$HOME/.your-agent/skills/tasktree"
```

For team or long-running work, prefer installing a tagged release instead of `main`:

```bash
mkdir -p ~/.codex/skills
git clone --branch v0.1.0 https://github.com/alvax64/tasktree ~/.codex/skills/tasktree
```

For a one-command install:

```bash
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash
```

## Mode Decision Table

| Situation | Recommended mode |
| --- | --- |
| Team repo, multiple agents, or long-running work | Companion Repository Mode |
| Protected source repo or branch-heavy work | Companion Repository Mode |
| Existing Jira, Linear, or GitHub Issues | Use tasktree as local coordination, not the source of truth |
| Small personal project | Local `.tasktree/` mode is acceptable |

Most agent work starts cleanly and gets messy later: plans change, branches diverge, chat context disappears, one agent finds work another agent needs, and "done" can mean anything unless evidence is written down. `tasktree` keeps that coordination state in Markdown so it can be read in a diff, edited by hand, committed to Git, and resumed by the next person or agent.

The idea is deliberately simple: active tasks stay short and scannable, long context moves into detail files, completed children get compacted only when safe, and unfinished work is never silently deleted.

The default workflow uses a companion repository named `<source-repo>.tasktree`, so task updates can move independently from source-code branches and pull requests. Local in-repo tracking with `.tasktree/` is available, but it is not the recommended default unless the work is a small personal project.

## A Common Story

You start with a repo and a clear request: audit this area, clean up that module, fix a batch of bugs, or let several agents work through a larger plan. The first pass is easy to follow because everything is still in one conversation.

Then reality shows up. One branch is not ready to merge. A second agent finds a blocker while a third creates follow-up work. Someone marks a task done, but the verification lives only in chat. A useful finding is buried in a transcript. The source repo should not be touched just to update planning notes, but the planning notes still need history, review, and handoff.

`tasktree` is for that point in the work. It gives the effort a small, explicit coordination repo: what is active, what is blocked, what was verified, what was compacted, and what the next person or agent should pick up. It is intentionally less formal than a project-management system and more durable than chat.

## What It Provides

- A `SKILL.md` with the operating rules agents should follow.
- Templates for tasktree files, config, status legends, details, journals, completed logs, source repo notes, and session logs.
- Companion-repository guidance for Git sync, multi-agent updates, and conflict handling.
- A small lint script for common tasktree mistakes.

The skill does not require a database, service, or custom task manager. Markdown remains the source of truth.

## Repository Layout

```txt
.
├── CHANGELOG.md
├── INSTALL.md
├── MIGRATIONS.md
├── README.md
├── SKILL.md
├── USAGE.md
├── VERSION
├── agents/
│   └── openai.yaml
├── examples/
│   ├── companion-repo/
│   └── local-mode/
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

See [INSTALL.md](INSTALL.md) for provider-specific install notes. The short version is: copy or clone this repository into your agent's skills directory, keeping the folder name as `tasktree`.

For agents that support installing from a GitHub URL, say:

```txt
Install the skill from https://github.com/alvax64/tasktree/tree/main
```

For manual installs, place this repository in the skills directory expected by your agent, keeping the folder name as `tasktree`.

Common locations:

```txt
$CODEX_HOME/skills/tasktree
~/.codex/skills/tasktree
```

The required file is `SKILL.md`. The `references/`, `agents/`, and `scripts/` directories are optional support files used by this skill.

## Basic Use

Ask your agent to use the skill:

```txt
Use $tasktree to create task tracking for this repository.
```

See [USAGE.md](USAGE.md) for a prompt cookbook covering initialization, planning, status updates, blockers, handoffs, compaction, and linting.

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

## Using With Claude

Claude-style agent skills also use a `SKILL.md` file with YAML frontmatter and Markdown instructions. To use this repository with a Claude environment that supports skills, keep the same directory shape and install or upload the `tasktree` folder wherever that environment expects skill packages.

For Claude Code, common locations are:

```txt
~/.claude/skills/tasktree
.claude/skills/tasktree
```

Install globally for your user:

```bash
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash -s -- --agent=claude
```

Install into a specific project, run from that project root:

```bash
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash -s -- --agent=claude-project
```

The portable parts are:

- `SKILL.md`
- `references/templates.md`
- `references/companion-mode.md`
- `scripts/tasktree_lint.py`, if the environment can run local scripts

The `agents/openai.yaml` file is specific to OpenAI/Codex UI metadata. Claude clients can ignore it unless they have their own adapter that reads it.

If the Claude environment does not load referenced files automatically, include `SKILL.md` first, then add the relevant reference file only when needed:

- Use `references/templates.md` when initializing or expanding a tasktree.
- Use `references/companion-mode.md` when working in a separate `<source-repo>.tasktree` repository.

## Other Providers And Agents

For agents that do not have a formal skill system, this repository can still be used as a promptable operating guide.

Practical options:

- Point the agent at `SKILL.md` and ask it to follow the workflow.
- Copy the relevant section of `SKILL.md` into the agent's persistent instructions.
- Keep `references/` available as supporting material instead of pasting everything into the prompt.
- Run `scripts/tasktree_lint.py` manually or through the agent when local command execution is available.

Minimum provider requirements:

- The agent can read Markdown instructions.
- The agent can edit files in the tasktree or companion repository.
- Git access is available if using Companion Repository Mode.

Provider-specific metadata files can be added alongside `agents/openai.yaml` if needed. Keep `SKILL.md` as the canonical instructions so the skill remains portable.

## Linting

The bundled lint script checks Markdown tasktree files for common coordination issues:

- Duplicate task IDs
- Malformed or unknown status markers
- Broken detail links
- Unresolved Git conflict markers
- Unknown statuses, including custom statuses not listed in `status-legend.md`

Run it against a tasktree root:

```bash
python scripts/tasktree_lint.py /path/to/repo.tasktree
```

For local in-repo tracking:

```bash
python scripts/tasktree_lint.py .tasktree
```

For machine-readable output:

```bash
python scripts/tasktree_lint.py --json /path/to/repo.tasktree
```

For additional handoff checks:

```bash
python scripts/tasktree_lint.py --strict /path/to/repo.tasktree
```

Strict mode checks `Next Recommended Task` references and warns about dangling detail files.

The linter is a helper, not a required runtime. Manual Markdown editing is still valid.

## Design Constraints

The skill is deliberately conservative:

- Keep active tasktree files short.
- Move long context into detail files.
- Split or refactor oversized tasktrees by source area, source directory, work type, milestone, release, owner, or agent when doing so improves scanning, conflict reduction, or handoff clarity.
- Mark `[x]` only with evidence, verification, or explicit acceptance.
- Never delete incomplete tasks.
- Never delete detail files unless explicitly requested.
- Compact completed child tasks only when every child is complete.
- Prefer Companion Repository Mode unless the user has a small personal project.

For the full behavior, read [SKILL.md](SKILL.md).
