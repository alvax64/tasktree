# Installing tasktree

Install `tasktree` by placing this repository in the skills directory used by your agent environment. Keep the folder name as `tasktree`.

## Codex

Canonical install:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/<owner>/tasktree ~/.codex/skills/tasktree
```

If you already cloned it somewhere else:

```bash
mkdir -p ~/.codex/skills
cp -R /path/to/tasktree ~/.codex/skills/tasktree
```

Update:

```bash
cd ~/.codex/skills/tasktree
git pull
```

Smoke check:

```bash
python ~/.codex/skills/tasktree/scripts/tasktree_lint.py --help
```

## Claude-style skill environments

Install or upload the `tasktree` folder wherever the client expects skill packages. The portable files are:

- `SKILL.md`
- `references/templates.md`
- `references/companion-mode.md`
- `scripts/tasktree_lint.py`, if local scripts are supported

The `agents/openai.yaml` file is Codex/OpenAI UI metadata. Other clients can ignore it.

## Generic agents

If your agent has no formal skill system, point it at `SKILL.md` and ask it to follow the workflow. Keep `references/` available so the agent can load templates or companion repository guidance only when needed.

Minimum requirements:

- The agent can read Markdown instructions.
- The agent can edit files in the tasktree or companion repository.
- Git is available if using Companion Repository Mode.

## Compatibility

Tasktree files are plain Markdown. Updating this skill changes the operating guidance for future agent work, but it does not automatically rewrite existing `.tasktree/` or `<repo>.tasktree` repositories.

When release notes mention a format migration, read `MIGRATIONS.md` before updating active tasktree repositories.
