from pathlib import Path
from html import escape as E
import json, shutil
from content import SERVICES, GENERAL_FAQS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
BASE = 'https://bartsch-dachbeschichtung.de'

ROUTES = {
    '/services/': '/leistungen/',
    '/our-approach/': '/ablauf/',
    '/about/': '/ueber-uns/',
    '/contact/': '/kontakt/',
    '/privacy/': '/datenschutz/',
    '/terms/': '/nutzungshinweise/'
}
for s in SERVICES:
    ROUTES['/services/' + s['old_slug'] + '/'] = '/leistungen/' + s['slug'] + '/'

for old in ROUTES:
    p = OUT / old.strip('/')
    if p.exists():
        shutil.rmtree(p)

def photo(key, alt, cls='', eager=False):
    return f'<img class="{cls}" src="/assets/{key}-1200.webp" srcset="/assets/{key}-480.webp 480w, /assets/{key}-768.webp 768w, /assets/{key}-1200.webp 1200w, /assets/{key}-1600.webp 1600w" sizes="(max-width: 700px) 100vw, 55vw" width="1536" height="1024" alt="{E(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async" '+('fetchpriority="high"' if eager else '')+'>'

def btn(text='Anfrage vorbereiten', url='/kontakt/', secondary=False):
    return f'<a class="button {"secondary" if secondary else ""}" href="{url}">{text}<span aria-hidden="true">↗</span></a>'

def faq(items):
    return '<div class="faqs">' + ''.join(f'<details><summary>{E(q)}<span aria-hidden="true">+</span></summary><p>{E(a)}</p></details>' for q, a in items) + '</div>'

def bullets(items):
    return '<ul class="checklist">' + ''.join(f'<li>{E(x)}</li>' for x in items) + '</ul>'

def steps(items):
    return '<div class="steps">' + ''.join(f'<article class="reveal"><span class="number">0{i+1}</span><h3>{E(t)}</h3><p>{E(d)}</p></article>' for i, (t, d) in enumerate(items)) + '</div>'

PROCESS = [
    ('Bedarf beschreiben.', 'Wählen Sie Ihre gewünschte Dach- oder Fassadenleistung und nennen Sie Standort in Hamburg, Dachfläche und Wunschtermin.'),
    ('Kostenlose Beratung & Besichtigung.', 'Wir prüfen das Dach oder die Fassade vor Ort in Hamburg & Norddeutschland und erstellen ein unverbindliches Angebot.'),
    ('Fachgerechte Umsetzung.', 'Pünktliche, saubere und professionelle Beschichtung / Säuberung durch das Team von Bartsch & Loßner GmbH.'),
    ('Gemeinsame Abnahme.', 'Prüfen Sie das fertig beschichtete Dach oder die Fassade direkt mit uns vor Ort.')
]

def service_links():
    return ''.join(f'<a href="/leistungen/{s["slug"]}/">{s["name"]}</a>' for s in SERVICES)

PAGES = []

