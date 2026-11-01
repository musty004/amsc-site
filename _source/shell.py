"""Shared HTML shell for every AMSC page: head, header, footer and the small
components the pages are built from. Edit here, run build.py, and every page
updates together."""
import json, os
from html import escape
import data as D

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

# build.py fills these in before any page is rendered
ASSET_VER = {"css": "1", "js": "1"}
LOCAL_CLASH = False   # True when assets/fonts/ClashDisplay-Variable.woff2 exists

with open(os.path.join(HERE, "img-manifest.json")) as f:
    MANIFEST = json.load(f)

# ------------------------------------------------------------------ icons
_S = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"'
_F = 'viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"'
ICONS = {
"arrow":   f'<svg {_S}><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
"external":f'<svg {_S}><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
"clock":   f'<svg {_S}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
"pin":     f'<svg {_S}><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
"calendar":f'<svg {_S}><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
"book":    f'<svg {_S}><path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v18H6.5A2.5 2.5 0 0 0 4 22z"/><path d="M8 7h8M8 11h6"/></svg>',
"quran":   f'<svg {_S}><path d="M12 6.5S9.5 4 5 4v14c4.5 0 7 2 7 2s2.5-2 7-2V4c-4.5 0-7 2.5-7 2.5Z"/><path d="M12 6.5V20"/></svg>',
"mosque":  f'<svg {_S}><path d="M12 3c2.5 2 4 3.8 4 6H8c0-2.2 1.5-4 4-6Z"/><path d="M4 21V12a3 3 0 0 1 3-3M20 21V12a3 3 0 0 0-3-3"/><path d="M4 21h16M9 21v-4a3 3 0 0 1 6 0v4"/></svg>',
"arch":    f'<svg {_S}><path d="M5 21V10.5C5 7 8 4.6 12 3c4 1.6 7 4 7 7.5V21"/><path d="M9 21v-6a3 3 0 0 1 6 0v6M3 21h18"/></svg>',
"users":   f'<svg {_S}><circle cx="9" cy="8" r="3.2"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 5.5a3.2 3.2 0 0 1 0 6M17.5 14.4A6.5 6.5 0 0 1 21.5 20"/></svg>',
"heart":   f'<svg {_S}><path d="M12 20s-7-4.5-7-9.5A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 7 3.5C19 15.5 12 20 12 20Z"/></svg>',
"cap":     f'<svg {_S}><path d="M2 8.5 12 4l10 4.5-10 4.5Z"/><path d="M6 11v4.5c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5V11"/></svg>',
"pen":     f'<svg {_S}><path d="M4 20h4L20 8a2.8 2.8 0 0 0-4-4L4 16Z"/><path d="M14.5 5.5 18.5 9.5"/></svg>',
"camera":  f'<svg {_S}><path d="M3 8.5A2.5 2.5 0 0 1 5.5 6h2L9 4h6l1.5 2h2A2.5 2.5 0 0 1 21 8.5v9A2.5 2.5 0 0 1 18.5 20h-13A2.5 2.5 0 0 1 3 17.5Z"/><circle cx="12" cy="13" r="3.5"/></svg>',
"gift":    f'<svg {_S}><rect x="3" y="9" width="18" height="12" rx="1.5"/><path d="M3 13h18M12 9v12"/><path d="M12 9C10 9 7.5 8.5 7.5 6.2A2.2 2.2 0 0 1 12 6a2.2 2.2 0 0 1 4.5.2C16.5 8.5 14 9 12 9Z"/></svg>',
"shield":  f'<svg {_S}><path d="M12 3 20 6v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6Z"/><path d="m9 12 2 2 4-4"/></svg>',
"chip":    f'<svg {_S}><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M10 2v4M14 2v4M10 18v4M14 18v4M2 10h4M2 14h4M18 10h4M18 14h4"/></svg>',
"ball":    f'<svg {_S}><circle cx="12" cy="12" r="9"/><path d="m12 7 4 3-1.5 4.7h-5L8 10Z"/><path d="M12 3v4M4.5 9.5 8 10M19.5 9.5 16 10M7.5 20l2-5.3M16.5 20l-2-5.3"/></svg>',
"mic":     f'<svg {_S}><rect x="9" y="2.5" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M9 21h6"/></svg>',
"mail":    f'<svg {_S}><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/></svg>',
"phone":   f'<svg {_S}><path d="M6 3h3l1.5 4.5-2 1.5a12 12 0 0 0 6.5 6.5l1.5-2L21 15v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4 5.2 2 2 0 0 1 6 3Z"/></svg>',
"download":f'<svg {_S}><path d="M12 3v12M7.5 11 12 15.5 16.5 11"/><path d="M4 19h16"/></svg>',
"lock":    f'<svg {_S}><rect x="4.5" y="10" width="15" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
"compass": f'<svg {_S}><circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5Z"/></svg>',
"star":    f'<svg {_S}><path d="m12 3.5 2.6 5.4 5.9.8-4.3 4.2 1 5.9-5.2-2.8L6.8 19.8l1-5.9L3.5 9.7l5.9-.8Z"/></svg>',
"briefcase":f'<svg {_S}><rect x="3" y="7.5" width="18" height="12.5" rx="2"/><path d="M9 7.5V6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v1.5M3 12.5h18"/></svg>',
"wheat":   f'<svg {_S}><path d="M12 22V9"/><path d="M12 13c-2.5 0-4-1.6-4-4 2.5 0 4 1.6 4 4ZM12 13c2.5 0 4-1.6 4-4-2.5 0-4 1.6-4 4ZM12 9C9.8 9 8.5 7.6 8.5 5.5 10.7 5.5 12 6.9 12 9ZM12 9c2.2 0 3.5-1.4 3.5-3.5C13.3 5.5 12 6.9 12 9ZM12 17c-2.5 0-4-1.6-4-4 2.5 0 4 1.6 4 4ZM12 17c2.5 0 4-1.6 4-4-2.5 0-4 1.6-4 4Z"/><path d="M12 5.5V2"/></svg>',
"wings":   f'<svg {_S}><path d="M12 17c-1.6-3-5-4-10-4 1.5 3.2 5 5 10 5 5 0 8.5-1.8 10-5-5 0-8.4 1-10 4Z"/><path d="M4 9.5c2.5 0 5 .8 6.5 2.5M20 9.5c-2.5 0-5 .8-6.5 2.5"/></svg>',
"check":   f'<svg {_S}><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>',
"share":   f'<svg {_S}><circle cx="18" cy="5.5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="18.5" r="2.5"/><path d="m8.2 10.8 7.6-4.1M8.2 13.2l7.6 4.1"/></svg>',
"printer": f'<svg {_S}><path d="M7 8V3h10v5"/><rect x="3" y="8" width="18" height="9" rx="2"/><path d="M7 14h10v7H7z"/></svg>',
"alert":   f'<svg {_S}><path d="M12 3 2 20h20Z"/><path d="M12 10v4M12 17h.01"/></svg>',
"menu":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
"close":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6 6 18"/></svg>',
"whatsapp":f'<svg {_F}><path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2Zm5.8 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.1.1-1.8-.1-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5.1-4.5-.1-.2-1.2-1.5-1.2-2.9s.7-2 1-2.3c.2-.3.5-.4.7-.4h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.5-.3.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2 1.3 2.3 1.4.3.1.5.1.7-.1l.8-1c.2-.2.4-.2.6-.1l2 1c.2.1.4.2.4.3.1.2.1.7-.1 1.4Z"/></svg>',
"instagram":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true" focusable="false"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor" stroke="none"/></svg>',
"facebook":f'<svg {_F}><path d="M13.5 21v-7.6h2.6l.4-3h-3V8.5c0-.9.25-1.5 1.5-1.5H16.6V4.3A20 20 0 0 0 14.3 4.2c-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21Z"/></svg>',
}


