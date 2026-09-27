from pathlib import Path
from html import escape as E
import json, shutil
from content import SERVICES, GENERAL_FAQS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
BASE = 'https://dachdecker-pintilei.de'

# German canonical routes. Former English links retain German transition pages.
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
    ('Dachbedarf beschreiben.', 'Wählen Sie Ihre Dachleistung und nennen Sie Ort in Harburg/Hamburg, Ausmaß und Wunschtermin.'),
    ('Kostenfreie Ersterfassung.', 'Wir besprechen Leistungen, Materialien und Kosten vor Ort oder telefonisch unter +49 176 73501602.'),
    ('Termin & Durchführung.', 'Pünktliche und saubere Ausführung durch erfahrene Dachdecker von Dachservice Pintilei.'),
    ('Gemeinsame Abnahme.', 'Prüfen Sie das fertige Dach oder die Reparatur direkt mit uns vor Ort.')
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
                'name': 'Dachservice Pintilei',
                'url': BASE + '/',
                'telephone': '+49 176 73501602',
                'address': {
                    '@type': 'PostalAddress',
                    'streetAddress': 'Winsener Str. 19',
                    'postalCode': '21077',
                    'addressLocality': 'Harburg',
                    'addressCountry': 'DE'
                },
                'aggregateRating': {
                    '@type': 'AggregateRating',
                    'ratingValue': '5.0',
                    'reviewCount': '69'
                }
            },
            {
                '@type': 'WebSite',
                '@id': BASE + '/#website',
                'name': 'Dachservice Pintilei',
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
    
    nav = '<a href="/leistungen/">Leistungen</a><a href="/ablauf/">Ablauf</a><a href="/ueber-uns/">Über uns</a><a href="/kontakt/">Kontakt</a>'
    html = f'''<!doctype html><html lang="de-DE"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | Dachservice Pintilei Harburg</title><meta name="description" content="{E(description)}"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:locale" content="de_DE"><meta property="og:site_name" content="Dachservice Pintilei"><meta property="og:title" content="{E(title)} | Dachservice Pintilei"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{E(title)} | Dachservice Pintilei"><meta name="twitter:description" content="{E(description)}"><meta name="theme-color" content="#084bff"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css"><script src="/assets/site.js" defer></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body><a class="skip" href="#main">Zum Inhalt springen</a><header class="header"><a class="logo" href="/" aria-label="Dachservice Pintilei – Startseite"><i></i>Dachservice Pintilei</a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menü <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Hauptnavigation">{nav}<a class="button secondary" href="tel:+4917673501602">📞 +49 176 73501602</a></nav></header><main id="main">{body}</main><section class="final-cta"><div><p class="eyebrow">DACHSERVICE PINTILEI · HARBURG</p><h2>Ihr Dach in besten Händen.<br>Jetzt Anfragen.</h2><p style="margin-top:0.5rem;color:rgba(255,255,255,0.9);">Winsener Str. 19, 21077 Harburg · Tel: +49 176 73501602</p></div>{btn('Dach-Anfrage stellen','/kontakt/')}</section><footer><div class="footer-top"><div><a class="logo" href="/"><i></i>Dachservice Pintilei</a><p>Ihr zuverlässiger Dachdecker in Harburg.<br>⭐ 5.0 (69 Google Bewertungen)</p><p style="font-size:0.9rem;margin-top:0.5rem;">📍 Winsener Str. 19, 21077 Harburg<br>📞 +49 176 73501602<br>⏰ Mo - Fr ab 07:00 Uhr geöffnet</p></div><div><h3>Unsere Dach-Leistungen</h3>{service_links()}</div><div><h3>Navigation</h3><a href="/ablauf/">Unser Ablauf</a><a href="/ueber-uns/">Über Dachservice Pintilei</a><a href="/faq/">Häufige Fragen</a><a href="/kontakt/">Kontakt & Anfahrt</a></div><div class="footer-note"><span class="eyebrow">SANIERUNG · REPARATUR · WARTUNG</span><p>Qualitätsarbeit am Dach für Hausbesitzer und Gewerbe in Harburg & Hamburg.</p></div></div><div class="footer-bottom"><span>© 2026 Dachservice Pintilei · Winsener Str. 19, 21077 Harburg</span><div><a href="/impressum/">Impressum</a><a href="/datenschutz/">Datenschutz</a><a href="/nutzungshinweise/">Nutzungshinweise</a><a href="#main">Nach oben ↑</a></div></div></footer></body></html>'''
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
    art = photo(s['image'], s['alt']) if i < 3 else '<div class="clear-art"><span>DACH<br>SERVICE<br><em>PINTILEI.</em></span><p>Zuverlässig. Meisterhaft. Harburg.</p></div>'
    rows += f'<article class="service-row reveal"><div class="service-visual">{art}<span class="image-label">0{i+1} / {s["category"]}</span></div><div class="service-copy"><p class="eyebrow">0{i+1} — {s["name"]}</p><h3>{s["short"].replace(chr(10),"<br>")}</h3><p>{s["intro"]}</p><a class="text-link" href="/leistungen/{s["slug"]}/">Leistung entdecken <span aria-hidden="true">↗</span></a></div></article>'

hero = f'''<section class="hero wrap"><div class="hero-copy"><p class="eyebrow">DACHSERVICE PINTILEI · HARBURG (HAMBURG)</p><h1><span>Ihr Dachdecker</span><span>in Harburg &</span><span class="blue"> Umgebung.</span></h1><p>Dachsanierung, Eindeckung, Sturmschaden-Reparatur, Dachrinnenreinigung & Flachdachabdichtung.<br><strong>⭐ 5.0 Sterne (69 Google Bewertungen)</strong> · Winsener Str. 19, 21077 Harburg</p><div class="actions">{btn('Leistungen entdecken','/leistungen/')}<a class="button secondary" href="tel:+4917673501602">Anrufen: +49 176 73501602</a></div><div class="hero-foot"><span class="blue" aria-hidden="true">✳</span> Geöffnet Mo - Fr ab 07:00 Uhr · Schnelle Hilfe bei Sturmschäden.</div></div><div class="hero-visual"><div class="hero-main">{photo('moving','Handwerker bei Dacharbeiten an einem Gebäude in Harburg',eager=True)}<span class="photo-caption">DACHSERVICE PINTILEI — HARBURG</span></div><div class="hero-small">{photo('cleaning','Dachrinnen- und Dachwartung')}<span>FACHGERECHTE QUALITÄTSARBEIT</span></div></div></section>'''

page('/', 'Dachdecker & Dachservice in Harburg', 'Dachservice Pintilei: Professionelle Dachsanierung, Dachreparatur, Sturmschaden-Notdienst, Dachrinnenreinigung und Flachdachabdichtung in 21077 Harburg & Hamburg. 5.0 Sterne bei 69 Google-Bewertungen.', hero + strip + f'<section class="wrap section"><div class="section-heading"><p class="eyebrow">UNSERE LEISTUNGEN AM DACH</p><h2>Starkes Dach.<br><span class="muted">Verlässlicher Partner.</span></h2><p>Egal ob Sturmschaden, geplante Sanierung oder Dachrinne:<br>Dachservice Pintilei ist Ihr Fachbetrieb in Harburg.</p></div>{rows}</section><section class="dark section"><div class="wrap"><p class="eyebrow">VOM ERSTEN ANRUF BIS ZUM DICHTEN DACH</p><h2>Ihr Weg zum sanierten Dach.</h2>{steps(PROCESS)}<a class="text-link" href="/ablauf/">Unseren Ablauf kennenlernen ↗</a></div></section><section class="wrap section question-grid"><div><p class="eyebrow">HÄUFIGE FRAGEN</p><h2>Fragen zu<br>Dachservice Pintilei?</h2><a class="text-link" href="/faq/">Alle häufigen Fragen ↗</a></div>{faq(GENERAL_FAQS[:4])}</section>')

page('/leistungen/', 'Dachdecker-Leistungen in Harburg & Hamburg', 'Übersicht unserer Leistungen: Dachsanierung, Dachreparatur, Dachrinnenreinigung und Flachdachabdichtung durch Dachservice Pintilei in Harburg.', intro('Unsere Leistungen', 'Qualitätsarbeit.<br><span class="blue">Für Ihr Dach.</span>', 'Ob Einfeilhaus, Gewerbeobjekt oder Notdienst nach Sturm: Entdecken Sie unsere Fachleistungen in Harburg und Umgebung.') + strip + f'<section class="wrap section">{rows}</section>')

for s in SERVICES:
    path = '/leistungen/' + s['slug'] + '/'
    visual = photo(s['image'], s['alt'], eager=True) if s['category'] != 'ABDICHTUNG' else '<div class="clear-art"><span>DACH<br>SERVICE<br><em>PINTILEI.</em></span><p>Dauerhaft dicht und geschützt.</p></div>'
    body = intro(s['name'], s['short'].replace('\n', '<br>'), s['intro']) + f'<section class="wrap detail-hero"><div class="detail-photo">{visual}</div><aside class="blue-panel"><p class="eyebrow">PASSEND FÜR</p>{bullets(s["for"])}<p>{s["aside"]}</p>{btn("Anfrage vorbereiten", "/kontakt/?service=" + s["slug"], True)}</aside></section><section class="wrap section split"><div><p class="eyebrow">DARAUF KOMMT ES AN</p><h2>Klarer Umfang.<br>Guter Anfang.</h2><p class="lead">{s["overview"]}</p></div><div><h3>Das gehört zum Leistungsumfang</h3>{bullets(s["included"])}<p class="note">{s["scope_note"]}</p></div></section><section class="soft section"><div class="wrap"><p class="eyebrow">SCHRITT FÜR SCHRITT</p><h2>So läuft die Umsetzung.</h2>{steps(s["steps"])}</div></section><section class="wrap section split"><div><p class="eyebrow">GUT VORBEREITET</p><h2>Das hilft bei<br>Ihrer Anfrage.</h2><p>Mit diesen Angaben lässt sich Ihr Dachprojekt vorab gut einschätzen.</p>{bullets(s["prepare"])}</div><div class="border-panel"><p class="eyebrow">KOSTEN VERSTEHEN</p><h3>Was beeinflusst den Preis?</h3>{bullets(s["cost"])}<p>Wir erstellen Ihnen nach Besichtigung einen transparenten Kostenvoranschlag ohne versteckte Gebühren.</p>{btn("Dachprojekt beschreiben", "/kontakt/?service=" + s["slug"])}</div></section><section class="wrap section question-grid"><div><p class="eyebrow">HÄUFIGE FRAGEN</p><h2>Fragen zu dieser<br>Leistung.</h2></div>{faq(s["faqs"])}</section><section class="wrap related"><p class="eyebrow">WEITERE LEISTUNGEN VON DACHSERVICE PINTILEI</p><div>{"".join(f"<a href='/leistungen/{x['slug']}/'>{x['name']} ↗</a>" for x in SERVICES if x != s)}</div></section>'
    page(path, s['name'], s['description'], body)

page('/ablauf/', 'Ablauf Ihrer Dachsanierung & Reparatur', 'So einfach planen Sie Ihr Dachprojekt mit Dachservice Pintilei in Harburg: Von der Kontaktaufnahme bis zur fertigen Abnahme.', intro('Unser Ablauf', 'Verlässliche Arbeit<br>mit <span class="blue">klarem Plan.</span>', 'Wie läuft eine Dachreparatur oder Sanierung ab? Hier erfahren Sie Schritt für Schritt, wie Dachservice Pintilei Ihr Projekt umsetzt.') + f'<section class="wrap wide-image">{photo("moving", "Dachdeckerarbeiten bei Dachservice Pintilei", eager=True)}</section><section class="wrap section">{steps(PROCESS)}</section><section class="soft section"><div class="wrap split"><div><p class="eyebrow">UNSER VERSPRECHEN</p><h2>Worauf Sie sich<br>verlassen können.</h2></div><div>{bullets(["Transparente Festpreise & detaillierter Kostenvoranschlag", "Schnelle Reaktionszeit & Notdienst bei Sturmschäden", "Winsener Str. 19, 21077 Harburg als lokaler Ansprechpartner", "Hervorragende Kundenbewertungen (5.0 Sterne)", "Saubere und pünktliche Ausführung durch Fachkräfte"])}</div></div></section>')

page('/ueber-uns/', 'Über Dachservice Pintilei in Harburg', 'Ihr erfahrener Roofing Contractor in Harburg: Dachservice Pintilei steht für Qualität, Zuverlässigkeit und beste Kundenbewertungen (5.0 bei 69 Bewertungen).', intro('Über Dachservice Pintilei', 'Ihr Dachdecker<br>in <span class="blue">Harburg & Hamburg.</span>', 'Winsener Str. 19, 21077 Harburg · Telefon: +49 176 73501602 · ⭐ 5.0 (69 Google Bewertungen)') + f'<section class="wrap split section"><div class="statement">Qualität am Dach.<br>Verlässlich vor Ort.<br><span class="blue">5.0 Sterne Qualität.</span></div><div><p class="eyebrow">LOKALE EXPERTISE IN HARBURG</p><h2>Dachservice Pintilei – Ihr Fachbetrieb.</h2><p>Dachservice Pintilei ist Ihr verlässlicher Ansprechpartner für alle Arbeiten rund um Ihr Dach in Harburg, Hamburg und Umgebung. Egal ob Eindeckung, Sturmschaden-Reparatur, Dachrinnenreinigung oder Flachdachabdichtung – wir sorgen dafür, dass Ihr Haus nachhaltig geschützt bleibt.</p><p>Mit Sitz in der Winsener Str. 19, 21077 Harburg legen wir höchsten Wert auf Pünktlichkeit, ehrliche Beratung und sauberes Handwerk. 69 zufriedene Kundenbewertungen mit 5.0 Sternen sprechen für sich.</p><div style="margin-top:1.5rem;padding:1.2rem;background:#f0f4ff;border-radius:8px;border-left:4px solid #084bff;"><p style="margin:0;font-weight:600;color:#084bff;">📍 Kontaktdaten:</p><p style="margin:0.3rem 0 0 0;">Dachservice Pintilei<br>Winsener Str. 19, 21077 Harburg, Deutschland<br>Telefon: +49 176 73501602<br>Öffnungszeiten: Mo - Fr ab 07:00 Uhr geöffnet<br>Website: dachdecker-pintilei.de</p></div></div></section>')

options = ''.join(f'<option value="{s["slug"]}">{s["name"]}</option>' for s in SERVICES)
form = f'''<section class="wrap quote-layout"><aside><p class="eyebrow">DACHSERVICE PINTILEI · ANFRAGE</p><h2>Ihr Dachprojekt.<br>Schnell angefragt.</h2><p>Nennen Sie uns Ihr Anliegen. Wir melden uns umgehend bei Ihnen zurück oder erstellen Ihnen eine detaillierte Projektübersicht.</p><div class="quote-note"><strong>Direkt anrufen?</strong><p>Bei akuten Sturmschäden erreichen Sie uns direkt unter:<br><strong style="font-size:1.1rem;color:#084bff;">📞 +49 176 73501602</strong></p></div><a class="text-link" href="/faq/">Vorher noch eine Frage? ↗</a></aside><form id="quote-form"><div class="form-progress" aria-label="Schritte der Dach-Anfrage"><span class="active">01 Vorhaben</span><span>02 Kontaktdaten</span><span>03 Übersicht</span></div><div class="form-step" data-step="0"><h2>Was soll am Dach gemacht werden?</h2><label for="service">Gewünschte Dachleistung *</label><select name="service" id="service" required><option value="">Bitte auswählen</option>{options}</select><div class="form-grid"><div><label for="postal">Postleitzahl *</label><input id="postal" name="postal" required pattern="[0-9]{{5}}" inputmode="numeric" maxlength="5" autocomplete="postal-code" value="21077"></div><div><label for="city">Ort *</label><input id="city" name="city" required maxlength="100" autocomplete="address-level2" value="Harburg"></div></div><label for="date">Wunschtermin / Dringlichkeit (optional)</label><input id="date" name="date" type="date"><label for="details">Beschreiben Sie das Vorhaben oder den Schaden *</label><textarea id="details" name="details" required minlength="15" maxlength="2500" rows="5" placeholder="Zum Beispiel: Fehlende Ziegel nach Sturm, Dachrinnenreinigung für Einfamilienhaus oder geplante Neueindeckung. Bitte nennen Sie Besonderheiten."></textarea><p class="field-help">Mindestens 15 Zeichen.</p><button class="button" type="button" data-next>Weiter <span aria-hidden="true">→</span></button></div><div class="form-step" data-step="1" hidden><h2>Ihre Kontaktdaten</h2><label for="name">Ihr Name *</label><input name="name" id="name" required maxlength="100" autocomplete="name"><label for="email">E-Mail-Adresse *</label><input name="email" id="email" type="email" required maxlength="200" autocomplete="email"><label for="phone">Telefonnummer *</label><input name="phone" id="phone" type="tel" required maxlength="30" autocomplete="tel" placeholder="+49 176 ..."><label class="checkbox"><input name="understand" type="checkbox" required> <span>Ich möchte eine kostenfreie Anfrage an Dachservice Pintilei stellen.</span></label><div class="actions"><button class="button secondary" type="button" data-back>← Zurück</button><button class="button" type="button" data-next>Angaben prüfen →</button></div></div><div class="form-step" data-step="2" hidden><h2>Alles auf einen Blick.</h2><dl id="quote-review"></dl><p>Prüfen Sie Ihre Angaben vor dem Absenden / Herunterladen.</p><div class="actions"><button class="button secondary" type="button" data-back>← Bearbeiten</button><button class="button" type="submit">Projektbeschreibung herunterladen ↓</button></div></div><p id="form-status" role="status" aria-live="polite"></p></form></section>'''

page('/kontakt/', 'Kontakt zu Dachservice Pintilei Harburg', 'Dachdecker in Harburg kontaktieren: Winsener Str. 19, 21077 Harburg. Tel: +49 176 73501602. Anfrage stellen oder Notdienst rufen.', intro('Kontakt & Anfahrt', 'Dachservice Pintilei.<br><span class="blue">Hier erreichen Sie uns.</span>', 'Winsener Str. 19, 21077 Harburg · Telefon: +49 176 73501602 · Mo - Fr ab 07:00 Uhr geöffnet.') + form)

page('/faq/', 'Häufige Fragen – Dachservice Pintilei', 'Antworten zu Leistungen, Notdienst bei Sturmschäden, Einsatzgebieten in Harburg & Hamburg, Preisen und Öffnungszeiten von Dachservice Pintilei.', intro('Häufige Fragen', 'Antworten rund um<br><span class="blue">Ihr Dach.</span>', 'Häufig gestellte Fragen zu unseren Dachdecker-Leistungen in Harburg.') + '<section class="wrap narrow section">' + faq(GENERAL_FAQS) + '</section>')

page('/datenschutz/', 'Datenschutz – Dachservice Pintilei', 'Datenschutzhinweise von Dachservice Pintilei, Winsener Str. 19, 21077 Harburg.', intro('Datenschutz', 'Schutz Ihrer Daten.<br>Dachservice Pintilei.', 'Datenschutzerklärung für Besucher der Webseite dachdecker-pintilei.de') + '''<article class="wrap prose section"><h2>Verantwortlicher</h2><p>Dachservice Pintilei<br>Winsener Str. 19<br>21077 Harburg, Deutschland<br>Telefon: +49 176 73501602<br>Webseite: dachdecker-pintilei.de</p><h2>Erhebung personenbezogener Daten</h2><p>Wir verarbeiten personenbezogene Daten wie Name, E-Mail-Adresse und Telefonnummer ausschließlich zur Bearbeitung Ihrer Anfragen und Dachdecker-Aufträge.</p></article>''')

page('/nutzungshinweise/', 'Nutzungshinweise – Dachservice Pintilei', 'Hinweise zum Angebot von Dachservice Pintilei in Harburg.', intro('Nutzungshinweise', 'Dachservice Pintilei.<br>Harburg.', 'Hinweise zur Nutzung unserer Dienste.') + '''<article class="wrap prose section"><h2>Dienstleistungen</h2><p>Dachservice Pintilei führt Dacharbeiten, Dachreparaturen, Dachrinnenreinigungen und Abdichtungen in Harburg und Umgebung fachgerecht aus.</p></article>''')

page('/impressum/', 'Impressum – Dachservice Pintilei Harburg', 'Impressum und Anbieterkennzeichnung von Dachservice Pintilei in Harburg.', intro('Impressum', 'Anbieterkennzeichnung.<br><span class="blue">Dachservice Pintilei.</span>', 'Rechtliche Angaben gemäß § 5 DDG.') + '''<article class="wrap prose section"><h2>Anbieter & Kontakt</h2><p><strong>Dachservice Pintilei</strong><br>Winsener Str. 19<br>21077 Harburg, Deutschland</p><p><strong>Inhaber:</strong> Pintilei<br><strong>Telefon:</strong> +49 176 73501602<br><strong>Webseite:</strong> <a href="https://dachdecker-pintilei.de/" target="_blank" rel="noopener">dachdecker-pintilei.de</a><br><strong>Öffnungszeiten:</strong> Mo - Fr ab 07:00 Uhr</p><p><strong>Unternehmensgegenstand:</strong> Dachdecker-Dienstleistungen (Roofing Contractor), Dachsanierung, Dachreparatur, Dachrinnenreinigung & Flachdachabdichtung.</p></article>''')

page('/404.html', 'Seite nicht gefunden', 'Zurück zu Dachservice Pintilei.', intro('404 – Seite nicht gefunden', 'Zurück zur<br><span class="blue">Startseite.</span>', 'Diese Seite ist nicht verfügbar.') + '<div class="wrap actions section">' + btn('Leistungen ansehen', '/leistungen/') + btn('Zur Startseite', '/', True) + '</div>')

(OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + BASE + '/sitemap.xml\n')
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>' + BASE + p + '</loc></url>' for p in PAGES) + '</urlset>')

for old, new in ROUTES.items():
    target = OUT / old.strip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f'<!doctype html><html lang="de-DE"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Seite umgezogen | Dachservice Pintilei</title><meta name="description" content="Diese Dachservice Pintilei Seite ist unter einer neuen Adresse erreichbar."><meta name="robots" content="noindex,follow"><link rel="canonical" href="{BASE+new}"><meta http-equiv="refresh" content="0;url={new}"></head><body><h1>Diese Seite ist umgezogen.</h1><p><a href="{new}">Weiter zu Dachservice Pintilei</a></p></body></html>')

print(f'Built {len(PAGES)+1} pages for Dachservice Pintilei')
