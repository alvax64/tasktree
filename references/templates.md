# tasktree Templates

Use these templates when initializing or expanding a tasktree. Keep Markdown plain text and edit only the sections that are useful for the current repository.

## Root Tasktree

```md
# Tasktree

Scope: repo-work
Mode: Companion Repository
Config: config.md
Legend: status-legend.md

repo-work/
├── [ ] AUD-001 Frontend audit -> details/audits/frontend-audit.md
│   ├── [x] AUD-001.1 Review TypeScript config -> details/audits/frontend/typescript-config.md
│   ├── [ ] AUD-001.2 Inspect router architecture -> details/audits/frontend/router-architecture.md
│   └── [B] AUD-001.3 Validate production build checks -> details/audits/frontend/production-build.md
├── [ ] REF-001 Simplify auth module -> details/refactors/auth-module.md
└── [ ] BUG-001 Fix flaky user settings test -> details/bugs/flaky-user-settings-test.md

## Next Recommended Task

- AUD-001.2 Inspect router architecture

## Open Blockers

- AUD-001.3 Blocked pending CI/build-command confirmation.
```

## Config

```md
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
```

## Status Legend

```md
# Status Legend

[ ] Pending - not started.
[x] Done - complete and verified or explicitly accepted.
[I] In progress - actively being worked.
[B] Blocked - cannot proceed without dependency, decision, access, or external input.
[Q] QA - implemented or drafted, awaiting verification.
[R] Review - awaiting human or peer review.
[H] Human input needed - agent needs a decision from a human.
[?] Needs investigation - unclear scope or unknown cause.
[!] Risk / urgent - elevated priority, risk, or time sensitivity.

Completion rule:
Only [x] counts as complete unless config.md explicitly says otherwise.
```

## Full Detail File

```md
# TASK-ID Task Title

Status: [ ]
Area:
Work type:
Owner:
Source repo:
Branch:
Worktree:
Related PR:
Related issue:
Related files:
Created:
Updated:
Completed:
Tasktree path:
Verification:
Evidence:

## Goal

State the desired outcome in one or two paragraphs.

## Context

Record background, assumptions, constraints, and links to relevant tasktree or source files.

## Checklist

- [ ] Step 1
- [ ] Step 2

## Findings

Record discoveries made during investigation or implementation.

## Decisions

Record decisions and why they were made.

## Implementation Notes

Record implementation details, affected files, commands, caveats, and migration notes.

## Verification

Commands, checks, test results, review notes, or acceptance evidence.

## Risks / Blockers

Known risks, blockers, missing access, missing decisions, or external dependencies.

## Follow-ups

Tasks discovered that should become tasktree nodes if they are actionable.

## Completion Summary

Summarize what was completed, what was verified, what remains, and where evidence lives.
```

## Compact Detail File

```md
# TASK-ID Task Title

Status: [ ]
Updated:
Tasktree path:

## Notes

## Verification

## Completion Summary
```

## Journal

```md
# Journal

## YYYY-MM-DD

- Initialized tasktree in Companion Repository Mode.
- Added AUD-001 frontend audit and BUG-001 flaky settings test.
- Assumption: production build verification should include both type checking and bundling until confirmed.
```

## Completed Log

```md
# Completed Log

## YYYY-MM-DD

- Compacted FE-001 after completing FE-001.1 and FE-001.2.
  Summary: Frontend architecture audit completed. Details preserved in details/audits/frontend/.
```

## Companion Source Repo File

Use this as `source-repo.md` in Companion Repository Mode.

```md
# Source Repository

Name:
Default local path:
Remote:
Default branch:
Primary package manager:
Primary test command:
Primary build command:
Notes:
```

## Session Log

Use append-only session logs for high-concurrency work.

```md
# Session Log: YYYY-MM-DD agent-name

Agent:
Source repo branch:
Source repo worktree:
Tasktree commit at start:
Tasktree commit at end:

## Worked On

## Status Changes

## Findings

## Blockers

## New Tasks

## Verification

## Next Recommended Task
```
