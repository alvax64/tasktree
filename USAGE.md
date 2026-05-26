# Using tasktree

This is a prompt cookbook for humans using the `tasktree` skill with coding agents.

## Initialize tracking

```txt
Use $tasktree to initialize task tracking for this repository.
```

Recommended default: Companion Repository Mode in an adjacent repo named `<source-repo>.tasktree`.

## Convert a plan into tasks

```txt
Use $tasktree to convert this plan into tasktree tasks.
```

Useful follow-up:

```txt
Use $tasktree to create detail files for the major tasks and set the next recommended task.
```

## Start work

```txt
Use $tasktree to start AUD-001.2.
```

Expected behavior:

- Mark the task `[I]` if in-progress status is configured.
- Read the linked detail file.
- Record assumptions or missing context before editing source files.

## Record a blocker

```txt
Use $tasktree to mark AUD-001.3 blocked because CI credentials are missing.
```

Expected behavior:

- Mark the task `[B]`.
- Record the blocker reason in the task line or detail file.
- Add it to `Open Blockers` if relevant.

## Complete work

```txt
Use $tasktree to complete BUG-014 with verification from npm test.
```

Expected behavior:

- Record verification evidence.
- Mark the task `[x]`.
- Update the journal.
- Compact completed children only when safe.

## Handoff

```txt
Use $tasktree to create a handoff summary for the next agent.
```

Expected behavior:

- Update touched task statuses.
- Record blockers and unfinished work.
- Update `journal.md` or a session log.
- Set `Next Recommended Task`.

## Compact completed work

```txt
Use $tasktree to compact completed tasks where safe.
```

Expected behavior:

- Compact only parents whose children are all complete.
- Preserve detail files.
- Add a completed-log entry.

## Lint

```txt
Use $tasktree to lint the tasktree.
```

Manual command:

```bash
python scripts/tasktree_lint.py /path/to/repo.tasktree
```

JSON output for agents:

```bash
python scripts/tasktree_lint.py --json /path/to/repo.tasktree
```

Strict mode:

```bash
python scripts/tasktree_lint.py --strict /path/to/repo.tasktree
```

## Agent behavior guarantees

- Incomplete tasks are never silently deleted.
- Stable task IDs are preserved.
- Completed IDs are not reused.
- Blockers are recorded explicitly.
- `[x]` requires evidence, verification, or explicit acceptance.
- Companion Repository Mode is preferred for shared, protected, or long-running work.
- Handoff state is updated before ending a meaningful work cycle.
