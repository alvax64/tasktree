# Tasktree Config

Version: 1
Mode: Companion Repository
Root tasktree: TASKTREE.md
Details directory: details
Journal: journal.md
Completed log: completed.md
Status legend: status-legend.md

## Completion

Done statuses:
- [x]

Only [x] counts as complete unless this list changes.

## Default Metadata

- Status
- Short description
- Detail path
- Optional: task ID, updated date, owner or agent, related branch, verification, priority, risk, tags, source commit, PR, estimate, blocker reason, evidence path, or related source files

## Split Policy

Start with one file. Split only when it improves clarity, reduces conflicts, or makes navigation easier.

Refactor or split when the root tasktree is no longer quickly scannable, repeated multi-agent conflicts occur, completed work dominates active work, or a subtree maps cleanly to a source area, source directory, work type, milestone, release, owner, or agent.

When splitting:
- Preserve task IDs.
- Keep incomplete tasks discoverable from the root tasktree.
- Use root `TASKTREE.md` as an index.
- Replace moved subtrees with pointer tasks or section links.
- Update `journal.md`, `Next Recommended Task`, and this config if paths changed.
- Run `tasktree_lint.py --strict` when available.