def page(path, title, description, body):
    canonical = BASE + path
    schema = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'RoofingContractor',
                '@id': BASE + '/#organization',
                'name': 'Bartsch & Loßner GmbH Dachbeschichtung',
                'url': BASE + '/',
                'telephone': '+49 40 64413366',
                'address': {
                    '@type': 'PostalAddress',
                    'streetAddress': 'Pestalozzistraße 25',
                    'postalCode': '22305',
                    'addressLocality': 'Hamburg-Nord',
                    'addressCountry': 'DE'
                },
                'aggregateRating': {
                    '@type': 'AggregateRating',
                    'ratingValue': '4.8',
                    'reviewCount': '71'
                }
            },
            {
                '@type': 'WebSite',
                '@id': BASE + '/#website',
                'name': 'Bartsch & Loßner GmbH',
                'url': BASE + '/',
                'inLanguage': 'de-DE'
            },
            {
                '@type': 'WebPage',
                '@id': canonical + '#webpage',
                'name': title,
                'description': description,
                'url': canonical,
                'inLanguage': 'de-DE',
                'isPartOf': {'@id': BASE + '/#website'}
            }
        ]
    }
    if path not in ['/', '/404.html']:
        crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Startseite', 'item': BASE + '/'}]
        if path.startswith('/leistungen/') and path != '/leistungen/':
            crumbs.append({'@type': 'ListItem', 'position': 2, 'name': 'Leistungen', 'item': BASE + '/leistungen/'})
        crumbs.append({'@type': 'ListItem', 'position': len(crumbs) + 1, 'name': title, 'item': canonical})
        schema['@graph'].append({'@type': 'BreadcrumbList', 'itemListElement': crumbs})
    
    nav = '<a href="/leistungen/">Dach & Fassade</a><a href="/ablauf/">Ablauf</a><a href="/ueber-uns/">Über uns</a><a href="/kontakt/">Kontakt</a>'
    html = f'''<!doctype html><html lang="de-DE"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | Bartsch &amp; Loßner GmbH Hamburg</title><meta name="description" content="{E(description)}"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:locale" content="de_DE"><meta property="og:site_name" content="Bartsch &amp; Loßner GmbH"><meta property="og:title" content="{E(title)} | Bartsch &amp; Loßner GmbH"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{E(title)} | Bartsch &amp; Loßner GmbH"><meta name="twitter:description" content="{E(description)}"><meta name="theme-color" content="#4c974c"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css"><script src="/assets/site.js" defer></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body><a class="skip" href="#main">Zum Inhalt springen</a><header class="header"><a class="logo" href="/" aria-label="Bartsch &amp; Loßner GmbH – Startseite"><i></i>Bartsch &amp; Loßner</a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menü <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Hauptnavigation">{nav}<a class="button secondary" href="tel:+494064413366">📞 +49 40 64413366</a></nav></header><main id="main">{body}</main><section class="final-cta"><div><p class="eyebrow">BARTSCH &amp; LOßNER GMBH · HAMBURG-NORD</p><h2>Ihr Fachbetrieb aus Hamburg<br>für den Norden.</h2><p style="margin-top:0.5rem;color:rgba(255,255,255,0.9);">Pestalozzistraße 25, 22305 Hamburg-Nord · Tel: +49 40 64413366</p></div>{btn('Projekt anfragen','/kontakt/')}</section><footer><div class="footer-top"><div><a class="logo" href="/"><i></i>Bartsch &amp; Loßner GmbH</a><p>Dachbeschichtung &amp; Fassadensanierung.<br>⭐ 4.8 (71 Google-Bewertungen)</p><p style="font-size:0.9rem;margin-top:0.5rem;">📍 Pestalozzistraße 25, 22305 Hamburg-Nord<br>📞 +49 40 64413366<br>⏰ Mo - Fr: 08:00 - 18:00 Uhr</p></div><div><h3>Unsere Leistungen</h3>{service_links()}</div><div><h3>Navigation</h3><a href="/ablauf/">Unser Ablauf</a><a href="/ueber-uns/">Über Bartsch &amp; Loßner</a><a href="/faq/">Häufige Fragen</a><a href="/kontakt/">Kontakt &amp; Anfahrt</a></div><div class="footer-note"><span class="eyebrow">KOMPETENT · SCHNELL · ZUVERLÄSSIG</span><p>Qualitäts-Dachbeschichtung &amp; Fassadenschutz in Hamburg und ganz Norddeutschland.</p></div></div><div class="footer-bottom"><span>© 2026 Bartsch &amp; Loßner GmbH · Pestalozzistraße 25, 22305 Hamburg-Nord</span><div><a href="/impressum/">Impressum</a><a href="/datenschutz/">Datenschutz</a><a href="/nutzungshinweise/">Nutzungshinweise</a><a href="#main">Nach oben ↑</a></div></div></footer></body></html>'''
    target = OUT / '404.html' if path == '/404.html' else OUT / path.strip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html)
    if path != '/404.html':
        PAGES.append(path)

