---
name: skill-maker
description: |
  Guided builder for creating new agents and skills from scratch.
  AUTO-ACTIVATE for: "create a skill", "build a skill", "make a skill",
  "create an agent", "build an agent", "make an agent",
  "new skill", "new agent", "skill maker", "agent maker",
  "skill builder", "agent builder".
  Also triggered by /skill-maker command.
---

# Skill Maker

Interactive builder that guides you through creating a new agent or skill from scratch. Asks structured questions, validates your design, and writes all files in the correct format.

**CRITICAL: All questions to the user MUST use the `AskUserQuestion` tool with selectable options.** Never ask questions as plain text. For every question, provide concrete answer options the user can select from. The user can always pick "Other" for custom input. Use `multiSelect: true` when multiple answers apply.

| Action | Command | What it does |
|--------|---------|-------------|
| Create agent | `/skill-maker agent` | Guided agent builder → writes `.claude/agents/{name}.md` |
| Create skill | `/skill-maker skill` | Guided skill builder → writes `.claude/skills/{name}/SKILL.md` |
| Browse examples | `/skill-maker examples` | Show annotated examples of existing agents and skills |

## Command Format

```
/skill-maker                    # Menu — choose agent or skill
/skill-maker agent              # Jump straight to agent builder
/skill-maker skill              # Jump straight to skill builder
/skill-maker examples           # Browse annotated examples
```

**Examples:**
- `/skill-maker` — Pick what to build
- `/skill-maker agent` — Build a new diagnostic agent
- `/skill-maker skill` — Build a new action skill

## Path Resolution

**Must be run from the hub root or inside a client folder.**

To find the hub root:
1. Check current directory for `main-config.json` or `clients/` directory
2. If not found, walk up parent directories until found
3. The hub root is where `main-config.json` lives

If the current directory is inside a client subfolder (`clients/<name>/`), use that client as the default target.

## Data Sources

| File | Required | Purpose |
|------|----------|---------|
| `reference/agent-template.md` | Yes | Agent file template |
| `reference/skill-template.md` | Yes | Skill file template |
| `reference/design-guide.md` | Yes | Design principles and conventions |
| Existing agents in target client | Optional | Reference for naming and style |
| Existing skills in target client | Optional | Reference for naming and style |

## Process

### Phase 0: Route & Prerequisites

1. **Parse subcommand:**
   - `agent` → E01 (read `reference/agent-template.md` + `reference/design-guide.md`)
   - `skill` → E02 (read `reference/skill-template.md` + `reference/design-guide.md`)
   - `examples` → E03 (show annotated examples)
   - No subcommand → ask via AskUserQuestion: "What do you want to build?"
     - Options: "Agent — diagnoses and recommends" / "Skill — executes and creates deliverables" / "Not sure — show me the difference"
     - If "Not sure" → show the comparison from `reference/design-guide.md`, then ask again

2. **Determine target client:**
   - If cwd is inside `clients/<name>/` → use that client, confirm with user
   - If cwd is hub root → ask via AskUserQuestion: "Which client should this be created for?"
     - Options: list all client folders from `clients/`, plus "Hub-level (shared across all clients)"
   - Hub-level agents go in `.claude/agents/`, hub-level skills go in `.claude/skills/`

---

### E01: Build an Agent

**Read `reference/agent-template.md` and `reference/design-guide.md` before starting.**

Walk through these questions one at a time via AskUserQuestion.

#### Step 1: Purpose

Ask: "What should this agent diagnose or analyze?"
- Options: generate 3-4 example purposes based on common PPC patterns, plus "Other (describe it)"
- Examples: "Analyze campaign budget allocation efficiency" / "Diagnose low conversion rates" / "Review ad copy quality" / "Other"

Follow up: "Describe the specific problem this agent solves in 1-2 sentences."
- This becomes the agent's core purpose statement

#### Step 2: Name

Based on the purpose, suggest 3 name options following kebab-case convention.

Ask: "What should the agent be called?"
- Options: your 3 suggestions plus "Other"
- Naming convention: `{what-it-does}-{analyzer|reviewer|decider|auditor}`
- Examples: `budget-allocation-analyzer`, `conversion-drop-decider`, `copy-quality-reviewer`

Validate: kebab-case, descriptive, ends with role suffix.

#### Step 3: Trigger command

Suggest a slash command based on the name.

Ask: "What slash command should trigger this agent?"
- Options: 2-3 suggestions plus "Other"
- Convention: `/command-name` (short, memorable)

#### Step 4: Input data

