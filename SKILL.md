---
name: tasktree
description: Maintain plain-text, Markdown-compatible task trees for AI agents and humans working in or alongside repositories. Use when Codex needs to create, update, compact, split, synchronize, lint, or hand off durable task tracking across local .tasktree directories, multi-file tasktrees, or companion repositories named <repo>.tasktree.
---

# tasktree

Use tasktree to keep durable task state in Markdown-compatible files. A tasktree records pending work, completed work, discoveries, blockers, evidence, and handoffs without requiring a database or external issue tracker.

Do not use tasktree for trivial one-shot answers unless the user asks for durable tracking. Do not replace Jira, Linear, GitHub Issues, or a compliance tracker unless the user explicitly wants tasktree as the local companion.

## Core Loop

Before creating, expanding, starting, completing, blocking, splitting, merging, or handing off work, check whether a tasktree exists.

Detection order:

1. `.tasktree/TASKTREE.md`
2. `.tasktree/**/TASKTREE.md`
3. `tasktree/TASKTREE.md`
4. `docs/tasktree/TASKTREE.md`
5. Adjacent companion repo named `<current-repo>.tasktree`
6. User-specified path

If a tasktree exists, update it whenever tasks are created, completed, blocked, or discovered. Before ending a meaningful work cycle, update relevant task statuses, detail files, blockers, journal/session log, completed log when needed, and "Next Recommended Task".

Never silently overwrite an existing tasktree.

## Default Layout

Use `.tasktree/` by default.

Start with one file:

```txt
.tasktree/
└── TASKTREE.md
```

For normal repository work, create:

```txt
.tasktree/
├── TASKTREE.md
├── config.md
├── status-legend.md
├── journal.md
├── completed.md
└── details/
```

Split into multiple tasktree files only when it improves clarity, reduces conflicts, or makes navigation easier.

## Modes

Use Local Mode when the tasktree should live inside the source repository. This is the default for focused work, local audits, refactors, feature plans, migrations, docs cleanup, and bug batches owned by one main human or agent.

Use Companion Repository Mode when task state should live outside the source repository. Default to an adjacent repo named `<source-repo>.tasktree`. Use this for multi-agent work, branch-heavy work, long-running audits/refactors, protected source repositories, or teams that need tasktree commits independent from source-code PRs.

In Companion Repository Mode, read `references/companion-mode.md` before initializing or editing the companion repo.

## Initialization

If no tasktree exists, ask only the minimum useful question:

```txt
I can initialize tasktree in Local Mode inside this repository or Companion Repository Mode in a separate repo named <repo>.tasktree.

Suggested default: Local Mode, unless this is multi-agent, long-running, branch-heavy, or should be independent from the source repo.

Default metadata:
- Status
- Task ID
- Short description
- Detail path
- Updated date
- Owner/agent
- Related branch when relevant
- Verification when relevant

Use these defaults, or specify extra fields such as priority, risk, tags, source commit, PR, estimate, blocker reason, evidence path, or related source files.
```

Use `references/templates.md` for initial `config.md`, `status-legend.md`, `journal.md`, `completed.md`, detail files, companion `source-repo.md`, and session logs.

## Tasktree Format

A tasktree file is Markdown-compatible plain text with a title, optional scope/config notes, a tree-shaped task list, optional "Next Recommended Task", and optional "Open Blockers".

Task line grammar:

```txt
<TREE_PREFIX> <STATUS> <TASK_ID> <SHORT_DESCRIPTION> [-> <DETAIL_PATH>] [#tag ...] [{metadata}]
```

Examples:

```txt
├── [ ] BUG-001 Fix flaky user settings test -> details/bugs/flaky-user-settings-test.md
├── [B] SEC-004 Rotate stale test credentials -> details/security/rotate-test-credentials.md #security #blocked
└── [R] REF-003 Review routing refactor -> details/refactors/routing.md {owner:agent-a updated:2026-05-22}
```

Rules:

- Keep task lines short enough to scan.
- Put long context, findings, decisions, evidence, and verification in detail files.
- Paths are relative to the tasktree file containing the line.
- Use `->` for ASCII-safe detail links; preserve `→` if the existing tasktree uses it.
- Do not wrap task lines unless necessary.
- Do not bury actionable tasks only in prose.

## Statuses

Default statuses:

```md
[ ] Pending
[x] Done
[I] In progress
[B] Blocked
[Q] QA / verification
[R] Review
[H] Human input needed
[?] Needs investigation
[!] Risk / urgent
```

Rules:

- `[ ]` and `[x]` are Markdown task-list-compatible.
- Only `[x]` counts as complete by default.
- Custom statuses are plain text markers, not Markdown checkboxes.
- Custom statuses must be exactly one visible character inside brackets and listed in `status-legend.md`.
- Unknown statuses are not complete.
- Do not treat `[Q]`, `[R]`, `[B]`, `[H]`, `[?]`, `[!]`, or `[I]` as done.

## IDs

Use stable task IDs:

