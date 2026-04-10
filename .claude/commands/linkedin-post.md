---
description: Genereer een LinkedIn post voor New Sky — stelt vragen over thema en invalshoek, zoekt actueel nieuws, en schrijft de post in New Sky-stijl.
argument-hint: [thema] [invalshoek]
allowed-tools: [WebFetch, WebSearch, Read, AskUserQuestion]
---

# LinkedIn Post Genereren

Lees eerst `linkedin-post.md` volledig — dat bevat de ICP, posttypes, brand voice, format en voorbeelden.

Volg daarna dit stappenplan:

## Stap 1 — Thema kiezen

Vraag de gebruiker welk thema de post moet raken. Presenteer de 7 thema's als genummerde lijst:

1. **Margestructuur & producteconomie** — break-even ROAS, retouren, kortingsbeleid, AOV
2. **Attributie & datakwaliteit** — last-click, Performance Max, platform vs. backend-data
3. **Kanaalmix & kanaalafhankelijkheid** — e-mailkanaal, CRO, Google vs. Meta, organisch
4. **Schaalstrategie & groeibeslissingen** — volumegroei vs. winstgroei, CAC, opschalingstiming
5. **Bureau-relatie & inkoop van advertentiediensten** — KPIs, audits, incentivestructuren
6. **Klantprofiel & segmentatie** — cohortanalyse, lookalike audiences, eerste aankoopproduct
7. **Businessmodel & strategische positie** — CAC/LTV-ratio, retentie, exitwaarde

Vraag: "Welk thema wil je voor deze post? (1–7, of omschrijf vrij)"

## Stap 2 — Invalshoek kiezen

Toon op basis van het gekozen thema de bijbehorende invalshoeken uit `linkedin-post.md` als keuzelijst.

Vraag: "Welke invalshoek spreekt je aan? Of heb je een eigen idee?"

## Stap 3 — Posttype bepalen

Stel op basis van de gekozen thema/invalshoek-combinatie een passend posttype voor (zie de aanbevolen combinaties in `linkedin-post.md`). Vraag de gebruiker of ze dit type willen of iets anders:

- ACTUALITEIT — bron als anker
- BENCHMARK — statistiek als spiegel
- CASE STUDY — cijfers als bewijs
- FOUNDER STORY — eerlijkheid als autoriteit
- DIAGNOSE — herkenning als haak
- MYTHE ONTKRACHTEN — data als fundament
- PERSPECTIEF — een stellingname

## Stap 4 — Actueel nieuws zoeken

Zoek altijd een recent, relevant artikel — ook als het posttype geen ACTUALITEIT is. Het artikel geeft concrete context en maakt de post tijdelijk relevant.

Zoek in deze volgorde:
1. Gebruik WebFetch op: `https://emerce.nl`, `https://ecommercenews.nl`, `https://retailtrends.nl`, `https://www.thuiswinkel.org`
2. Of gebruik WebSearch met een gerichte query op het gekozen thema/invalshoek + "e-commerce Nederland 2025"

Kies het meest relevante artikel. Noteer: bron, titel, kernboodschap, datum.

## Stap 5 — Post schrijven

Schrijf de post volledig in het Nederlands, strikt volgens het format in `linkedin-post.md`:

```
[POSTTYPE] — [subtitel]

[HAAK — 1 zin die spanning, herkenning of nieuwsgierigheid creëert]

[Situatieschets — spiegel de interne monoloog van de ICP, 2-3 zinnen]

[Wat wij zien / hoe wij diagnosticeren — toon het denkproces, 2-4 zinnen]

[De concrete consequentie — wat er mis gaat als dit patroon doorgaat, 2-3 zinnen]

[Slotparagraaf — de diagnostische vraag aan de lezer]
```

**Verplichte checks voor publicatie:**
- [ ] Geen hashtags, geen emoji, geen CTA naar New Sky
- [ ] Eindigt met een directe diagnostische vraag aan de lezer
- [ ] Bevat specifieke getallen — geen vage kwalificaties
- [ ] Branchetermen (ROAS, LTV, CAC) worden inline uitgelegd bij eerste gebruik
- [ ] Zinnen zijn kort en puntig — bijzinnen splitsen in twee zinnen waar mogelijk
- [ ] De haak is scroll-stoppend: spanning, herkenning of een verrassende stelling
- [ ] De ICP herkent zichzelf in de situatieschets
