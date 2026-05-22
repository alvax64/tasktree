# Companion Repository Mode

Use Companion Repository Mode when task state should be updated independently from the source repository.

Default source and tasktree repository names:

```txt
source repo: my-repo
tasktree repo: my-repo.tasktree
```

## Layout

```txt
my-repo.tasktree/
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

## Update Workflow

1. Enter the companion repo.
2. Run `git status`.
3. If local edits exist, commit, stash, or resolve them before pulling.
4. Fetch/pull before editing.
5. Prefer `git pull --rebase` if the repo uses linear history.
6. Edit the smallest relevant tasktree file.
7. Update detail files, journal, and completed log as needed.
8. Run `python scripts/tasktree_lint.py .` if the lint script is available.
9. Commit with a focused message.
10. Push after meaningful updates.
11. If push is rejected, pull/rebase, resolve conflicts, and push again.
12. Never force-push shared branches unless explicitly permitted.

Recommended commit messages:

```txt
tasktree: initialize backlog
tasktree: add frontend audit tasks
tasktree: update AUD-001 router findings
tasktree: complete BUG-014
tasktree: split refactor tasktree
tasktree: record handoff for agent-a
```

## Multi-Agent Sync Rules

- Pull before editing.
- Commit after meaningful updates.
- Push promptly.
- Prefer small, focused commits.
- Prefer editing the smallest relevant file.
- Use stable IDs to merge changes safely.
- Keep active task lines short.
- Put long notes in detail files.
- Use append-only session logs for high-concurrency work.
- Split files by area, work type, or owner when conflicts repeat.
- Avoid force pushes on shared branches.
- Use PRs if branch protection requires them.
- Treat tasktree status as shared coordination state.

## Conflict Handling

When a Git conflict occurs:

1. Do not choose one side blindly.
2. Identify all task IDs changed on both sides.
3. Preserve all incomplete tasks from both sides.
4. Preserve blockers and human-input statuses.
5. Preserve the most conservative status when evidence differs.
6. If one side marks `[x]` and another keeps a task active, inspect evidence.
7. If evidence is unclear, keep the task active and record a discrepancy.
8. Merge journal entries append-only.
9. Keep both completed-log entries unless exact duplicates.
10. Run tasktree lint/checks if available.
11. Add a journal entry describing conflict resolution.

Status conflict policy:

```txt
[ ] vs [I]  -> [I] if actively in progress, otherwise [ ]
[I] vs [B]  -> [B] unless blocker is obsolete
[Q] vs [x]  -> [x] only with verification evidence
[R] vs [x]  -> [x] only with review or acceptance evidence
[B] vs [x]  -> inspect evidence; if unclear, keep [B]
unknown     -> treat as not done
```

If conflict complexity is high, split the file after resolution to reduce future conflicts.
