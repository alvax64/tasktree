#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const packageRoot = path.resolve(__dirname, "..");
const skillName = "tasktree";
const copyEntries = [
  "SKILL.md",
  "VERSION",
  "README.md",
  "INSTALL.md",
  "CHANGELOG.md",
  "MIGRATIONS.md",
  "install.sh",
  "agents",
  "references",
  "scripts",
];

function usage(exitCode = 0) {
  const out = exitCode === 0 ? console.log : console.error;
  out(`Usage:
  tasktree install [--agent=codex|claude|claude-project] [--dest=/path/to/tasktree] [--force]
  tasktree update [--agent=codex|claude|claude-project] [--dest=/path/to/tasktree]
  tasktree path [--agent=codex|claude|claude-project] [--dest=/path/to/tasktree]

Defaults:
  --agent=codex installs to \${CODEX_HOME:-~/.codex}/skills/tasktree
  --agent=claude installs to ~/.claude/skills/tasktree
  --agent=claude-project installs to ./.claude/skills/tasktree
`);
  process.exit(exitCode);
}

function parseArgs(argv) {
  const args = {
    command: argv[2],
    agent: process.env.TASKTREE_AGENT || "codex",
    dest: process.env.TASKTREE_DEST || "",
    force: false,
  };

  for (const arg of argv.slice(3)) {
    if (arg === "--force") {
      args.force = true;
    } else if (arg.startsWith("--agent=")) {
      args.agent = arg.slice("--agent=".length);
    } else if (arg.startsWith("--dest=")) {
      args.dest = arg.slice("--dest=".length);
    } else if (arg === "--help" || arg === "-h") {
      usage(0);
    } else {
      console.error(`Unknown argument: ${arg}`);
      usage(2);
    }
  }

  if (!args.command || args.command === "--help" || args.command === "-h") {
    usage(args.command ? 0 : 2);
  }

  return args;
}

function homePath(...parts) {
  const home = process.env.HOME || process.env.USERPROFILE;
  if (!home) {
    throw new Error("Cannot determine home directory. Pass --dest=/path/to/tasktree.");
  }
  return path.join(home, ...parts);
}

function resolveDest(args) {
  if (args.dest) {
    return path.resolve(args.dest);
  }

  switch (args.agent) {
    case "codex": {
      const codexHome = process.env.CODEX_HOME
        ? path.resolve(process.env.CODEX_HOME)
        : homePath(".codex");
      return path.join(codexHome, "skills", skillName);
    }
    case "claude":
      return homePath(".claude", "skills", skillName);
    case "claude-project":
      return path.resolve(process.cwd(), ".claude", "skills", skillName);
    default:
      throw new Error(`Unknown agent: ${args.agent}. Use --dest=/path/to/tasktree for custom agents.`);
  }
}

function rmrf(target) {
  fs.rmSync(target, { recursive: true, force: true });
}

function copyRecursive(src, dest) {
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const entry of fs.readdirSync(src)) {
      copyRecursive(path.join(src, entry), path.join(dest, entry));
    }
    return;
  }

  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
  fs.chmodSync(dest, stat.mode);
}

function install(dest, { force }) {
  if (fs.existsSync(dest)) {
    if (!force) {
      throw new Error(
        `tasktree is already installed at ${dest}\n` +
          "Run `tasktree update` to replace it, or pass --force."
      );
    }
    rmrf(dest);
  }

  fs.mkdirSync(dest, { recursive: true });
  for (const entry of copyEntries) {
    const src = path.join(packageRoot, entry);
    if (fs.existsSync(src)) {
      copyRecursive(src, path.join(dest, entry));
    }
  }
}

function main() {
  const args = parseArgs(process.argv);
  const dest = resolveDest(args);

  if (args.command === "path") {
    console.log(dest);
    return;
  }

  if (args.command === "install") {
    install(dest, { force: args.force });
    console.log(`Installed tasktree to ${dest}`);
    console.log("Restart your agent to pick up the skill.");
    return;
  }

  if (args.command === "update") {
    install(dest, { force: true });
    console.log(`Updated tasktree at ${dest}`);
    console.log("Restart your agent to pick up the updated skill.");
    return;
  }

  console.error(`Unknown command: ${args.command}`);
  usage(2);
}

try {
  main();
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