def icon(name, cls="ico"):
    svg = ICONS[name]
    return svg.replace("<svg ", f'<svg class="{cls}" ', 1) if cls else svg


# ------------------------------------------------------------------ helpers
def ar(text, cls="ar"):
    """Arabic text, marked up so screen readers and browsers shape it correctly."""
    return f'<span class="{cls}" lang="ar" dir="rtl">{text}</span>'


def img(name, alt, sizes="(min-width: 1100px) 50vw, 100vw", cls="", eager=False, style=""):
    """Responsive WebP image from the manifest written by images.py."""
    m = MANIFEST[name]
    sizes_list = m["sizes"]
    big = sizes_list[-1]
    fallback = next((s for s in sizes_list if s["w"] >= 800), big)
    srcset = ", ".join(f'assets/img/{s["file"]} {s["w"]}w' for s in sizes_list)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    return (f'<img{c} src="assets/img/{fallback["file"]}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{big["w"]}" height="{big["h"]}" alt="{escape(alt, quote=True)}" {load} decoding="async"{st}>')


def ext(href, text, cls=""):
    """External link: opens in a new tab, marked for screen readers."""
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="{href}" target="_blank" rel="noopener">{text}{icon("external", "ico ico--ext")}<span class="sr-only"> (opens in a new tab)</span></a>'