Ask: "What data does this agent need to read?"
- Options (multiSelect): "Google Ads CSV data (keywords, campaigns, etc.)" / "Business context (business.md)" / "Brand context (brand.md)" / "Analysis reports from other skills" / "Landing page content" / "Competitor data" / "Other"

For each selected source, ask: "Which specific file(s)?"
- Show known file paths from `context/` structure

#### Step 5: Analysis process

Ask: "How should the agent analyze the data? Describe the steps."
- Guide them through defining 2-5 analysis phases
- For each phase, ask:
  - "What does this phase do?"
  - "What does it look for?"
  - "What decision does it make?"

#### Step 6: Output format

Ask: "How should the agent present its findings?"
- Options: "Markdown report with sections" / "Severity-rated issue list" / "Decision tree (recommend next action)" / "Scored checklist (0-100)" / "CSV with flagged items" / "Other"

Ask: "Where should the output be written?"
- Options: "Display to user only" / "`context/analysis/{name}.md`" / "Other path"

#### Step 7: Downstream actions

Ask: "After this agent runs, what should the user do next?"
- Options (multiSelect): list existing skills that might be relevant, plus "Other" and "No specific next step"

#### Step 8: Model selection

Ask: "How complex is the analysis?"
- Options:
  - "Simple pattern matching and flagging → haiku (fast, cheap)"
  - "Multi-step reasoning and nuanced judgment → sonnet (balanced)"
  - "Deep strategic analysis requiring expert reasoning → opus (powerful, slower)"

#### Step 9: Tools needed

Ask: "What tools does this agent need?"
- Options (multiSelect): "Read (read files)" / "Glob (find files by pattern)" / "Grep (search file contents)" / "Write (write output files)" / "Bash (run scripts/commands)"
- Default suggestion based on the workflow described

#### Step 10: Review & confirm

Present the complete agent design as a summary:

```
Agent Summary:
  Name:           {name}
  Command:        {command}
  Model:          {model}
  Tools:          {tools}
  Purpose:        {purpose}
  Input data:     {data sources}
  Output:         {output format} → {output path}
  Next steps:     {downstream suggestions}
```

Ask: "Does this look correct?"
- Options: "Yes, generate the agent file" / "No, let me change something"
- If "No" → ask which part to change, update, re-display

#### Step 11: Generate

1. Read `reference/agent-template.md`
2. Fill the template with all gathered details
3. Expand the analysis process into proper phases with clear instructions
4. Write to `clients/{client}/.claude/agents/{name}.md` (or `.claude/agents/{name}.md` for hub-level)
5. Display the generated file to the user
6. Ask: "Want to review and adjust anything in the generated file?"

---

### E02: Build a Skill

**Read `reference/skill-template.md` and `reference/design-guide.md` before starting.**

Walk through these questions one at a time via AskUserQuestion.

#### Step 1: Purpose

Ask: "What should this skill create or do?"
- Options: generate 3-4 example purposes, plus "Other (describe it)"
- Examples: "Generate importable CSV files" / "Build HTML pages" / "Pull and format data from an API" / "Run an interactive interview/questionnaire" / "Other"

Follow up: "Describe the specific deliverable or action in 1-2 sentences."

#### Step 2: Name

Based on the purpose, suggest 3 name options.

Ask: "What should the skill be called?"
- Options: your 3 suggestions plus "Other"
- Naming convention: `{noun}-{maker|builder|gatherer|analyzer|optimizer|auditor}`
- Examples: `rsa-maker`, `landing-page-builder`, `search-term-analyzer`

Validate: kebab-case, descriptive, ends with role suffix.

#### Step 3: Commands and actions

Ask: "How many distinct actions should this skill have?"
- Options: "1 — single action" / "2-3 actions" / "4-6 actions" / "More than 6 (consider splitting into multiple skills)"

For each action:
- Ask: "What does action {N} do? Give it a short name."
  - Example: "create", "analyze", "export", "diagnose"
- Ask: "Describe what this action does in 1 sentence."

Compose the command format: `/skill-name action1|action2|action3`

#### Step 4: Auto-activate triggers

Ask: "What natural language phrases should trigger this skill? List 4-8 trigger phrases."
- Generate suggestions based on the purpose
- Options: your suggestions plus "Other (add more)"
- Convention: short verb phrases a user would naturally say

#### Step 5: Input data

Ask: "What data does this skill need to read?"
- Options (multiSelect): "Business context (business.md)" / "Brand context (brand.md)" / "Google Ads CSV data" / "Offer angles (offer-angles.md)" / "Competitor data" / "Output from another skill/agent" / "User input only (no files)" / "Other"

