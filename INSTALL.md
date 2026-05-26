# Installing tasktree

Install `tasktree` by placing this repository in the skills directory used by your agent environment. Keep the folder name as `tasktree`.

## Codex

Ask Codex to install directly from GitHub:

```txt
Install the skill from https://github.com/alvax64/tasktree/tree/main
```

Restart Codex after installation so the skill is loaded.

Canonical install:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/alvax64/tasktree ~/.codex/skills/tasktree
```

Pinned release install:

```bash
mkdir -p ~/.codex/skills
git clone --branch v0.1.0 https://github.com/alvax64/tasktree ~/.codex/skills/tasktree
```

One-command install:

```bash
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash
```

NPM installer:

```bash
npx @alvax64/tasktree install --agent=codex
```

Update with npm:

```bash
npx @alvax64/tasktree update --agent=codex
```

Install script options:

```bash
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash -s -- --agent=codex
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash -s -- --ref=v0.1.0
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash -s -- --force
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

For Claude Code, install globally for your user:

```bash
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash -s -- --agent=claude
```

Or with npm:

```bash
npx @alvax64/tasktree install --agent=claude
```

This installs to:

```txt
~/.claude/skills/tasktree
```

Or install into a specific project, run from that project root:

```bash
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash -s -- --agent=claude-project
```

Or with npm:

```bash
npx @alvax64/tasktree install --agent=claude-project
```

This installs to:

```txt
.claude/skills/tasktree
```

For another agent, pass the exact destination skill directory:

```bash
curl -fsSL https://raw.githubusercontent.com/alvax64/tasktree/main/install.sh | bash -s -- --dest "$HOME/.your-agent/skills/tasktree"
```

Or with npm:

```bash
npx @alvax64/tasktree install --dest "$HOME/.your-agent/skills/tasktree"
```

## Generic agents

If your agent has no formal skill system, point it at `SKILL.md` and ask it to follow the workflow. Keep `references/` available so the agent can load templates or companion repository guidance only when needed.

Minimum requirements:

- The agent can read Markdown instructions.
- The agent can edit files in the tasktree or companion repository.
- Git is available if using Companion Repository Mode.

## Compatibility

Tasktree files are plain Markdown. Updating this skill changes the operating guidance for future agent work, but it does not automatically rewrite existing `.tasktree/` or `<repo>.tasktree` repositories.

When release notes mention a format migration, read `MIGRATIONS.md` before updating active tasktree repositories.

## Publishing checklist

Before publishing a release:

- Update `VERSION`.
- Update `CHANGELOG.md`.
- Add `MIGRATIONS.md` notes if the tasktree file format or migration guidance changed.
- Smoke check the bundled linter:

```bash
python scripts/tasktree_lint.py --help
```

- Commit the release changes.
- Tag the release:

```bash
git tag vX.Y.Z
git push origin main --tags
```

Use `main` for latest installs and release tags for stable team installs.