def pill(text, kind=""):
    k = f" pill--{kind}" if kind else ""
    return f'<span class="pill{k}">{text}</span>'


def mail_link(cls="", text=None):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="mailto:{D.EMAIL}">{text or D.EMAIL}</a>'


# ------------------------------------------------------------------ chrome
NAV = [
    ("about.html", "About"),
    ("programmes.html", "Programmes"),
    ("events.html", "Events"),
    ("executive.html", "Executives"),
    ("freshers.html", "Freshers"),
    ("gallery.html", "Gallery"),
    ("blog.html", "Blog"),
    ("contact.html", "Contact"),
]

LOGO = '<img class="brand__mark" src="assets/img/logo-icon-40.webp" srcset="assets/img/logo-icon-80.webp 2x" alt="" width="40" height="40">'
LOGO_WHITE = '<img class="brand__mark" src="assets/img/logo-mark-48.webp" srcset="assets/img/logo-mark-96.webp 2x" alt="" width="48" height="48" loading="lazy" decoding="async">'


def header(current):
    links = "".join(
        f'<li><a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == current else ""}>{t}</a></li>'
        for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="salahbar" role="region" aria-label="Prayer times in Kaduna today">
  <div class="salahbar__inner">
    <a class="salahbar__label" href="salah.html">Prayer times, Kaduna</a>
    <ul class="salahbar__list" id="salah-list"></ul>
    <span class="salahbar__next" id="salah-next" aria-live="polite"></span>
  </div>
</div>
<header class="site-header">
  <div class="header__inner">
    <a class="brand" href="index.html" aria-label="AMSC home">
      {LOGO}
      <span class="brand__text">
        <span class="brand__name">AMSC</span>
        <span class="brand__sub">AFIT Muslim Students&rsquo; Community</span>
      </span>
    </a>
    <nav class="nav" id="primary-nav" aria-label="Main">
      <ul class="nav__list">{links}</ul>
      <div class="nav__extra">
        <a href="salah.html">Prayer times</a>
        <a href="academics.html">Academics</a>
        <a href="sisters.html">Sisters</a>
        <a href="welfare.html">Welfare</a>
        <a href="amanah.html">Amanah Desk</a>
      </div>
      <a class="btn btn--yellow nav__join" href="{D.JOIN}">Join AMSC</a>
    </nav>
    <button class="navtoggle" type="button" aria-expanded="false" aria-controls="primary-nav">
      <span class="navtoggle__open">{icon("menu", "")}</span><span class="navtoggle__close">{icon("close", "")}</span>
      <span class="sr-only">Menu</span>
    </button>
  </div>
</header>'''


def footer():
    pubs = (ext(D.SUBSTACK, "Read our publications") if D.SUBSTACK
            else '<span class="footer__soon">Publications: coming soon</span>')
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer__top">
      <div class="footer__brand">
        <a class="brand brand--light" href="index.html" aria-label="AMSC home">{LOGO_WHITE}
          <span class="brand__text">
            <span class="brand__name">AMSC</span>
            <span class="brand__sub">AFIT Muslim Students&rsquo; Community</span>
          </span></a>
        <p class="footer__tagline">{ar(D.TAGLINE_AR, "ar footer__ar")}<span>{D.TAGLINE_EN}</span></p>
        <p class="footer__place">Air Force Institute of Technology, Kaduna</p>
      </div>
      <div>
        <h2 class="footer__h">Explore</h2>
        <ul>
          <li><a href="about.html">About AMSC</a></li>
          <li><a href="programmes.html">Programmes</a></li>
          <li><a href="events.html">Events</a></li>
          <li><a href="executive.html">Executive Committee</a></li>
          <li><a href="gallery.html">Gallery</a></li>
          <li><a href="blog.html">Blog</a></li>
        </ul>
      </div>
      <div>
        <h2 class="footer__h">For students</h2>
        <ul>
          <li><a href="freshers.html">Freshers&rsquo; guide</a></li>
          <li><a href="academics.html">Academics</a></li>
          <li><a href="salah.html">Prayer times</a></li>
          <li><a href="sisters.html">Sisters</a></li>
          <li><a href="welfare.html">Welfare</a></li>
          <li><a href="amanah.html">Amanah Desk</a></li>
          <li><a href="library.html">Library</a></li>
        </ul>
      </div>
      <div>
        <h2 class="footer__h">Get involved</h2>
        <ul>
          <li><a href="{D.JOIN}">Join AMSC</a></li>
          <li><a href="join.html#volunteer">Volunteer</a></li>
          <li><a href="give.html">Give and dues</a></li>
          <li><a href="alumni.html">AMAN alumni network</a></li>
          <li><a href="contact.html">Contact us</a></li>
        </ul>
      </div>
      <div>
        <h2 class="footer__h">Contact</h2>
        <ul>
          <li>{mail_link("footer__email")}</li>
          <li><a href="{D.JOIN}">Join the WhatsApp Community</a></li>
          <li>{pubs}</li>
        </ul>
        <div class="social">
          <a href="{D.IG}" target="_blank" rel="noopener" aria-label="Instagram {D.IG_HANDLE} (opens in a new tab)">{icon("instagram", "")}</a>
          <a href="{D.FB}" target="_blank" rel="noopener" aria-label="Facebook (opens in a new tab)">{icon("facebook", "")}</a>
          <a href="{D.JOIN}" aria-label="Register to join the WhatsApp Community">{icon("whatsapp", "")}</a>
        </div>
      </div>
    </div>
    <div class="footer__bottom">
      <span>&copy; 2026 {D.ORG} ({D.SHORT}). {D.CAMPAIGN}</span>
      <span>Maintained by the AMSC Media team</span>
    </div>
  </div>
</footer>'''


def head_fonts():
    if LOCAL_CLASH:
        return ""
    url = "https://api.fontshare.com/v2/css?f[]=clash-display@500,600&amp;display=swap"
    return f'''<link rel="preconnect" href="https://api.fontshare.com">
<link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
<link rel="preload" as="style" href="{url}">
<link rel="stylesheet" href="{url}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{url}"></noscript>'''


def page(slug, title, description, body, current=None, extra_head="", noindex=False):
    cur = current if current is not None else slug
    full_title = f"{D.ORG} ({D.SHORT})" if slug == "index.html" else f"{title} | {D.SHORT}"
    url = D.SITE_URL + "/" + ("" if slug == "index.html" else slug)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f'''<!DOCTYPE html>
<html lang="en-NG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{escape(description, quote=True)}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0056CE">
<meta property="og:site_name" content="{D.ORG}">
<meta property="og:title" content="{escape(title if slug != 'index.html' else D.ORG, quote=True)}">
<meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{D.SITE_URL}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="assets/fonts/dm-sans-latin-wght.woff2" as="font" type="font/woff2" crossorigin>
{head_fonts()}
<link rel="stylesheet" href="assets/style.css?v={ASSET_VER['css']}">
<link rel="icon" href="assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
{extra_head}</head>
<body>
{header(cur)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/main.js?v={ASSET_VER['js']}" defer></script>
</body>
</html>
'''


def pagehead(title, lede, crumb=None):
    trail = f'<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span>{crumb or title}</nav>'
    return f'''<section class="pagehead">
  <div class="wrap pagehead__inner">
    {trail}
    <h1>{title}</h1>
    <p class="pagehead__lede">{lede}</p>
  </div>
</section>'''


def band(heading, text, primary, secondary=None):
    """Closing call to action on a blue panel. primary/secondary are (href, label)."""
    def a(link, cls):
        href, label = link
        if href.startswith("http"):
            return f'<a class="btn {cls}" href="{href}" target="_blank" rel="noopener">{label}<span class="sr-only"> (opens in a new tab)</span></a>'
        return f'<a class="btn {cls}" href="{href}">{label}</a>'
    second = a(secondary, "btn--line-light") if secondary else ""
    return f'''<section class="section section--tight">
  <div class="wrap">
    <div class="band">
      <div class="band__copy"><h2>{heading}</h2><p>{text}</p></div>
      <div class="band__actions">{a(primary, "btn--yellow")}{second}</div>
    </div>
  </div>
</section>'''


def soon(heading="Publications coming soon", text="Our publications and updates will be available soon."):
    return f'''<div class="soon">
  {pill("Coming soon", "green")}
  <h3>{heading}</h3>
  <p>{text}</p>
</div>'''


def person(p, compact=False, show_wing=False, whatsapp=None):
    name, dept, level, role, phone, _ = p
    wing = f' <span class="person__wing">{D.wing_of(p)}</span>' if show_wing else ""
    if compact:
        ph = ""
    elif phone:
        ph = f'<a class="person__tel" href="tel:{D.tel(phone)}">{icon("phone")}{D.pretty_phone(phone)}<span class="sr-only">, call {name}</span></a>'
    else:
        ph = '<span class="person__tel person__tel--none">Contact not provided</span>'
    if whatsapp:
        ph += f'<a class="person__tel person__wa" href="{whatsapp}" target="_blank" rel="noopener">{icon("whatsapp")}Chat on WhatsApp<span class="sr-only"> with {name} (opens WhatsApp)</span></a>'
    meta = f'<span class="person__meta">{dept}, {level}</span>'
    return f'''<li class="person{" person--compact" if compact else ""}">
  <span class="mono" aria-hidden="true">{D.initials(name)}</span>
  <span class="person__body">
    <span class="person__role">{role}{wing}</span>
    <strong class="person__name">{name}</strong>
    {meta}
    {ph}
  </span>
</li>'''


def formspree_form(action, inner, title, text, subject, cls="form"):
    """Form sent to Formspree in the background; a full-page thank-you appears on success."""
    return f'''<form class="{cls}" action="{action}" method="POST" data-formspree data-success-title="{escape(title, quote=True)}" data-success-text="{escape(text, quote=True)}">
  <input type="hidden" name="_subject" value="{escape(subject, quote=True)}">
  <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
{inner}
  <p class="form-error" role="alert" hidden></p>
</form>'''


def gform():
    """The registration Google Form, embedded so visitors stay on the site.
    main.js loads it, then shows a full-page thank-you after it is submitted."""
    return f'''<div class="gform" data-gform="{D.GFORM_EMBED}">
  <iframe title="AMSC registration form" data-title="AMSC registration form">Loading the form&hellip;</iframe>
  <noscript><p class="note">The form needs JavaScript. <a href="{D.GFORM}">Open the registration form</a>.</p></noscript>
</div>
<p class="note">Form not loading? {ext(D.GFORM, "Open it in a new tab")}.</p>'''