def intro(label, title, text):
    return f'<section class="page-intro wrap"><div class="breadcrumb"><a href="/">Startseite</a><span>/</span>{E(label)}</div><p class="eyebrow">{E(label)}</p><h1>{title}</h1><p class="lead">{E(text)}</p></section>'

strip = '<div class="service-strip wrap">' + ''.join(f'<a href="/leistungen/{s["slug"]}/"><span>0{i+1}</span><strong>{s["name"]}</strong><b aria-hidden="true">↗</b></a>' for i, s in enumerate(SERVICES)) + '</div>'

rows = ''
for i, s in enumerate(SERVICES):
    art = photo(s['image'], s['alt']) if i < 3 else '<div class="clear-art"><span>BARTSCH<br>&amp; LOßNER<br><em>GMBH.</em></span><p>Kompetent. Schnell. Zuverlässig.</p></div>'
    rows += f'<article class="service-row reveal"><div class="service-visual">{art}<span class="image-label">0{i+1} / {s["category"]}</span></div><div class="service-copy"><p class="eyebrow">0{i+1} — {s["name"]}</p><h3>{s["short"].replace(chr(10),"<br>")}</h3><p>{s["intro"]}</p><a class="text-link" href="/leistungen/{s["slug"]}/">Leistung entdecken <span aria-hidden="true">↗</span></a></div></article>'

hero = f'''<section class="hero wrap"><div class="hero-copy"><p class="eyebrow">BARTSCH &amp; LOßNER GMBH · HAMBURG-NORD</p><h1><span>Ihr Fachbetrieb aus</span><span>Hamburg für</span><span class="blue"> den Norden.</span></h1><p>Dachbeschichtung, Versiegelung, Dachreinigung, Fassadenanstrich &amp; Reparaturen.<br><strong>kompetent – schnell – zuverlässig</strong><br>⭐ <strong>4.8 Sterne (71 Google Bewertungen)</strong> · Pestalozzistraße 25, 22305 Hamburg-Nord</p><div class="actions">{btn('Leistungen entdecken','/leistungen/')}<a class="button secondary" href="tel:+494064413366">Anrufen: +49 40 64413366</a></div><div class="hero-foot"><span class="blue" aria-hidden="true">✳</span> Geöffnet Mo - Fr 08:00 - 18:00 Uhr · Kostenlose Beratung vor Ort.</div></div><div class="hero-visual"><div class="hero-main">{photo('moving','Handwerker bei der Dachbeschichtung in Hamburg',eager=True)}<span class="photo-caption">BARTSCH &amp; LOßNER GMBH — HAMBURG</span></div><div class="hero-small">{photo('cleaning','Dachreinigung und Entmoosung')}<span>QUALITÄTS-DACHBESCHICHTUNG</span></div></div></section>'''

page('/', 'Dachbeschichtung & Dachreinigung Hamburg', 'Bartsch & Loßner GmbH: Professionelle Dachbeschichtung, Dachreinigung, Entmoosung und Fassadenbeschichtung in Hamburg-Nord. ⭐ 4.8 bei 71 Google-Bewertungen.', hero + strip + f'<section class="wrap section"><div class="section-heading"><p class="eyebrow">LEISTUNGEN FÜR DACH &amp; FASSADE</p><h2>Ihr Haus in neuem Glanz.<br><span class="muted">Dauerhaft geschützt.</span></h2><p>Ob Dachbeschichtung, Entmoosung oder Fassadenschutz:<br>Bartsch &amp; Loßner GmbH ist Ihr Fachbetrieb für Hamburg &amp; den Norden.</p></div>{rows}</section><section class="dark section"><div class="wrap"><p class="eyebrow">VOM BESICHTIGUNGSTERMIN BIS ZUM FERTIGEN DACH</p><h2>So einfach verläuft Ihre Dachbeschichtung.</h2>{steps(PROCESS)}<a class="text-link" href="/ablauf/">Unseren Ablauf kennenlernen ↗</a></div></section><section class="wrap section question-grid"><div><p class="eyebrow">HÄUFIGE FRAGEN</p><h2>Fragen an<br>Bartsch &amp; Loßner?</h2><a class="text-link" href="/faq/">Alle häufigen Fragen ↗</a></div>{faq(GENERAL_FAQS[:4])}</section>')

