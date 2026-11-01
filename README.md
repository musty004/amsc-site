# AMSC website — v3 (2026/2027 session)

The official website of the **AFIT Muslim Students' Community (AMSC)**, Air Force Institute of
Technology, Kaduna. *معًا في الدين والهدف — Together in Faith and Purpose.*

A static site: plain HTML, one stylesheet, one small script. No framework, no database.

---

## Publish it

1. Open Netlify, go to the site's **Deploys** tab, and drag this whole `amsc-site` folder onto it.
2. Netlify reads `_headers` (caching and security headers) and `_redirects` (old page names,
   and keeping `_source/` private) automatically.
3. Keep the Netlify account, domain and this folder on an **AMSC organisation account**, not a
   personal one, so the site survives when its builder graduates.

### Forms and contact routes

| What | Where it goes |
|---|---|
| Registration (membership + WhatsApp Community) | The AMSC Google Form, embedded on `join.html#register`. Every "Join" and "Join the WhatsApp Community" button on the site opens it. An admin adds registered students to the WhatsApp Community. |
| Contact form (`contact.html`) | Formspree `myeepzbb` |
| Volunteer form (`join.html#volunteer-form`) | Formspree `myeepzbb` (same as contact, marked "Volunteering") |
| AMAN alumni register (`alumni.html`) | Formspree `xdeedkpz` |
| Welfare | No form. WhatsApp buttons to the brothers' and sisters' welfare officers. |
| Islamiyya notes access | WhatsApp to the Mudeer |

After every successful submission, a full-page thank-you message appears. After the first
deploy, send one test message through each Formspree form and confirm it arrives in the Formspree
inbox; a brand-new Formspree form may ask its owner to confirm by email first.

The Google Form, Formspree endpoints and WhatsApp numbers are all set in `_source/data.py`.

---

## Edit it

There are two ways.

**Small text fix:** open the `.html` file, change the words, save, re-upload. Note that the next
full rebuild will overwrite that change unless you also make it in `_source/`.

**Anything lasting:** edit the files in `_source/`, then rebuild:

```
cd _source
python3 build.py
```

| To change… | Edit |
|---|---|
| Executive Committee names, roles, phones | `_source/data.py` → `BROTHERS`, `SISTERS` |
| Email, Instagram, Facebook, Google Form, Formspree links | `_source/data.py` (top of the file) |
| The Substack link, once it exists | `_source/data.py` → `SUBSTACK = "https://…"` |
| Freshers' clearance steps | `_source/data.py` → `FRESHER_*` |
| The website address (when you get a domain) | `_source/data.py` → `SITE_URL` |
| Header, footer, navigation | `_source/shell.py` |
| Page text | `page_home.py` (home), `pages_a.py` (About, Programmes, Join), `pages_b.py` (Academics, Events, Prayer), `pages_c.py` (Sisters, Welfare, Library), `pages_d.py` (Gallery, Blog, Give, Alumni, Contact), `pages_e.py` (Executive, Freshers, 404) |
| Colours, fonts, spacing | `assets/style.css`, tokens at the top under `:root` |
| Jama'ah times at the AFIT Mosque | `assets/main.js` → `JAMAAH` |

`build.py` also writes `sitemap.xml`, `robots.txt`, `site.webmanifest`, `_headers`, `_redirects`,
a tiny Arabic font file containing only the letters the site uses, and version numbers on the CSS
and JS so visitors always get the latest copy. Requires Python 3 with `fonttools` and `brotli`
(`pip install fonttools brotli`).

### Photos

1. Put the full-size JPG in `_source/img-originals/`.
2. Add its name to `PHOTOS` (or `FLYERS`) in `_source/images.py`.
3. Run `python3 images.py`, then `python3 build.py`.

This creates compressed WebP copies at several widths. Browsers download only the size they
need, and images below the fold load only when scrolled to. Requires Pillow (`pip install pillow`).

Do not publish a photograph of a sister without her permission.

### When the Substack publication exists

Set `SUBSTACK` in `data.py` and rebuild. The footer switches from "Publications: coming soon" to
a live link. Before that: confirm the official name and URL, which email owns the account, who
manages it, recovery and password arrangements, and a second trusted administrator.

---

## Brand system