```txt
<PREFIX>-<NUMBER>
<PREFIX>-<NUMBER>.<CHILD_NUMBER>
<PREFIX>-<NUMBER>.<CHILD_NUMBER>.<GRANDCHILD_NUMBER>
```

Recommended prefixes: `BACK`, `AUD`, `REF`, `BUG`, `FEAT`, `DOC`, `TEST`, `SEC`, `PERF`, `MIG`, `REL`, `INF`, `OPS`, `UX`, `DATA`.

ID rules:

- Never renumber existing IDs just to improve ordering.
- Child IDs inherit parent IDs.
- Moving a task to another file must preserve its ID.
- Splitting a task should keep the original as parent and add child IDs.
- Completed IDs must never be reused.
- External issue IDs may be metadata, but tasktree IDs remain independent.
- If duplicate IDs are found, assign a new ID to the newer or less-referenced task and record the correction in the journal.

## Detail Files

Use detail files for major tasks, multi-step tasks, handoff-sensitive work, investigations, audits, refactors, bugs, security work, release work, and anything with important findings or verification.

Detail files are optional for tiny checklist items.

Read `references/templates.md` for full and compact detail file templates.

## Planning Workflow

When converting a plan to tasktree:

1. Read existing tasktree and config.
2. Use one file unless splitting is clearly useful.
3. Convert plan items into task nodes.
4. Assign stable task IDs.
5. Create detail files for major tasks.
6. Keep small leaf tasks inline if detail files add no value.
7. Link tasks to detail files with relative paths.
8. Add assumptions to detail files or journal.
9. Add risks and unknowns as `[?]`, `[B]`, or `[!]`.
10. Update "Next Recommended Task".
11. In Companion Repository Mode, commit/push after the planning update.

## Work Workflow

Before starting:

1. Read the active tasktree file.
2. Read relevant detail files.
3. In Companion Repository Mode, run `git status` and pull/fetch before editing.
4. Mark the task `[I]` if in-progress status is configured.

During work:

1. Record findings in the detail file.
2. Add discovered tasks immediately.
3. Mark blockers `[B]` and record blocker reason.
4. Move tasks to `[Q]` if verification remains.
5. Move tasks to `[R]` if review remains.
6. Do not leave discovered work only in chat.

When completing:

1. Verify the task or record explicit acceptance.
2. Update verification evidence.
3. Mark task `[x]`.
4. Compact completed parents if safe.
5. Update journal.
6. Update completed log if compaction occurred.
7. In Companion Repository Mode, commit/push the update.

## Handoff Workflow

Before ending a meaningful work cycle:

1. Update all touched task statuses.
2. Add newly discovered tasks.
3. Mark blockers.
4. Update detail files.
5. Add verification notes.
6. Compact completed parents when safe.
7. Update `journal.md` or a session log.
8. Set "Next Recommended Task".
9. In Companion Repository Mode, commit/push or record why it could not be done.
10. Summarize active tasks and blockers.

## Completion Compaction

When all subtasks under a parent are complete:

1. Confirm every child is complete according to configured done statuses.
2. Confirm no child has a non-done custom status.
3. Update useful child detail files.
4. Update the parent detail file with a completion summary.
5. Mark the parent `[x]`.
6. Remove completed child lines from the active tasktree file.
7. Add a completed-log or journal entry.
8. Never delete detail files unless explicitly requested.

Never compact a parent with `[B]`, `[Q]`, `[R]`, `[H]`, `[?]`, `[!]`, `[I]`, or unknown-status children.

## Splitting

Start with one file. Split when one or more are true:

- A tasktree file exceeds roughly 120 active task lines.
- A section exceeds roughly 40 active task lines.
- Nesting exceeds 3-4 levels and becomes hard to scan.
- Multiple agents or humans edit the same section concurrently.
- A domain has independent ownership.
- Unrelated workstreams are mixed together.
- Detail paths make the root tasktree noisy.
- Merge conflicts happen repeatedly.
- A task family has its own lifecycle.

When splitting, preserve IDs, statuses, and detail links; fix relative paths; add a journal entry; and prefer a dedicated commit in Companion Repository Mode.

## Safety Rules

- Never delete incomplete tasks.
- Never mark a task `[x]` without verification, evidence, or explicit acceptance.
- Never compact a parent if any child is not complete.
- Never remove children with custom non-done statuses.
- Never silently overwrite a tasktree.
- Never invent completed work.
- Never reuse task IDs.
- Never delete detail files unless explicitly requested.
- Never hide discovered work only in chat.
- If tasktree and source repo disagree, record the discrepancy.
- If unsure, create a finding or blocker instead of marking done.
- If a task was completed outside the session, note the evidence.
- Preserve audit history in journal, completed log, or detail files.

## Optional Linting

If this skill directory includes `scripts/tasktree_lint.py`, run it against a tasktree root when useful:

```bash
python scripts/tasktree_lint.py .tasktree
```

Use lint results to catch duplicate IDs, malformed statuses, broken detail links, and unresolved conflict markers. Plain Markdown remains canonical even if tooling exists.
