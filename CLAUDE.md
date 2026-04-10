# CLAUDE.md — New Sky AI Agents

## Overview

This repository contains AI agent definitions and automation for New Sky, a Dutch paid advertising agency targeting e-commerce webshops (€2M–€10M revenue) in the Netherlands and Belgium.

## Repository structure

```
linkedin/                  Agent definition + project docs
  linkedin-post.md         Full agent definition (ICP, post types, voice, format, examples)
  CLAUDE.md                Project-level instructions
scripts/                   Automation scripts
  daily_linkedin.py        Daily news digest + LinkedIn post generator
.github/workflows/         GitHub Actions
  daily-linkedin.yml       Weekday cron job (05:00 UTC)
.claude/                   Claude Code interactive config
  commands/linkedin-post.md  Slash command for manual post generation
  settings.local.json        Tool permissions
```

## LinkedIn Agent

### Automated daily workflow (GitHub Actions)

Runs every weekday at 05:00 UTC (07:00 CEST / 06:00 CET) via GitHub Actions:

1. Fetches news from 8 sources (4 Dutch, 4 international)
2. Selects the top 5 most relevant articles
3. Generates a LinkedIn post draft using Claude API
4. Emails the digest + draft to luuk@newsky.nl via Gmail SMTP

**GitHub Actions secrets required:**
- `ANTHROPIC_API_KEY` — Claude API key
- `GMAIL_ADDRESS` — sender Gmail address
- `GMAIL_APP_PASSWORD` — Gmail App Password
- `EMAIL_TO` — recipient address

### Manual post generation (Claude Code)

Use the `/linkedin-post` slash command or follow the steps in `linkedin/CLAUDE.md`.

### Post rotation

Two-axis rotation — vary BOTH the post type AND the topic theme:
1. **Post type:** ACTUALITEIT, BENCHMARK, CASE STUDY, FOUNDER STORY, DIAGNOSE, MYTHE ONTKRACHTEN, PERSPECTIEF
2. **Theme:** Margestructuur, Attributie & data, Kanaalmix, Schaalstrategie, Bureau-relatie, Klantprofiel, Businessmodel

Do not default to LTV/returning customers — all themes are equally important.
