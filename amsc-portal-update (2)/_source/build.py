"""Build the AMSC site.

    cd _source
    python3 build.py

Writes every .html page into the site folder (the folder above _source/),
plus sitemap.xml, robots.txt, site.webmanifest, the Netlify _headers and
_redirects files, the Arabic font subset and cache-busting asset versions.

Run images.py first if you added or replaced photos.
"""
import hashlib, os, re, shutil, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import data as D
import shell

FONTS_SRC = os.path.join(HERE, "fonts-src")
FONTS_OUT = os.path.join(ROOT, "assets", "fonts")
CSS = os.path.join(ROOT, "assets", "style.css")
JS = os.path.join(ROOT, "assets", "main.js")
CLASH_FILE = os.path.join(FONTS_OUT, "ClashDisplay-Variable.woff2")


def short_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def prepare_css():
    """Switch to a self-hosted Clash Display automatically if the file exists."""
    shell.LOCAL_CLASH = os.path.exists(CLASH_FILE)
    css = open(CSS, encoding="utf-8").read()
    block = ('/*CLASH_LOCAL*/@font-face{font-family:"Clash Display";'
             'src:url("fonts/ClashDisplay-Variable.woff2") format("woff2");'
             'font-weight:200 700;font-style:normal;font-display:swap}')
    css = re.sub(r"/\*CLASH_LOCAL\*/(@font-face\{[^}]*\})?", block if shell.LOCAL_CLASH else "/*CLASH_LOCAL*/", css)
    with open(CSS, "w", encoding="utf-8") as f:
        f.write(css)


def main():
    prepare_css()
    portal_files()
    shell.ASSET_VER["css"] = short_hash(CSS)
    shell.ASSET_VER["js"] = short_hash(JS)
    v = lambda rel: f"{rel}?v={short_hash(os.path.join(ROOT, rel))}"
    portal_css = f'<link rel="stylesheet" href="{v("assets/portal.css")}">\n'
    portal_js = ("portal-config.js", v("assets/vendor/supabase.js"), v("assets/portal-data.js"), v("assets/portal.js"))

    # pages import shell, so import them after the shell is configured
    import page_home as H
    import pages_a as A, pages_b as B, pages_c as C, pages_d as Dd, pages_e as E, pages_f as F

    PAGES = [
        # slug, title, description, body, nav item to highlight, extra <head>, noindex[, csp, scripts]
        ("index.html", "Home", "The AFIT Muslim Students’ Community (AMSC) at the Air Force Institute of Technology, Kaduna: building brotherhood and purpose through faith, and fostering academic excellence in Muslim students.", H.INDEX, "index.html", H.EXTRA_HEAD, False),
        ("about.html", "About AMSC", "Who the AFIT Muslim Students’ Community is: our mission, values, the meaning of our logo, and the committees that run the community.", A.ABOUT, None, "", False),
        ("programmes.html", "Programmes", "Islamiyyah, tutorials, IDIT digital skills training, the Sisters Circle, the annual Musabaqatul Qur’an, Da’wah Week and the Ramadan Lecture and Iftar.", A.PROGRAMMES, None, "", False),
        ("events.html", "Events", "The AMSC year: Freshers’ Orientation, IDIT, World Hijab Day, the Musabaqatul Qur’an, Ramadan, Eid and the FYB Sendforth Walimah.", B.EVENTS, None, "", False),
        ("executive.html", "Executive Committee", "What the AMSC Executive Committee does, and the nominees for the 1448 AH / 2026–2027 session, with roles, departments, levels and contacts.", E.EXECUTIVE, None, "", False),
        ("freshers.html", "Freshers’ guide", "AFIT freshers’ clearance and registration guide: documents to prepare, payments, the physical clearance route and who to call for help.", E.FRESHERS, None, "", False),
        ("gallery.html", "Gallery", "Photographs and flyers from AMSC programmes: lectures, the Musabaqatul Qur’an, orientation, sisters’ activities and community gatherings.", Dd.GALLERY, None, "", False),
        ("blog.html", "Blog", "Islamic reminders, community news, event reports and learning resources from the AFIT Muslim Students’ Community.", Dd.BLOG, None, "", False),
        ("contact.html", "Contact", "Email AMSC at " + D.EMAIL + ", join the WhatsApp Community, follow us on Instagram and Facebook, or find the right officer.", Dd.CONTACT, None, "", False),
        ("join.html", "Join AMSC", "Register with the AFIT Muslim Students’ Community to become a member and be added to the AMSC WhatsApp Community. Also: semester dues and volunteering.", A.JOIN, "", "", False),
        ("academics.html", "Academics", "Weekend tutorials, the past question bank, scholarships, attestation letters and exam-season support from AMSC.", B.ACADEMICS, "", "", False),
        ("salah.html", "Prayer times", "Today’s prayer times for Kaduna, jama’ah times at the AFIT Mosque and where to pray on campus.", B.SALAH, "", "", False),
        ("sisters.html", "Sisters", "The sisters’ wing of AMSC: the Sisters Circle, the online Ta’alim, World Hijab Day, welfare and leadership.", C.SISTERS, "", "", False),
        ("amanah.html", "Amanah Desk", "The AMSC Amanah Desk: the lost-and-found of the AFIT Muslim Students’ Community. Report a lost or found item, join the group or chat with the officer.", E.AMANAH, "", "", False),
        ("welfare.html", "Welfare", "Your AMSC welfare officers: chat with them on WhatsApp for help settling in and finding your way on campus.", C.WELFARE, "", "", False),
        ("library.html", "Library", "Islamiyyah notes, Qur’an resources, reading lists and the past question bank.", C.LIBRARY, "", "", False),
        ("give.html", "Give", "Semester dues, the welfare fund and named projects, with an account of how funds are used.", Dd.GIVE, "", "", False),
        ("alumni.html", "AMAN alumni network", "AMAN, the AFIT Muslim Alumni Network: register, mentor a student, share openings and give back.", Dd.ALUMNI, "", "", False),
        ("islamiyyah.html", "Islamiyyah", "AFIT Muslim Students’ Islamiyyah: weekend Qur’an (Musaffa, Tajweed and Hifz), Arabic and Islamic book studies at the AFIT Mosque, Saturdays and Sundays, 9:00am to 12:30pm.", F.ISLAMIYYAH, "programmes.html", "", False),
        ("portal.html", "Islamiyyah Student Portal", "Log in to the AMSC Islamiyyah Student Portal: Qur’an progress, books and notes, classes, teachers and announcements.", F.PORTAL, "", portal_css, True, PORTAL_CSP, portal_js),
        ("404.html", "Page not found", "This page could not be found.", E.NOT_FOUND, "", '<base href="/">\n', True),
    ]

    html_all = []
    for slug, title, desc, body, current, extra, noindex, *more in PAGES:
        csp, scripts = (more + [None, ()])[:2]
        html = shell.page(slug, title, desc, body, current=current, extra_head=extra, noindex=noindex,
                          csp=csp, scripts=scripts)
        with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
            f.write(html)
        html_all.append(html)

    # retire the old file names (Netlify serves _redirects first)
    for old in ("media.html", "press.html", "thanks.html"):
        p = os.path.join(ROOT, old)
        if os.path.exists(p):
            os.remove(p)

    fonts(html_all + [open(os.path.join(ROOT, "assets", "portal-data.js"), encoding="utf-8").read()])
    netlify_files([p for p in PAGES if not p[6]])
    print(f"built {len(PAGES)} pages -> {ROOT}")


