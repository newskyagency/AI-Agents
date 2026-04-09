# CLAUDE.md — New Sky AI Agents

## Overview

This repository contains agent definitions for New Sky's automated Claude Code agents. Each agent runs as a scheduled remote trigger in Anthropic's cloud — no local machine required.

New Sky is a Dutch paid advertising agency targeting e-commerce webshops (€2M–€10M revenue) in the Netherlands and Belgium.

## Repository structure

```
linkedin/           LinkedIn post generation + daily news digest agent
```

## Agents

### linkedin — Daily news digest + LinkedIn post draft

**Trigger:** `daily-linkedin-news`
**Schedule:** Every weekday at 05:00 UTC (07:00 CEST / 06:00 CET)
**Output:** Email to info@newsky.nl

What it does:
1. Fetches news from 8 sources (4 Dutch, 4 international) about e-commerce, PPC, and retail
2. Selects the top 5 most relevant articles with title, summary, and link
3. Generates a LinkedIn post draft based on the most relevant article
4. Emails the news digest + post draft to info@newsky.nl

Agent definition: `linkedin/linkedin-post.md`

Manage triggers at: https://claude.ai/code/scheduled