page('/leistungen/', 'Dachbeschichtung & Fassadenarbeiten Hamburg', 'Übersicht unserer Leistungen: Dachbeschichtung, Versiegelung, Dachreinigung, Entmoosung, Fassadenbeschichtung und Dachinspektion.', intro('Unsere Leistungen', 'Qualitätsarbeit.<br><span class="blue">Für Dach &amp; Fassade.</span>', 'Entdecken Sie unsere bewährten Leistungen rund um Dachbeschichtung und Gebäudeschutz in Hamburg und ganz Norddeutschland.') + strip + f'<section class="wrap section">{rows}</section>')

for s in SERVICES:
    path = '/leistungen/' + s['slug'] + '/'
    visual = photo(s['image'], s['alt'], eager=True) if s['category'] != 'SANIERUNG' else '<div class="clear-art"><span>BARTSCH<br>&amp; LOßNER<br><em>GMBH.</em></span><p>Werterhalt für Ihre Immobilie.</p></div>'
    body = intro(s['name'], s['short'].replace('\n', '<br>'), s['intro']) + f'<section class="wrap detail-hero"><div class="detail-photo">{visual}</div><aside class="blue-panel"><p class="eyebrow">PASSEND FÜR</p>{bullets(s["for"])}<p>{s["aside"]}</p>{btn("Anfrage vorbereiten", "/kontakt/?service=" + s["slug"], True)}</aside></section><section class="wrap section split"><div><p class="eyebrow">DARAUF KOMMT ES AN</p><h2>Klarer Umfang.<br>Nachhaltiger Schutz.</h2><p class="lead">{s["overview"]}</p></div><div><h3>Das gehört zum Leistungsumfang</h3>{bullets(s["included"])}<p class="note">{s["scope_note"]}</p></div></section><section class="soft section"><div class="wrap"><p class="eyebrow">SCHRITT FÜR SCHRITT</p><h2>So wird Ihr Dach wie neu.</h2>{steps(s["steps"])}</div></section><section class="wrap section split"><div><p class="eyebrow">GUT VORBEREITET</p><h2>Das hilft bei<br>Ihrer Anfrage.</h2><p>Mit diesen Angaben lässt sich das Projekt vorab gut einschätzen.</p>{bullets(s["prepare"])}</div><div class="border-panel"><p class="eyebrow">KOSTEN VERSTEHEN</p><h3>Was beeinflusst den Preis?</h3>{bullets(s["cost"])}<p>Wir erstellen Ihnen nach Besichtigung einen fairen und transparenten Festpreis.</p>{btn("Projekt beschreiben", "/kontakt/?service=" + s["slug"])}</div></section><section class="wrap section question-grid"><div><p class="eyebrow">HÄUFIGE FRAGEN</p><h2>Fragen zu dieser<br>Leistung.</h2></div>{faq(s["faqs"])}</section><section class="wrap related"><p class="eyebrow">WEITERE LEISTUNGEN VON BARTSCH &amp; LOßNER GMBH</p><div>{"".join(f"<a href='/leistungen/{x['slug']}/'>{x['name']} ↗</a>" for x in SERVICES if x != s)}</div></section>'
    page(path, s['name'], s['description'], body)