| Token | Value | Use |
|---|---|---|
| Primary blue | `#0056CE` | Hero, page headers, buttons, CTA panels. Dominant colour. |
| Yellow | `#FCBA00` | Primary buttons on blue, labels, highlights |
| Green | `#18C021` | Small accents and status dots. For green **text** the site uses `#0F7A17`, which passes contrast checks. |
| White | `#FFFFFF` | Backgrounds and text on blue |
| Ink | `#0B2559` | Headings and body text: a deep shade of the brand blue |
| Mist | `#EEF4FD` | Alternate section background |

- **Clash Display** for headlines, **DM Sans** for everything else (−3% letter spacing on UI text,
  slightly relaxed for long paragraphs), **Noto Kufi Arabic** for Arabic text.
- **Signature shapes:** the mihrab arch (photo frames, monograms, page headers) and a faint
  eight-point star lattice on blue panels.
- **Clash Display** is loaded from Fontshare, its official free source. To self-host it instead
  (slightly faster), download it from fontshare.com, put `ClashDisplay-Variable.woff2` in
  `assets/fonts/`, and run `build.py`; the build detects the file and switches over.

---

## Pages

Main navigation: Home · About · Programmes · Events · Executives · Freshers · Gallery · Blog ·
Contact · Join AMSC

Also: Academics · Prayer times · Sisters · Welfare · Library · Give · AMAN alumni · 404

`media.html` is now `gallery.html` and `press.html` is now `blog.html`; old links redirect.

---

## What changed in v3

- Rebuilt on the official brand: #0056CE / #FCBA00 / #18C021 / white, Clash Display + DM Sans.
  The previous navy-and-gold palette and four font families are gone.
- Arabic tagline, English tagline, core message, key message and "One Ummah. One Campus." added.
- Simpler home page: hero, introduction, four areas of work, Executive preview, publications
  "coming soon", call to action.
- New **Executive Committee** page: what the committee does, and all 36 nominees for 1448 AH /
  2026–2027 by portfolio, with department, level and tap-to-call numbers.
- New **Freshers' guide**: checklist that remembers ticks, payment steps, clearance route, the
  JAMB CAPS name check, welfare officers' numbers, share and print buttons.
- Programmes page now covers all seven programmes in the brief, including Da'wah Week and the
  Annual Ramadan Lecture and Iftar.
- Official email on every page. Instagram (@afitmsc) and Facebook links from the brief. The AMSC
  WhatsApp Community is joined by registering; no direct group link or QR code is published.
  YouTube removed (not in the brief). No Substack link.
- Events relabelled: last session's dated events now show as last session, not "coming up".
- About page: values, the meaning of the logo, purpose and committees.
- Forms: registration through the embedded Google Form; contact, volunteer and alumni through
  Formspree with a full-page thank-you; welfare through WhatsApp to the welfare officers.
- Performance: images converted to responsive WebP (home page on a phone down from about 1.9 MB
  to about 0.4 MB; About page from 0.74 MB to 0.15 MB), lazy loading, width/height on every
  image, two self-hosted font files,
  long-term caching, a fixed prayer-times bug, and the infinite ticker animation removed.
- Accessibility: skip link, visible focus, labelled forms, screen-reader text for new-tab links,
  Arabic marked as Arabic, colour contrast checked. Lighthouse (mobile): accessibility 100,
  best practices 100, SEO 100 on all pages tested.
- Link previews on WhatsApp now show a branded image (`assets/img/og-image.jpg`).

## To confirm before or soon after launch

- **Phone numbers:** the brief asks for contact numbers on the site. Confirm each officer is
  happy for their number to be public.
- **WhatsApp line +234 902 759 7106** is carried over from v2 and is not in the 2026 brief. Keep
  or remove it in `data.py` (`WA_LINE`).
- **Spellings:** "Fatima Abubakar" (brief) vs "Fatimah Abubakar" (welfare flyer); "Musabaqatul"
  (AMSC flyers, used here) vs "Musaabaqatul" (brief). Two different nominees are listed as
  "Public Relation Officer II" (Abubakar Muhammad Girei and Ummul Khair Muhammad).
- **Tutorial timetable:** the Academics page shows "coming soon". Add the table in
  `_source/pages_b.py` when the academics team confirms it.
- **Jama'ah times** in `main.js` and the fallback prayer timetable.
- The Sendforth agenda flyer says "4th July 2027"; the main flyer says 2026.
