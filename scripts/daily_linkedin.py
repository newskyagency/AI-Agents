"""
Daily LinkedIn News & Post Generator for New Sky.

Fetches e-commerce news, selects top 5 articles, generates a LinkedIn post
draft using Claude, and emails the digest to info@newsky.nl.
"""

import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import anthropic
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

NEWS_SOURCES = {
    "Dutch": [
        ("Emerce", "https://www.emerce.nl"),
        ("E-commerce News NL", "https://www.ecommercenews.nl"),
        ("RetailTrends", "https://retailtrends.nl"),
        ("Thuiswinkel.org", "https://www.thuiswinkel.org"),
    ],
    "International": [
        ("PPC News Feed", "https://ppcnewsfeed.com/"),
        ("PPC Hero", "https://ppchero.com/"),
        ("Search Engine Journal", "https://www.searchenginejournal.com/category/digital/ecommerce/"),
        ("Jon Loomer", "https://www.jonloomer.com/"),
    ],
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; NewSkyBot/1.0; +https://newsky.nl)"
}

MODEL = "claude-sonnet-4-6"


# ---------------------------------------------------------------------------
# Step 1 — Fetch news
# ---------------------------------------------------------------------------


def fetch_page(url: str) -> str:
    """Fetch a URL and return cleaned text content."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove scripts, styles, navs
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)[:8000]
    except Exception as e:
        print(f"  Warning: could not fetch {url}: {e}")
        return ""


def fetch_all_sources() -> str:
    """Fetch all news sources and return combined content."""
    parts = []
    for category, sources in NEWS_SOURCES.items():
        parts.append(f"\n## {category} sources\n")
        for name, url in sources:
            print(f"Fetching {name} ({url})...")
            content = fetch_page(url)
            if content:
                parts.append(f"### {name} — {url}\n{content}\n")
            else:
                parts.append(f"### {name} — {url}\n(Could not fetch)\n")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Step 2 & 3 — Claude: select top 5 + generate post
# ---------------------------------------------------------------------------


def load_agent_definition() -> str:
    """Load the linkedin-post.md agent definition."""
    path = Path(__file__).resolve().parent.parent / "linkedin" / "linkedin-post.md"
    return path.read_text(encoding="utf-8")


def generate_with_claude(news_content: str, agent_def: str) -> str:
    """Call Claude to select top 5 news + generate LinkedIn post."""
    client = anthropic.Anthropic()
    today = datetime.now().strftime("%A %d %B %Y")

    prompt = f"""Je bent de dagelijkse nieuwsassistent en LinkedIn-contentgenerator van New Sky.
Vandaag is {today}.

## Jouw agent-definitie (LinkedIn post regels)

{agent_def}

## Vandaag opgehaald nieuws van alle bronnen

{news_content}

## Opdracht

### Stap 1 — Top 5 nieuwsoverzicht
Selecteer de 5 meest relevante artikelen voor Nederlandse webshop-eigenaren met €2M-€10M omzet.
Per artikel:
- **Titel** (originele titel of korte samenvatting)
- **Bron** (naam website)
- **Link** (directe URL als die te vinden is, anders de homepage van de bron)
- **Korte omschrijving** (2-3 zinnen: wat staat erin en waarom relevant voor de ICP)

### Stap 2 — LinkedIn post
Kies het meest relevante artikel uit de top 5 en genereer een LinkedIn post.
- Kies het best passende posttype (ACTUALITEIT, BENCHMARK, CASE STUDY, FOUNDER STORY, DIAGNOSE, MYTHE ONTKRACHTEN, of PERSPECTIEF)
- Kies het thema uit de 7 thema's dat het beste aansluit
- Varieer: gebruik NIET hetzelfde posttype of thema als gisteren
- Volg ALLE regels uit de agent-definitie: structuur, haakregels, stijlregels
- Geen hashtags, geen emoji, geen CTA naar New Sky
- Nederlands, 260-400 woorden
- Controleer tegen de checklist

### Output formaat

Geef je antwoord in EXACT dit formaat:

===TOP5===
(je top 5 nieuwsoverzicht hier, in HTML)
===END_TOP5===

===POST_TYPE===
(het gekozen posttype, bijv. ACTUALITEIT)
===END_POST_TYPE===

===POST_THEME===
(het gekozen thema, bijv. Margestructuur)
===END_POST_THEME===

===POST_SOURCE===
(titel + bron van het artikel waarop de post gebaseerd is)
===END_POST_SOURCE===

===POST===
(de volledige LinkedIn post, klaar om te kopiëren)
===END_POST===
"""

    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def parse_response(response: str) -> dict:
    """Parse the structured Claude response into sections."""
    sections = {}
    for key in ["TOP5", "POST_TYPE", "POST_THEME", "POST_SOURCE", "POST"]:
        start = f"==={key}==="
        end = f"===END_{key}==="
        if start in response and end in response:
            content = response.split(start)[1].split(end)[0].strip()
            sections[key] = content
        else:
            sections[key] = "(niet gevonden)"
    return sections


# ---------------------------------------------------------------------------
# Step 4 — Send email
# ---------------------------------------------------------------------------


def build_email_html(sections: dict) -> str:
    """Build the HTML email body."""
    today = datetime.now().strftime("%d %B %Y")
    return f"""\
<html>
<body style="font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto; color: #333;">

<h2>Top 5 e-commerce nieuws — {today}</h2>

{sections["TOP5"]}

<hr style="margin: 30px 0;">

<h2>LinkedIn Post Draft</h2>
<p>
  <strong>Type:</strong> {sections["POST_TYPE"]}<br>
  <strong>Thema:</strong> {sections["POST_THEME"]}<br>
  <strong>Gebaseerd op:</strong> {sections["POST_SOURCE"]}
</p>

<pre style="background: #f5f5f5; padding: 20px; border-radius: 8px; white-space: pre-wrap; font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6;">{sections["POST"]}</pre>

<hr style="margin: 30px 0;">
<p style="color: #999; font-size: 12px;">
  Automatisch gegenereerd door de New Sky LinkedIn-agent via GitHub Actions.<br>
  Kopieer de post naar LinkedIn of pas aan waar nodig.
</p>

</body>
</html>"""


def send_email(html_body: str):
    """Send the digest email via Gmail SMTP."""
    gmail_address = os.environ["GMAIL_ADDRESS"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    email_to = os.environ.get("EMAIL_TO", "info@newsky.nl")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Ochtendupdate e-commerce + LinkedIn draft — {datetime.now().strftime('%d %b %Y')}"
    msg["From"] = gmail_address
    msg["To"] = email_to
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, gmail_password)
        server.sendmail(gmail_address, email_to, msg.as_string())

    print(f"Email sent to {email_to}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("New Sky — Daily LinkedIn News & Post Generator")
    print("=" * 60)

    # Step 1: Fetch news
    print("\n[1/4] Fetching news sources...")
    news_content = fetch_all_sources()

    # Step 2: Load agent definition
    print("\n[2/4] Loading agent definition...")
    agent_def = load_agent_definition()

    # Step 3: Generate with Claude
    print("\n[3/4] Generating top 5 + LinkedIn post with Claude...")
    response = generate_with_claude(news_content, agent_def)
    sections = parse_response(response)

    print(f"\n  Post type: {sections['POST_TYPE']}")
    print(f"  Theme: {sections['POST_THEME']}")
    print(f"  Source: {sections['POST_SOURCE']}")

    # Step 4: Send email
    print("\n[4/4] Sending email...")
    html_body = build_email_html(sections)
    send_email(html_body)

    print("\nDone!")


if __name__ == "__main__":
    main()
