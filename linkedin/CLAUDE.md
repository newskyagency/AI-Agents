# CLAUDE.md — LinkedIn Post Agent

## Project

LinkedIn post generation agent for New Sky — a Dutch paid advertising agency targeting e-commerce webshops (€2M–€10M revenue) in the Netherlands and Belgium.

The full agent definition (ICP, post types, brand voice, format template, examples) lives in `linkedin-post.md`.

## Automated daily workflow

A scheduled remote trigger (`daily-linkedin-news`) runs every weekday at 05:00 UTC (07:00 CEST / 06:00 CET):

1. Fetches news from all sources listed below
2. Selects the top 5 most relevant articles (title, source, link, short description)
3. Generates a LinkedIn post draft based on the most relevant article, choosing the best-fitting post type and theme
4. Emails the news digest + post draft to info@newsky.nl via Gmail

## News sources

### Dutch (e-commerce & retail)
- https://www.emerce.nl
- https://www.ecommercenews.nl
- https://retailtrends.nl
- https://www.thuiswinkel.org

### International (PPC & e-commerce)
- https://ppcnewsfeed.com/
- https://ppchero.com/
- https://www.searchenginejournal.com/category/digital/ecommerce/
- https://www.jonloomer.com/

## Manual post generation

1. Read `linkedin-post.md` first
2. **Choose (or suggest) the post type** — ACTUALITEIT, BENCHMARK, CASE STUDY, FOUNDER STORY, DIAGNOSE, MYTHE ONTKRACHTEN, or PERSPECTIEF
3. **For ACTUALITEIT** — fetch a recent article from one of the news sources
4. **Write the post** following the format and voice defined in `linkedin-post.md`
5. **Self-check** against the checklist at the bottom of `linkedin-post.md`

## Post rotation

Two-axis rotation — vary BOTH the post type AND the topic theme:

1. **Post type rotation** — cycle through all 7 types. Use the one least recently used.
2. **Topic theme rotation** — `linkedin-post.md` contains 7 topic themes. Avoid repeating the same theme as the previous 2–3 posts.

Themes: Margestructuur, Attributie & data, Kanaalmix, Schaalstrategie, Bureau-relatie, Klantprofiel, Businessmodel.

**Do not default to LTV/returning customers.** That is one angle within Thema 1 and Thema 6. The other themes are equally important.

## Key constraints

- Dutch only
- No hashtags, no emoji, no CTA to New Sky
- Every post ends with a direct diagnostic question to the reader
- Always use specific numbers — never vague qualifiers
- Explain industry terms (ROAS, LTV) inline on first use
