# Skill Template

Copy this template and fill in the `{placeholders}`.

## Main file: `SKILL.md`

```markdown
---
name: {skill-name}
description: |
  {One-line description of what the skill does.}
  AUTO-ACTIVATE for: "{trigger 1}", "{trigger 2}",
  "{trigger 3}", "{trigger 4}".
  Also triggered by /{command} command.
---

# {Skill Title}

{One sentence: what this skill creates or does. N execute actions.}

**CRITICAL: All questions to the user MUST use the `AskUserQuestion` tool with selectable options.** Never ask questions as plain text. For every question, provide 2-4 concrete answer options. Use `multiSelect: true` when multiple answers apply.

| Action | Command | What it does |
|--------|---------|-------------|
| {Action 1} | `/{skill-name} {action1}` | {What it does} |
| {Action 2} | `/{skill-name} {action2}` | {What it does} |

## Command Format

` ` `
/{skill-name}                    # Menu of available actions
/{skill-name} {action1}          # E01: {Action 1 name}
/{skill-name} {action2}          # E02: {Action 2 name}
` ` `

**Examples:**
- `/{skill-name} {action1}` — {description}
- `/{skill-name} {action2}` — {description}
- `/{skill-name} {action1} --{flag} "{value}"` — {description with flag}

---

## Data Sources

| File | Required | Purpose |
|------|----------|---------|
| `context/{file}` | Yes | {What it provides} |
| `context/{file}` | Optional | {What it provides} |

---

## Process

---

### Phase 0: Route & Prerequisites

1. **Parse subcommand:**
   - `{action1}` → E01 (read `reference/{execute-file}.md`)
   - `{action2}` → E02 (read `reference/{execute-file}.md`)
   - No subcommand → present menu with AskUserQuestion

2. **Load business.md** — extract vertical. If missing, STOP: tell user to run `/business-context-gatherer` first.

3. **Check prerequisites per action:**

| Action | Prerequisites |
|--------|--------------|
| E01 ({action1}) | {required files} |
| E02 ({action2}) | {required files} |

---

### E01: {Action 1 Title}

**Read `reference/{execute-file}.md` for detailed flow.**

Summary:
1. {Step 1}
2. {Step 2}
3. {Step 3}
4. Write output to `{output-path}`

**Output:** `{output-path}`

---

### E02: {Action 2 Title}

**Read `reference/{execute-file}.md` for detailed flow.**

Summary:
1. {Step 1}
2. {Step 2}
3. Write output to `{output-path}`

**Output:** `{output-path}`

---

## After Any Action

1. **Log to memory:** Append entry to `context/memory/YYYY-MM-DD.md`
2. **Suggest next step:**
   - After E01 → "Run `/{next-command}` to {action}"
   - After E02 → "Run `/{next-command}` to {action}"

---

## Integration Points

### Uses (reads from):
- `context/{file}` — {purpose}

### Produces (writes to):
- `{output-path}` — {what it contains}

### Downstream consumers:
- `/{next-skill}` — uses {output} for {purpose}
```

## Reference file template: `references/execute-{action}.md`

For complex actions, split the detailed logic into a reference file:

```markdown
# Execute: {Action Title}

Detailed execution flow for E0{N} of `/{skill-name}`.

## Prerequisites

- `{file}` must exist (from `/{prerequisite-skill}`)

## Phase 1: {Gather / Load / Prepare}

1. Read `{input-file}`
2. Extract:
   - {data point 1}
   - {data point 2}

## Phase 2: {Process / Analyze / Transform}

For each {unit}:

1. {Step with specific logic}
2. {Decision point}:
   - If {condition A}: {action}
   - If {condition B}: {action}

### {Sub-section for complex logic}

{Detailed rules, formulas, or decision trees}

## Phase 3: {Output / Write / Present}

Write to `{output-path}`:

| Column | Source | Notes |
|--------|--------|-------|
| {col1} | {where it comes from} | {formatting rules} |
| {col2} | {where it comes from} | {formatting rules} |

## Validation

Before writing output, verify:
- [ ] {Check 1}
- [ ] {Check 2}
- [ ] {Check 3}
```

## Frontmatter Field Reference

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | kebab-case, must match folder name |
| `description` | Yes | First line = summary. Include AUTO-ACTIVATE triggers and /command |

## Naming Conventions

Skill names follow: `{noun}-{role}`

| Role suffix | Use when |
|-------------|----------|
| `-maker` | Creates new content (ads, offers, pages) |
| `-builder` | Generates structured output (HTML, templates) |
| `-gatherer` | Collects and organizes data from sources |
| `-analyzer` | Processes data and produces analysis |
| `-optimizer` | Takes audit results and applies fixes |
| `-auditor` | Scores against a checklist (0-100) |
| `-specialist` | Multi-modal skill covering a domain |

**Examples:** `rsa-maker`, `landing-page-builder`, `business-context-gatherer`, `search-term-analyzer`

## Directory Structure

```
.claude/skills/{skill-name}/
├── SKILL.md                    # Main skill definition (always required)
└── references/                 # Optional: detailed execution docs
    ├── execute-{action1}.md    # Detailed flow for action 1
    ├── execute-{action2}.md    # Detailed flow for action 2
    └── {checklist-or-schema}.md # Supporting reference material
```