page('/ablauf/', 'Ablauf der Dachbeschichtung', 'So einfach verläuft Ihr Projekt mit Bartsch & Loßner GmbH: Von der kostenlosen Dachprüfung bis zur fertigen Beschichtung.', intro('Unser Ablauf', 'Kompetente Arbeit<br>mit <span class="blue">klarem System.</span>', 'Wie verläuft eine Dachbeschichtung oder Fassadenreinigung? Hier erfahren Sie Schritt für Schritt, wie wir arbeiten.') + f'<section class="wrap wide-image">{photo("moving", "Bartsch & Lossner GmbH bei der Arbeit", eager=True)}</section><section class="wrap section">{steps(PROCESS)}</section><section class="soft section"><div class="wrap split"><div><p class="eyebrow">UNSERE GARANTIE</p><h2>Worauf Sie sich<br>verlassen können.</h2></div><div>{bullets(["Erfahrungsstarker Fachbetrieb aus Hamburg", "Kompetent – schnell – zuverlässig", "Kostenlose Beratung & Probefläche direkt vor Ort", "Hervorragende Kundenbewertungen (4.8 Sterne)", "Langlebiger Schutz mit Qualitäts-Dachfarben"])}</div></div></section>')

page('/ueber-uns/', 'Über Bartsch & Loßner GmbH Hamburg', 'Ihr Fachbetrieb aus Hamburg für den Norden: Bartsch & Loßner GmbH steht für erstklassige Dachbeschichtungen, Fassadenschutz und hohe Kundenzufriedenheit (4.8 bei 71 Bewertungen).', intro('Über Bartsch & Loßner GmbH', 'Ihr Fachbetrieb<br>in <span class="blue">Hamburg-Nord.</span>', 'Pestalozzistraße 25, 22305 Hamburg-Nord · Telefon: +49 40 64413366 · ⭐ 4.8 (71 Google Bewertungen)') + f'<section class="wrap split section"><div class="statement">Ihr Fachbetrieb.<br>Aus Hamburg.<br><span class="blue">Für den Norden.</span></div><div><p class="eyebrow">ERFAHRUNG &amp; QUALITÄT</p><h2>Bartsch &amp; Loßner GmbH – Kompetent, schnell, zuverlässig.</h2><p>Bartsch &amp; Loßner GmbH Dachbeschichtung ist Ihr erfahrener Spezialist für Dachbeschichtungen, Dachreinigungen, Entmoosung und Fassadenarbeiten in Hamburg-Nord und der gesamten norddeutschen Region.</p><p>Mit Sitz in der Pestalozzistraße 25 (in hwcon GmbH) legen wir höchsten Wert auf sorgfältige Vorarbeiten, erstklassige Materialien und nachhaltige Ergebnisse. 71 zufriedene Kundenbewertungen mit 4.8 Sternen bestätigen unsere Qualität.</p><div style="margin-top:1.5rem;padding:1.2rem;background:#f0f4ff;border-radius:8px;border-left:4px solid #4c974c;"><p style="margin:0;font-weight:600;color:#3b7a3b;">📍 Kontaktdaten:</p><p style="margin:0.3rem 0 0 0;">Bartsch &amp; Loßner GmbH Dachbeschichtung<br>Pestalozzistraße 25, 22305 Hamburg-Nord (in hwcon GmbH)<br>Telefon: +49 40 64413366<br>Öffnungszeiten: Mo - Fr: 08:00 - 18:00 Uhr<br>Webseite: bartsch-dachbeschichtung.de</p></div></div></section>')