def fonts(html_all):
    os.makedirs(FONTS_OUT, exist_ok=True)
    shutil.copy(os.path.join(FONTS_SRC, "dm-sans-latin-wght-normal.woff2"),
                os.path.join(FONTS_OUT, "dm-sans-latin-wght.woff2"))
    # Arabic: keep only the characters the site actually uses
    text = "".join(html_all)
    chars = sorted({c for c in text if 0x0600 <= ord(c) <= 0x06FF or 0xFB50 <= ord(c) <= 0xFEFF or ord(c) in (0x200C, 0x200D)})
    chars += [chr(0x0640), "،", " "]
    from fontTools import subset
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    font = subset.load_font(os.path.join(FONTS_SRC, "noto-kufi-arabic-arabic-wght-normal.woff2"), opts)
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(chars))
    sub.subset(font)
    subset.save_font(font, os.path.join(FONTS_OUT, "noto-kufi-arabic-subset.woff2"), opts)
    for lic in ("DM-Sans-OFL.txt", "Noto-Kufi-Arabic-OFL.txt"):
        shutil.copy(os.path.join(FONTS_SRC, lic), os.path.join(FONTS_OUT, lic))


PORTAL_CSP = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://api.fontshare.com; "
              "font-src 'self' https://cdn.fontshare.com; img-src 'self' data: blob:; "
              "connect-src 'self' https://*.supabase.co wss://*.supabase.co https://api.aladhan.com; "
              "object-src 'none'; base-uri 'self'; form-action 'self'; frame-src 'none'")