For each selected source:
- Ask: "Is this required or optional?"
- Ask: "What specific file path?"

#### Step 6: User interaction

Ask: "Does this skill need to ask the user questions during execution?"
- Options: "Yes — interactive questionnaire" / "Yes — a few confirmation questions" / "No — fully automated from input files"

If interactive:
- Ask: "What kind of information do you need from the user?"
- Guide through designing the question flow

#### Step 7: Output format

Ask: "What does this skill produce?"
- Options (multiSelect): "CSV file (for Google Ads import)" / "Markdown report" / "HTML page" / "JSON data file" / "Updates to an existing context file" / "Display to user only" / "Other"

For each output:
- Ask: "Where should this be written?"
  - Suggest: `created/` for importable files, `context/analysis/` for reports, `context/` for context files

#### Step 8: Reference files

Ask: "Does this skill need reference files for complex logic?"
- Options: "Yes — has detailed sub-processes that should be in separate files" / "No — everything fits in the main SKILL.md"

If yes:
- Ask: "How many reference files? Describe each one briefly."
- Each reference file will be created as `references/{name}.md`

#### Step 9: Integration

Ask: "Which existing skills or agents connect to this one?"
- Options (multiSelect): list relevant existing skills, plus "None" and "Other"

Ask: "What should the user run after this skill completes?"
- Options: list relevant existing skills, plus "Nothing specific" and "Other"

#### Step 10: Review & confirm

Present the complete skill design:

```
Skill Summary:
  Name:            {name}
  Actions:         {action list}
  Triggers:        {auto-activate phrases}
  Input data:      {data sources with required/optional}
  User interaction: {yes/no + description}
  Output:          {deliverables + paths}
  Reference files: {count + descriptions}
  Integrations:    {upstream + downstream}
```

Ask: "Does this look correct?"
- Options: "Yes, generate the skill files" / "No, let me change something"

#### Step 11: Generate

1. Read `reference/skill-template.md`
2. Fill the template with all gathered details
3. Expand each action into a proper phase (E01, E02, etc.) with detailed steps
4. Create the skill directory: `clients/{client}/.claude/skills/{name}/`
5. Write `SKILL.md` with the full skill definition
6. If reference files were specified:
   - Create `references/` subdirectory
   - Write skeleton reference files with structure and TODOs for the user to fill in
7. Display the generated SKILL.md to the user
8. Ask: "Want to review and adjust anything?"

---

### E03: Browse Examples

Show annotated examples of existing agents and skills to help the user understand the patterns.

1. **List available examples:**
   - Read 2-3 agent files from the current client (or any client)
   - Read 2-3 skill SKILL.md files from the current client

2. **Present with annotations:**
   For each example, highlight:
   - The frontmatter structure and why each field matters
   - How the process phases are organized
   - What makes this agent/skill effective
   - Patterns to reuse

3. **Ask:** "Ready to build your own? Start with `/skill-maker agent` or `/skill-maker skill`"

---

## After Any Action

1. Display the path to the created file(s)
2. Suggest: "Test your new {agent/skill} by running `/{command}` from `clients/{client}/`"
3. If an agent was created: "You may want to create a skill that uses this agent's output as input"
4. If a skill was created with reference files: "Fill in the TODO sections in the reference files to complete the skill"

## Error Handling

| Error | Message |
|-------|---------|
| Hub root not found | "Could not find hub root (no main-config.json). Run this from your ppcos hub directory." |
| No clients found | "No client folders found. Run `/add-client` first." |
| Agent name already exists | "Agent `{name}` already exists in this client. Choose a different name or edit the existing one." |
| Skill name already exists | "Skill `{name}` already exists in this client. Choose a different name or edit the existing one." |
| Invalid name format | "Name must be kebab-case: lowercase letters, numbers, and hyphens only. Must start with a letter." |

## Integration Points

### Reads From
- `reference/agent-template.md` — agent file template
- `reference/skill-template.md` — skill file template
- `reference/design-guide.md` — conventions and design principles
- Existing agents/skills in target client — for naming and style reference

### Produces
- `clients/{client}/.claude/agents/{name}.md` — new agent file
- `clients/{client}/.claude/skills/{name}/SKILL.md` — new skill file
- `clients/{client}/.claude/skills/{name}/references/*.md` — skill reference files (if needed)

### Downstream
- The newly created agent or skill is immediately usable via its slash command