options = ''.join(f'<option value="{s["slug"]}">{s["name"]}</option>' for s in SERVICES)
form = f'''<section class="wrap quote-layout"><aside><p class="eyebrow">BARTSCH &amp; LOßNER GMBH · ANFRAGE</p><h2>Ihr Vorhaben.<br>Kostenlos anfragen.</h2><p>Beschreiben Sie Ihr Projekt. Wir melden uns umgehend bei Ihnen für eine kostenlose Beratung vor Ort.</p><div class="quote-note"><strong>Direkt anrufen?</strong><p>Sie erreichen uns zu unseren Bürozeiten unter:<br><strong style="font-size:1.1rem;color:#4c974c;">📞 +49 40 64413366</strong></p></div><a class="text-link" href="/faq/">Vorher noch eine Frage? ↗</a></aside><form id="quote-form"><div class="form-progress" aria-label="Schritte der Anfrage"><span class="active">01 Vorhaben</span><span>02 Kontaktdaten</span><span>03 Übersicht</span></div><div class="form-step" data-step="0"><h2>Was möchten Sie anfragen?</h2><label for="service">Gewünschte Leistung *</label><select name="service" id="service" required><option value="">Bitte auswählen</option>{options}</select><div class="form-grid"><div><label for="postal">Postleitzahl *</label><input id="postal" name="postal" required pattern="[0-9]{{5}}" inputmode="numeric" maxlength="5" autocomplete="postal-code" value="22305"></div><div><label for="city">Ort *</label><input id="city" name="city" required maxlength="100" autocomplete="address-level2" value="Hamburg"></div></div><label for="date">Wunschtermin (optional)</label><input id="date" name="date" type="date"><label for="details">Beschreiben Sie das Objekt oder Vorhaben *</label><textarea id="details" name="details" required minlength="15" maxlength="2500" rows="5" placeholder="Zum Beispiel: Dachbeschichtung für Einfamilienhaus in Hamburg, ca. 150m² Dachfläche, Betonsteine mit Moosbefall."></textarea><p class="field-help">Mindestens 15 Zeichen.</p><button class="button" type="button" data-next>Weiter <span aria-hidden="true">→</span></button></div><div class="form-step" data-step="1" hidden><h2>Ihre Kontaktdaten</h2><label for="name">Ihr Name *</label><input name="name" id="name" required maxlength="100" autocomplete="name"><label for="email">E-Mail-Adresse *</label><input name="email" id="email" type="email" required maxlength="200" autocomplete="email"><label for="phone">Telefonnummer *</label><input name="phone" id="phone" type="tel" required maxlength="30" autocomplete="tel" placeholder="+49 40 ..."><label class="checkbox"><input name="understand" type="checkbox" required> <span>Ich möchte eine kostenlose Anfrage an Bartsch &amp; Loßner GmbH stellen.</span></label><div class="actions"><button class="button secondary" type="button" data-back>← Zurück</button><button class="button" type="button" data-next>Angaben prüfen →</button></div></div><div class="form-step" data-step="2" hidden><h2>Alles auf einen Blick.</h2><dl id="quote-review"></dl><p>Prüfen Sie Ihre Angaben vor dem Absenden / Herunterladen.</p><div class="actions"><button class="button secondary" type="button" data-back>← Bearbeiten</button><button class="button" type="submit">Anfrage herunterladen ↓</button></div></div><p id="form-status" role="status" aria-live="polite"></p></form></section>'''

page('/kontakt/', 'Kontakt zu Bartsch & Loßner GmbH Hamburg', 'Dachbeschichtung in Hamburg-Nord anfragen: Pestalozzistraße 25, 22305 Hamburg. Tel: +49 40 64413366.', intro('Kontakt & Anfahrt', 'Bartsch &amp; Loßner GmbH.<br><span class="blue">Hier erreichen Sie uns.</span>', 'Pestalozzistraße 25, 22305 Hamburg-Nord (in hwcon GmbH) · Telefon: +49 40 64413366 · Mo - Fr: 08:00 - 18:00 Uhr.') + form)

page('/faq/', 'Häufige Fragen – Bartsch & Loßner GmbH', 'Antworten zu Dachbeschichtung, Preisen, Haltbarkeit, Probeflächen und Einsatzgebieten von Bartsch & Loßner GmbH in Hamburg.', intro('Häufige Fragen', 'Antworten rund um<br><span class="blue">Dach &amp; Fassade.</span>', 'Häufig gestellte Fragen zu unseren Beschichtungs- und Reinigungsarbeiten in Hamburg.') + '<section class="wrap narrow section">' + faq(GENERAL_FAQS) + '</section>')

