# Agent Template

Copy this template and fill in the `{placeholders}`.

```markdown
---
name: {agent-name}
description: |
  {One-line description of what the agent diagnoses or analyzes.}
  {Optional: "Do NOT use this agent for anything other than {scope}."}
  Triggered by /{command} command.
tools: [{tool-list}]
model: {haiku|sonnet|opus}
maxTurns: {10-30}
---

# {Agent Title}

{One sentence: what this agent does and why it matters.}

## Command Format

` ` `
/{command} [{optional-argument}]
` ` `

**Examples:**
- `/{command}` — {default behavior}
- `/{command} "{argument}"` — {behavior with argument}

## Data Sources

| File | Required | Purpose |
|------|----------|---------|
| `{path/to/file}` | Yes | {what it provides} |
| `{path/to/file}` | Optional | {what it provides} |

## Process

### Phase 0: Load Data

1. **Read required files:**
   - Read `{data-source-1}` — {what to extract}
   - Read `{data-source-2}` — {what to extract}
2. **Validate data exists:**
   - If `{file}` is missing: "{Helpful error message. Suggest which command to run.}"

### Phase 1: {First Analysis Step}

**Goal:** {What this phase determines.}

For each {unit of analysis}:
1. {Step 1 — what to check}
2. {Step 2 — what to evaluate}
3. {Step 3 — what to decide}

**Decision:**
- **{Outcome A}:** {What it means} → {Next action}
- **{Outcome B}:** {What it means} → {Next action}

### Phase 2: {Second Analysis Step}

{Same structure as Phase 1. Add more phases as needed.}

### Phase 3: Output

Compile findings into the output format below.

## Output Format

Write to `{output-path}`:

` ` `markdown
# {Report Title} — {date}

## Summary
{1-3 sentence overview of findings}

## Findings

### {Finding Category 1}
| {Column} | {Column} | {Column} |
|----------|----------|----------|
| {data}   | {data}   | {data}   |

## Recommendations
1. {Recommended action} — run `/{next-command}`
2. {Recommended action}

## Next Steps
- {Specific next step with command}
` ` `

## After Running

Suggest next steps:
- If {condition} → "Run `/{command}` to {action}"
- If {condition} → "Run `/{command}` to {action}"
```

## Frontmatter Field Reference

| Field | Required | Values | Notes |
|-------|----------|--------|-------|
| `name` | Yes | kebab-case | Must match filename (without .md) |
| `description` | Yes | Multi-line string | First line is the summary. Include trigger command |
| `tools` | Yes | Array of tool names | `Read`, `Glob`, `Grep`, `Write`, `Bash` |
| `model` | Yes | `haiku`, `sonnet`, `opus` | haiku = fast/cheap, sonnet = balanced, opus = deep |
| `maxTurns` | Optional | 10-30 | Limits agent execution length. Default varies |

## Naming Conventions

Agent names follow: `{what-it-analyzes}-{role}`

| Role suffix | Use when |
|-------------|----------|
| `-analyzer` | Deep analysis of a specific metric or dimension |
| `-reviewer` | Reviews content or configuration for issues |
| `-decider` | Routes to different actions based on analysis |
| `-auditor` | Scores against a checklist (0-100) |

**Examples:** `budget-allocation-analyzer`, `copy-quality-reviewer`, `qs-decider`, `placement-content-reviewer`