PORTAL_CONFIG = """// Islamiyyah Student Portal: connection to the Supabase database.
// Paste the two values from Supabase > Project Settings > API (or "Connect")
// between the quotes, then save. Both are safe to publish: the database's
// security rules decide who can see what.
window.AMSC_PORTAL = {
  supabaseUrl: "",   // looks like https://abcdefghijkl.supabase.co
  supabaseKey: "",   // the "anon public" or "publishable" key
  emailReset: false  // change to true only after setting up email (custom SMTP) in Supabase
};
"""


def portal_files():
    """Data the portal needs (surahs, juz, timetable), the surah list inside setup.sql,
    and a blank portal-config.js the first time."""
    import json, quran
    data = {
        "surahs": [list(x) for x in quran.SURAHS],
        "juz": [list(x) for x in quran.JUZ_STARTS],
        "timetable": [{"day": d, "start": a, "end": b, "title": t, "note": w} for d, a, b, t, w in D.ISLAMIYYAH_TIMETABLE],
        "venue": D.ISLAMIYYAH_VENUE,
        "books": [{"ar": a, "en": t, "subject": sj, "about": ab} for a, t, sj, ab in D.ISLAMIYYAH_BOOKS],
        "helpWa": D.portal_help_wa(),
    }
    with open(os.path.join(ROOT, "assets", "portal-data.js"), "w", encoding="utf-8") as f:
        f.write("/* Generated by _source/build.py from data.py and quran.py. Do not edit by hand. */\n")
        f.write("window.AMSC_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    cfg = os.path.join(ROOT, "portal-config.js")
    if not os.path.exists(cfg):
        with open(cfg, "w", encoding="utf-8") as f:
            f.write(PORTAL_CONFIG)
    sql_path = os.path.join(HERE, "portal", "setup.sql")
    sql = open(sql_path, encoding="utf-8").read()
    q = lambda t: "'" + t.replace("'", "''") + "'"
    rows = ",\n".join(f"  ({n}, {q(tr)}, {q(en)}, {q(a)}, {ay})" for n, tr, en, a, ay in quran.SURAHS)
    block = ("-- BEGIN SURAHS (written by _source/build.py from _source/quran.py)\n"
             "insert into public.surahs (number, name, meaning, name_ar, ayahs) values\n" + rows +
             "\non conflict (number) do update set name = excluded.name, meaning = excluded.meaning,\n"
             "  name_ar = excluded.name_ar, ayahs = excluded.ayahs;\n-- END SURAHS")
    sql = re.sub(r"-- BEGIN SURAHS.*?-- END SURAHS", lambda m: block, sql, flags=re.S)
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write(sql)


def netlify_files(pages):
    today = date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{D.SITE_URL}/{'' if s == 'index.html' else s}</loc><lastmod>{today}</lastmod></url>"
        for s, *_ in pages)
    w = lambda name, txt: open(os.path.join(ROOT, name), "w", encoding="utf-8").write(txt)
    w("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    w("robots.txt", f"User-agent: *\nDisallow: /_source/\nSitemap: {D.SITE_URL}/sitemap.xml\n")
    w("site.webmanifest", '{\n  "name": "AFIT Muslim Students’ Community",\n  "short_name": "AMSC",\n'
      '  "start_url": "/",\n  "display": "standalone",\n  "background_color": "#ffffff",\n  "theme_color": "#0056CE",\n'
      '  "icons": [\n    {"src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},\n'
      '    {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}\n  ]\n}\n')
    # CSS and JS are versioned (?v=hash) by build.py, so they can be cached for a year.
    # Images and fonts change name when they change, so the same applies.
    w("_headers", """# Netlify headers. Assets are fingerprinted or renamed when they change.
/assets/*
  Cache-Control: public, max-age=31536000, immutable
/*.html
  Cache-Control: public, max-age=0, must-revalidate
/
  Cache-Control: public, max-age=0, must-revalidate
/portal-config.js
  Cache-Control: public, max-age=0, must-revalidate
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()
""")
    w("_redirects", """# Old page names from the previous version of the site
/media.html      /gallery.html     301
/media           /gallery          301
/press.html      /blog.html        301
/press           /blog             301
/portal          /portal.html      200
# Keep the generator out of public view
/_source/*       /404.html         404
/netlify/*       /404.html         404
""")
    w("netlify.toml", """# Netlify settings for the AMSC site (written by _source/build.py).
# The site is already built (plain HTML), so Netlify only publishes this folder.
# To change content: edit files in _source/, run `python3 build.py` inside _source/,
# then commit and push. Netlify goes live automatically after each push.
[build]
  publish = "."
  command = ""

# netlify/functions/keepalive.mjs pings the portal database once a day so the
# free Supabase project is not paused for inactivity.
[functions]
  directory = "netlify/functions"
""")


if __name__ == "__main__":
    main()
