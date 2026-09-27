# Clearwork

A complete, static, thirteen-page service business demo. White/cobalt editorial design, responsive imagery, reduced-motion-aware reveals, accessible navigation, detailed service content and a local-only quote brief builder.

## Edit and build

- Edit service content in `scripts/content.py` and page templates in `scripts/build.py`.
- CSS and JavaScript are authored directly in `dist/assets/`.
- Run `python scripts/build.py` (Python standard library only).
- Run `python scripts/validate.py` for static integrity checks (Python standard library only).
- Optional local serving: `python -m http.server 8000 --directory dist`.
- Deploy the `dist` static directory using `.openai/hosting.json`.

## Launch configuration

This is a private concept demo with explicit `noindex,follow` on every page. SEO foundations include semantic HTML, descriptive titles, descriptions, canonical URLs, WebPage structured data, sitemap, responsive WebP images and no framework runtime. Public indexing requires configuring the real business/domain, appropriate contact and legal details, changing noindex and publishing to the intended public audience. Search rankings are not guaranteed.

The quote form validates three stages and downloads a local text brief. It does not send email, persist data, reserve dates or take payments. Connect a real enquiry endpoint and update privacy text before accepting enquiries. No analytics scripts are installed. Illustrative generated images are not actual employee or project photographs.

## Validation limits

Static checks and JavaScript syntax checks were run. CSS supports 320px through large desktop widths and reduced motion. No live browser, device, WebMCP compatibility or Lighthouse audit was performed in this delivery workflow.

## German localization — 17 September 2026

All 14 content pages use German copy and de-DE document/schema language; social metadata uses de_DE. German canonical service routes target Tank- & Zisternenreinigung, Gebäudereinigung, Umzugsservice, and Entrümpelung & Schrottabholung. Ten former English routes retain noindex static transition pages and are excluded from the sitemap. One German language version is published; no unsupported alternate-language hreflang claims are emitted.

The form uses a five-digit German postcode, separate locality, German validation and DD.MM.YYYY dates in the German text download. Moving and cistern imagery now uses illustrative German residential settings. Typography and mobile layout account for longer German compound nouns. The brand is not claimed as a registered trademark.

Impressum is explicitly incomplete because no real operator has been supplied. No invented address, city coverage, phone, reviews, certification, pricing or LocalBusiness data. Supply legal company name, actual address, contact details, service area and applicable company information before public launch. Hosting audience and noindex are preserved. Enquiry delivery remains local-only.

References consulted: https://www.gesetze-im-internet.de/ddg/__5.html and https://developers.google.com/search/docs/specialty/international/localized-versions . No legal-compliance certification or ranking claim is made.