page('/datenschutz/', 'Datenschutz – Bartsch & Loßner GmbH', 'Datenschutzhinweise von Bartsch & Loßner GmbH Dachbeschichtung, Pestalozzistraße 25, 22305 Hamburg-Nord.', intro('Datenschutz', 'Schutz Ihrer Daten.<br>Bartsch &amp; Loßner GmbH.', 'Datenschutzerklärung für Besucher der Webseite bartsch-dachbeschichtung.de') + '''<article class="wrap prose section"><h2>Verantwortlicher</h2><p>Bartsch &amp; Loßner GmbH Dachbeschichtung<br>Pestalozzistraße 25<br>22305 Hamburg-Nord, Deutschland<br>Telefon: +49 40 64413366<br>Webseite: bartsch-dachbeschichtung.de</p><h2>Erhebung personenbezogener Daten</h2><p>Wir verarbeiten personenbezogene Daten wie Name, E-Mail-Adresse und Telefonnummer ausschließlich zur Bearbeitung Ihrer Anfragen und Beschichtungsaufträge.</p></article>''')

page('/nutzungshinweise/', 'Nutzungshinweise – Bartsch & Loßner GmbH', 'Hinweise zum Angebot von Bartsch & Loßner GmbH in Hamburg.', intro('Nutzungshinweise', 'Bartsch &amp; Loßner GmbH.<br>Hamburg.', 'Hinweise zur Nutzung unserer Dienste.') + '''<article class="wrap prose section"><h2>Dienstleistungen</h2><p>Bartsch &amp; Loßner GmbH führt Dachbeschichtungen, Dachreinigungen, Entmoosung und Fassadenbeschichtungen in Hamburg und Norddeutschland fachgerecht aus.</p></article>''')

page('/impressum/', 'Impressum – Bartsch & Loßner GmbH Hamburg', 'Impressum und Anbieterkennzeichnung von Bartsch & Loßner GmbH in Hamburg.', intro('Impressum', 'Anbieterkennzeichnung.<br><span class="blue">Bartsch &amp; Loßner GmbH.</span>', 'Rechtliche Angaben gemäß § 5 DDG.') + '''<article class="wrap prose section"><h2>Anbieter &amp; Kontakt</h2><p><strong>Bartsch &amp; Loßner GmbH Dachbeschichtung</strong><br>Pestalozzistraße 25<br>22305 Hamburg-Nord, Deutschland<br><em>(Located in: hwcon GmbH)</em></p><p><strong>Telefon:</strong> +49 40 64413366<br><strong>Webseite:</strong> <a href="http://www.bartsch-dachbeschichtung.de/" target="_blank" rel="noopener">bartsch-dachbeschichtung.de</a><br><strong>Öffnungszeiten:</strong> Mo - Fr: 08:00 - 18:00 Uhr</p><p><strong>Unternehmensgegenstand:</strong> Dachbeschichtung, Dachreinigung, Entmoosung, Versiegelung &amp; Fassadenbeschichtung.</p></article>''')

page('/404.html', 'Seite nicht gefunden', 'Zurück zu Bartsch & Loßner GmbH.', intro('404 – Seite nicht gefunden', 'Zurück zur<br><span class="blue">Startseite.</span>', 'Diese Seite ist nicht verfügbar.') + '<div class="wrap actions section">' + btn('Leistungen ansehen', '/leistungen/') + btn('Zur Startseite', '/', True) + '</div>')

(OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + BASE + '/sitemap.xml\n')
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>' + BASE + p + '</loc></url>' for p in PAGES) + '</urlset>')

for old, new in ROUTES.items():
    target = OUT / old.strip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f'<!doctype html><html lang="de-DE"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Seite umgezogen | Bartsch &amp; Loßner GmbH</title><meta name="description" content="Diese Bartsch &amp; Loßner GmbH Seite ist unter einer neuen Adresse erreichbar."><meta name="robots" content="noindex,follow"><link rel="canonical" href="{BASE+new}"><meta http-equiv="refresh" content="0;url={new}"></head><body><h1>Diese Seite ist umgezogen.</h1><p><a href="{new}">Weiter zu Bartsch &amp; Loßner GmbH</a></p></body></html>')

print(f'Built {len(PAGES)+1} pages for Bartsch & Loßner GmbH')
