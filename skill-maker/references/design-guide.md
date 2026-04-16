# Design Guide — Agents vs Skills

Reference for deciding what to build and how to design it well.

## When to Build an Agent vs a Skill

### Build an AGENT when:

- The task is **diagnostic** — it figures out what's wrong
- The output is a **recommendation** or **analysis report**
- It follows a **structured SOP** (Standard Operating Procedure)
- It's called **by other skills** as a helper (e.g., a skill calls an agent to analyze data before acting)
- It should run **autonomously** with minimal user interaction
- It needs to be **fast and cheap** (agents typically use haiku or sonnet)

### Build a SKILL when:

- The task **produces a deliverable** — CSV, HTML, markdown, updated files
- It needs **user interaction** during execution (questions, confirmations)
- It should be **triggerable by natural language** (AUTO-ACTIVATE)
- It has **multiple actions** (create, analyze, export, diagnose)
- It **orchestrates** other agents or skills
- It needs **reference files** for complex sub-processes

### The gray area

Some tasks could be either. Use this tiebreaker:

| If the primary output is... | Build a... |
|----------------------------|------------|
| "Here's what's wrong and what to do" | Agent |
| "Here's the file I created for you" | Skill |
| "I analyzed X and scored it 73/100" | Agent (auditor pattern) |
| "I built X based on your answers" | Skill (maker pattern) |

## Comparison Table

| Aspect | Agent | Skill |
|--------|-------|-------|
| **File location** | `.claude/agents/{name}.md` | `.claude/skills/{name}/SKILL.md` |
| **File count** | Single .md file | SKILL.md + optional references/ |
| **Frontmatter** | name, description, tools, model, maxTurns | name, description (with AUTO-ACTIVATE) |
| **User interaction** | Minimal — presents findings | Heavy — asks questions, confirms |
| **Output** | Analysis reports, recommendations | CSV, HTML, markdown, updated files |
| **Model** | Specified in frontmatter (haiku/sonnet) | Inherits from parent session |
| **Triggers** | Slash command only | Slash command + natural language |
| **Complexity** | Single-file, focused | Multi-file, modular |

## Design Principles

### 1. Single responsibility
Each agent or skill does ONE thing well. If you're describing it with "and" — split it.
- Good: "Analyzes ad copy quality"
- Bad: "Analyzes ad copy quality and rewrites underperforming ads"
- Better: Agent analyzes → Skill rewrites (two separate files)

### 2. Explicit data contracts
Always document:
- What files it reads (and whether required or optional)
- What files it writes (and exact paths)
- What it expects to find in those files

### 3. Fail-fast with helpful messages
When a prerequisite is missing, STOP immediately and tell the user:
- What's missing
- Why it's needed
- Which command to run to fix it

### 4. Chain, don't monolith
Build small agents and skills that chain together:
```
/gads-context → pulls data
/search-term-analyzer → analyzes the data
/rsa-maker → creates ads based on analysis
```

### 5. AskUserQuestion for all user interaction (skills only)
Never ask questions as plain text. Always use AskUserQuestion with:
- 2-4 selectable options
- An "Other" option for custom input
- `multiSelect: true` when multiple answers apply

### 6. Suggest the next step
After completing, always tell the user what to run next.

## Common Patterns

### Auditor pattern (agent)
Scores something against a checklist (0-100). Outputs a report with PASS/FAIL/WARN per diagnostic.
```
Phase 0: Load data
Phase 1: Run diagnostics (D01, D02, D03...)
Phase 2: Calculate scores
Phase 3: Write report
```

### Maker pattern (skill)
Creates new content based on user input and context files.
```
Phase 0: Route + prerequisites
E01: Create — interactive questionnaire → write output
E02: Variants — generate alternatives from existing output
E03: Export — format for import into external tool
```

### Analyzer pattern (agent)
Deep-dives into a specific dimension of data. Outputs findings + recommendations.
```
Phase 0: Load data + business context
Phase 1: Segment and filter
Phase 2: Analyze per segment
Phase 3: Prioritize findings
Phase 4: Write report with recommendations
```

### Optimizer pattern (skill)
Takes audit output and applies fixes. Always includes dry-run confirmation.
```
Phase 0: Load audit results
Phase 1: Generate change plan
Phase 2: Show dry-run preview to user
Phase 3: Apply changes (after user confirms)
Phase 4: Write changelog
```

### Gatherer pattern (skill)
Collects data from external sources or user interviews. Writes structured context files.
```
Phase 0: Check what already exists
Phase 1: Gather data (API calls or user questions)
Phase 2: Structure and validate
Phase 3: Write to context file
```

## Naming Conventions

### Agents
`{what-it-analyzes}-{role}`

| Suffix | Use for |
|--------|---------|
| `-analyzer` | Deep analysis of a metric or dimension |
| `-reviewer` | Reviews content for issues |
| `-decider` | Routes to different actions |
| `-auditor` | Scores against a checklist |

### Skills
`{noun}-{role}`

| Suffix | Use for |
|--------|---------|
| `-maker` | Creates new content |
| `-builder` | Generates structured output (HTML, templates) |
| `-gatherer` | Collects and organizes data |
| `-analyzer` | Processes data and produces analysis |
| `-optimizer` | Applies fixes from audit results |
| `-auditor` | Scores against a checklist |
| `-specialist` | Multi-modal skill covering a domain |

## File Path Conventions

| What | Path |
|------|------|
| Agent (client-level) | `clients/{client}/.claude/agents/{name}.md` |
| Agent (hub-level) | `.claude/agents/{name}.md` |
| Skill (client-level) | `clients/{client}/.claude/skills/{name}/SKILL.md` |
| Skill (hub-level) | `.claude/skills/{name}/SKILL.md` |
| Skill references | `clients/{client}/.claude/skills/{name}/references/*.md` |
| Skill output (importable) | `clients/{client}/created/` |
| Skill output (analysis) | `clients/{client}/context/analysis/` |
| Context files | `clients/{client}/context/` |
