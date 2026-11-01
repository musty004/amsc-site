import data as D
import shell
from shell import icon, img, ar, pill, ext, band, pagehead, person, mail_link

# ================================================================== EXECUTIVE
def wing(title, people):
    if not people:
        return ""
    items = "".join(person(p) for p in people)
    return f'<div class="wing"><h4>{pill(title, "mist")}</h4><ul class="people">{items}</ul></div>'

blocks = []
for key, name, desc in D.PORTFOLIOS:
    b = [p for p in D.BROTHERS if p[5] == key]
    s = [p for p in D.SISTERS if p[5] == key]
    single = " wings--single" if not (b and s) else ""
    blocks.append(f'''<section class="portfolio" id="{key}" aria-labelledby="{key}-h">
  <div><h3 id="{key}-h">{name}</h3><p>{desc}</p></div>
  <div class="wings{single}">{wing("Brothers&rsquo; wing", b)}{wing("Sisters&rsquo; wing", s)}</div>
</section>''')
ROSTER = "\n".join(blocks)
JUMP = "".join(f'<li><a href="#{k}">{n}</a></li>' for k, n, _ in D.PORTFOLIOS)

EXECUTIVE = pagehead("Executive Committee",
  f"The students who lead AMSC for the {D.SESSION} session, and what each portfolio is responsible for.") + f'''
<section class="section">
  <div class="wrap split">
    <div>
      <h2>What the Executive Committee does</h2>
      <p class="lede">The Executive Committee provides leadership and coordination for AMSC. It plans
      the session, oversees our programmes, guides decisions and makes sure the community&rsquo;s
      goals are carried out.</p>
      <p>It is made up of students who give their time, skills and commitment alongside their
      studies, across a brothers&rsquo; wing led by the Ameer and a sisters&rsquo; wing led by the
      Ameerah. Most portfolios have an officer on each side, so every member has someone to go to.</p>
      <ul class="meta">
        <li>{icon("calendar")}Plans the session&rsquo;s programmes and calendar</li>
        <li>{icon("shield")}Represents AMSC to the Institute and seeks approval for programmes</li>
        <li>{icon("users")}Coordinates the committees and volunteers who run each programme</li>
        <li>{icon("pen")}Keeps the records, the accounts and the membership register</li>
        <li>{icon("heart")}Looks after the welfare of members, especially new students</li>
      </ul>
    </div>
    <figure class="mt-0">
      <div class="framed">{img("walimah-group", "AMSC members and invited guests at the FYB Sendforth Walimah, in front of the AFIT auditorium", "(min-width: 960px) 560px, 100vw")}</div>
      <figcaption class="note">Members and guests at the FYB Sendforth Walimah.</figcaption>
    </figure>
  </div>
</section>

<section class="section section--mist" id="roster">
  <div class="wrap">
    <div class="sechead sechead--split">
      <div>
        <p class="kicker">{pill("Nominees")} {D.SESSION} session</p>
        <h2>The Executive Council</h2>
        <p class="lede mb-0">{len(D.BROTHERS) + len(D.SISTERS)} nominees: {len(D.BROTHERS)} in the brothers&rsquo;
        wing and {len(D.SISTERS)} in the sisters&rsquo; wing, grouped by portfolio.</p>
      </div>
      <p class="muted">Short biographies and photographs will be added as they are approved. Tap a
      number to call.</p>
    </div>
    <nav class="jump" aria-label="Portfolios"><ul>{JUMP}</ul></nav>
    {ROSTER}
  </div>
</section>

{band("Questions for the committee?",
      f"Write to {D.EMAIL}, or find the right officer for what you need on the contact page.",
      ("mailto:" + D.EMAIL, "Email AMSC"), ("contact.html", "Who to ask"))}
'''

# ================================================================== FRESHERS
checklist = "".join(
    f'<li><label><input type="checkbox" id="prep-{i}"><span>{t}</span></label></li>'
    for i, t in enumerate(D.FRESHER_PREP, 1))
payments = "".join(f"<li><b>{h}</b><span>{t}</span></li>" for h, t in D.FRESHER_PAYMENT)
route = "".join(f"<li><h3>{h}</h3><p>{t}</p></li>" for h, t in D.FRESHER_ROUTE)
welfare_people = "".join([
    person(D.holder("Welfare Officer I", "b"), show_wing=True, whatsapp=D.officer_wa("Welfare Officer I", "b")),
    person(D.holder("Welfare Officer II", "s"), show_wing=True, whatsapp=D.officer_wa("Welfare Officer II", "s")),
    person(D.holder("Asst. Welfare Officer I", "b"), show_wing=True),
    person(D.holder("Asst. Welfare Officer II", "s"), show_wing=True)])

def ophoto(name, alt, caption, pos=None):
    st = f"object-position:{pos}" if pos else ""
    return f'<figure class="photo">{img(name, alt, "(min-width: 960px) 560px, (min-width: 640px) 50vw, 100vw", style=st)}<figcaption>{caption}</figcaption></figure>'

FRESHERS = f'''<section class="pagehead">
  <div class="wrap pagehead__inner">
    <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span>Freshers&rsquo; guide</nav>
    <p class="pagehead__ar">{ar("السلام عليكم ورحمة الله وبركاته")}</p>
    <h1>Freshers&rsquo; guide</h1>
    <p class="pagehead__lede">Assalamu alaikum warahmatullah wabarakatuh, dear AFIT freshers! As you
    step onto campus for this exciting new chapter, we pray your journey and clearance go with
    absolute ease. This page has everything you need for clearance, your first weeks, and the people
    to call when you need help.</p>
    <div class="actions mt-m no-print">
      <a class="btn btn--yellow" href="#clearance">Start the clearance guide</a>
      <button class="btn btn--line-light" type="button" data-share="AFIT freshers' guide from AMSC">{icon("share")}Share this guide</button>
      <button class="btn btn--line-light" type="button" data-print>{icon("printer")}Print or save as PDF</button>
    </div>
    <p class="share-status share-status--light" id="share-status" role="status"></p>
    <nav class="jump jump--light no-print" aria-label="On this page"><ul>
      <li><a href="#orientation">Orientation</a></li>
      <li><a href="#clearance">Clearance checklist</a></li>
      <li><a href="#route">Clearance route</a></li>
      <li><a href="#places">Places to know</a></li>
      <li><a href="#help">Who to call</a></li>
      <li><a href="#questions">Questions</a></li>
    </ul></nav>
  </div>
</section>

<section class="section" id="orientation">
  <div class="wrap">
    <div class="sechead">
      <h2>Freshers&rsquo; Orientation</h2>
      <p class="lede">Every session opens with an orientation for new Muslim students: you meet the
      community, learn where to pray between lectures, receive an academic survival guide and are
      paired with a senior student.</p>
    </div>

    <div class="year">
      <div class="year__head">
        {pill("2025/1447")}
        <h3>Navigating campus, guided by Islam in every step</h3>
        <p>Held on Saturday 8 November 2025, 9:00am to 12:00pm, at Mosugu Hall.</p>
      </div>
      <div class="photos">
        {ophoto("orientation-2025-sisters", "New sisters listening at the 2025/1447 Freshers' Orientation", "Sisters at the 2025/1447 orientation")}
        {ophoto("orientation-2025-brothers", "New brothers seated in the hall at the 2025/1447 Freshers' Orientation", "Brothers at the 2025/1447 orientation")}
        {ophoto("orientation-2025-hall", "Brothers listening to a talk at the 2025/1447 Freshers' Orientation", "Taking in the talks")}
      </div>
      <div class="actions mt-s">{ext(D.ALBUM_ORIENTATION_2025, "See all 2025/1447 photos", "btn btn--blue")}</div>
    </div>

    <div class="year">
      <div class="year__head">
        {pill("2024/1446")}
        <h3>Freshers&rsquo; Orientation, 2024/1446 session</h3>
        <p>New brothers and sisters at the orientation in the lecture hall.</p>
      </div>
      <div class="photos photos--2">
        {ophoto("orientation-2024-sisters", "New sisters seated in the lecture hall at the 2024/1446 Freshers' Orientation", "Sisters at the 2024/1446 orientation")}
        {ophoto("orientation-2024-brothers", "New brothers seated in the lecture hall at the 2024/1446 Freshers' Orientation", "Brothers at the 2024/1446 orientation")}
        {ophoto("orientation-2024-hall", "A full lecture hall of brothers and sisters at the 2024/1446 Freshers' Orientation", "A full hall for the 2024/1446 orientation")}
        {ophoto("orientation-2024-front", "Brothers listening at the 2024/1446 Freshers' Orientation", "Listening to the orientation talks")}
      </div>
    </div>
  </div>
</section>

<section class="section section--mist" id="clearance">
  <div class="wrap split">
    <div>
      <h2>Prepare these before you go</h2>
      <p>Tick each one off as you get it ready. Your ticks are saved on this phone or computer.</p>
      <ul class="checklist">{checklist}</ul>
      <p class="note checklist__count" id="checklist-count" aria-live="polite"></p>
    </div>
    <div class="notice notice--alert">{icon("alert")}<div>
      <h3>Avoid a common delay</h3>
      <p>Check that the name on your <strong>JAMB CAPS</strong> matches the name on your
      <strong>O&rsquo;Level results</strong>.</p>
      <p>If there is a mismatch, get it corrected early at any JAMB CBT centre, before you start
      clearance.</p>
    </div></div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      <h2>Payment and verification</h2>
      <p class="lede">Do these in order, before you start the physical clearance route.</p>
    </div>
    <ol class="steps">{payments}</ol>
  </div>
</section>

<section class="section section--blue" id="route">
  <div class="wrap">
    <div class="sechead">
      <h2>Your physical clearance route</h2>
      <p class="lede">Three stops, in this order. Carry your stamped receipts and all four sets of
      documents with you.</p>
    </div>
    <ol class="route">{route}</ol>
  </div>
</section>

<section class="section" id="places">
  <div class="wrap">
    <div class="sechead">
      <h2>Places to know</h2>
      <p class="lede">Where you will go for clearance, for prayer and for the community.</p>
    </div>
    <div class="grid grid--3">
      <div class="card">{icon("briefcase")}<h3>Bursary Unit</h3><p>First clearance stop. Your printed payment receipts are verified and stamped here.</p></div>
      <div class="card">{icon("book")}<h3>Academic Branch</h3><p>Second stop. Submit your four complete sets of documents.</p></div>
      <div class="card">{icon("cap")}<h3>Your department</h3><p>Final stop. Complete your registration with the Departmental Officer.</p></div>
      <div class="card">{icon("mosque")}<h3>AFIT Mosque</h3><p>Daily congregational prayers, weekend Islamiyya classes and the Friday Sisters Circle.</p></div>
      <div class="card">{icon("arch")}<h3>NAF Base Central Mosque</h3><p>Where we pray Jumu&rsquo;ah, beside the NAF Hospital.</p></div>
      <div class="card">{icon("star")}<h3>Air Force Primary School</h3><p>Where Eid prayers are usually held. The time is announced by the Imam at the Base Mosque.</p></div>
    </div>
    <p class="note">Full prayer times and locations are on the <a href="salah.html">prayer times page</a>.</p>
  </div>
</section>

<section class="section section--mist" id="help">
  <div class="wrap">
    <div class="sechead sechead--split">
      <div>
        <h2>Stuck? Call a welfare officer</h2>
        <p class="lede mb-0">The welfare officers are available to help newly admitted students with
        day-to-day life in the school environment, to the best of their capacity.</p>
      </div>
      <div class="card">
        <h3>Join the AMSC WhatsApp Community</h3>
        <p>Announcements, academic updates, clearance guides and peer support. Register once and you will be added.</p>
        <div class="card__foot"><a class="btn btn--blue btn--sm" href="{D.JOIN}">Register to join</a></div>
      </div>
    </div>
    <ul class="people grid grid--2">{welfare_people}</ul>
    <div class="grid grid--2 mt-m">
      <div class="card">
        {icon("compass")}
        <h3>Lost something during clearance?</h3>
        <p>Report it to the Amanah Desk, the AMSC lost-and-found. Found something? Report that too, so it gets back to its owner.</p>
        <div class="card__foot"><a class="link" href="amanah.html">Go to the Amanah Desk</a></div>
      </div>
      <div class="card">
        {icon("book")}
        <h3>Need study materials?</h3>
        <p>Through our partnership with PDFNest, you get exam-recommended PDFs, quick polls and academic updates.</p>
        <div class="card__foot"><a class="link" href="academics.html#pdfnest">About PDFNest</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sechead">
      <h2>Your first weeks</h2>
      <p class="lede">Once clearance is done, this is where the community meets.</p>
    </div>
    <div class="grid grid--4">
      <a class="card" href="salah.html">{icon("mosque")}<h3>Where to pray</h3><p>Prayer times, jama&rsquo;ah times and where we pray daily, on Fridays and on Eid.</p></a>
      <a class="card" href="programmes.html#timetable">{icon("calendar")}<h3>Weekly programmes</h3><p>Islamiyya, tutorials and the Sisters Circle, with days and venues.</p></a>
      <a class="card" href="academics.html">{icon("cap")}<h3>Academic support</h3><p>Tutorials taught by senior students, past questions and PDFNest.</p></a>
      <a class="card" href="{D.JOIN}">{icon("users")}<h3>Join AMSC</h3><p>Register as a member and get every announcement.</p></a>
    </div>
  </div>
</section>

<section class="section section--mist" id="questions">
  <div class="wrap split">
    <div>
      <h2>Freshers&rsquo; questions</h2>
      <p class="lede">The questions new students ask us most.</p>
    </div>
    <div>
      <details class="faq"><summary>Where do we pray Jumu&rsquo;ah?</summary><p>At the {D.JUMUAH_PLACE}.</p></details>
      <details class="faq"><summary>Where do I pray between lectures?</summary><p>The AFIT Mosque holds all five daily prayers in congregation, and the Male Hostel Mosque is closest for brothers in the hostel. See the <a href="salah.html">prayer times page</a> for jama&rsquo;ah times.</p></details>
      <details class="faq"><summary>How do I join AMSC and the WhatsApp Community?</summary><p>Fill in the <a href="{D.JOIN}">registration form</a>. An AMSC admin adds you to the WhatsApp Community with the number you give.</p></details>
      <details class="faq"><summary>Who can help me if I get stuck during clearance?</summary><p>Message or call a welfare officer. Their numbers are <a href="#help">above</a>.</p></details>
      <details class="faq"><summary>I lost an item. What do I do?</summary><p>Report it to the <a href="amanah.html">Amanah Desk</a>, the AMSC lost-and-found.</p></details>
      <details class="faq"><summary>Are there tutorials for 100 level?</summary><p>Yes. Weekend tutorials cover first-year courses such as general mathematics and chemistry. The timetable for this session will be published on the <a href="academics.html">academics page</a>.</p></details>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="band">
      <div class="band__copy">
        <h2>Save this guide and share it with your course mates</h2>
        <p>Keep everyone guided. The same guide is on our Instagram.</p>
      </div>
      <div class="band__actions no-print">
        <button class="btn btn--yellow" type="button" data-share="AFIT freshers' guide from AMSC">{icon("share")}Share this guide</button>
        {ext(D.IG_FRESHERS_POST, "View the Instagram post", "btn btn--line-light")}
      </div>
    </div>
    <p class="note">This guide reflects the process shared by AMSC for the {D.SESSION} session. If the
    Institute issues different instructions, follow the Institute.</p>
  </div>
</section>
'''

# ================================================================== AMANAH DESK
AMANAH = pagehead("Amanah Desk",
  "The official lost-and-found of the AFIT Muslim Students&rsquo; Community. Lost something? Found "
  "something? We help it get back to its owner.") + f'''
<section class="section">
  <div class="wrap split">
    <div>
      <p class="kicker">As-salāmu alaykum wa rahmatullāhi wa barakātuh, brothers and sisters.</p>
      <h2>Every item found is a trust</h2>
      <p class="lede">The Amanah Desk is where members report items they have lost or found, so each
      one can be recorded properly and returned to the person it belongs to.</p>
      <p>Our work is guided by the Islamic principle of <strong>amanah</strong>, trustworthiness. When
      you find something that is not yours, it becomes a responsibility, and returning it to its owner
      is an act of honesty and integrity.</p>
      <p>Whether you have lost something or found something that belongs to someone else, the Amanah
      Desk is here to help.</p>
    </div>
    <div class="amanah-quote">
      <p class="amanah-quote__ar">{ar("إِنَّ اللَّهَ يَأْمُرُكُمْ أَنْ تُؤَدُّوا الْأَمَانَاتِ إِلَىٰ أَهْلِهَا")}</p>
      <blockquote><p>&ldquo;Indeed, Allah commands you to render trusts to whom they are due.&rdquo;</p></blockquote>
      <p class="amanah-quote__ref">Surah An-Nisa 4:58</p>
      <p class="amanah-quote__motto">Post respectfully. Help sincerely. Return what is entrusted to you.</p>
    </div>
  </div>
</section>

<section class="section section--mist" id="access">
  <div class="wrap">
    <div class="sechead">
      <h2>Two ways to reach the Amanah Desk</h2>
      <p class="lede">Join the group to see and post lost and found items, or speak to the officer privately.</p>
    </div>
    <div class="options">
      <article class="option">
        {pill("Option 1")}
        <h3>Join the Amanah Desk group</h3>
        <p>The Amanah Desk has its own WhatsApp group where lost and found items are posted. The group
        is for AMSC members, so you need to <strong>register as an AMSC member</strong> before you can
        request access.</p>
        <ol class="steps steps--compact">
          <li><b>Register as an AMSC member</b><span>Fill in the registration form on this website.</span></li>
          <li><b>Request access to the group</b><span>In the last box of the form, write &ldquo;Please add me to the Amanah Desk group&rdquo;, or message the officer after you register.</span></li>
          <li><b>You are added</b><span>The desk adds you using the number you registered with.</span></li>
        </ol>
        <div class="actions"><a class="btn btn--blue" href="{D.JOIN}">Register as an AMSC Member</a></div>
      </article>
      <article class="option option--green">
        {pill("Option 2")}
        <h3>Chat with the Amanah Desk Officer</h3>
        <p>Prefer to speak to someone privately? Message the Amanah Desk Officer directly on WhatsApp to
        report a lost or found item, or to arrange a handover.</p>
        <p class="option__number">{icon("whatsapp")}{D.AMANAH_DISPLAY}</p>
        <div class="actions"><a class="btn btn--green" href="{D.AMANAH_WA}" target="_blank" rel="noopener">{icon("whatsapp")}Chat with the Amanah Desk Officer<span class="sr-only"> (opens WhatsApp)</span></a></div>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sechead">
      <h2>How to report an item</h2>
      <p class="lede">A clear report is the fastest way to reunite an item with its owner.</p>
    </div>
    <div class="grid grid--2">
      <div class="card">
        {icon("compass")}
        <h3>If you lost something</h3>
        <ul class="meta">
          <li>{icon("check")}What the item is, with its colour, brand and any marks that make it yours</li>
          <li>{icon("check")}Where and when you last had it</li>
          <li>{icon("check")}A photo of the item, if you have one</li>
          <li>{icon("check")}The best number to reach you</li>
        </ul>
      </div>
      <div class="card">
        {icon("shield")}
        <h3>If you found something</h3>
        <ul class="meta">
          <li>{icon("check")}Keep it safe and report it as soon as you can</li>
          <li>{icon("check")}Say what it is and where and when you found it</li>
          <li>{icon("check")}Hold back a detail or two, so the owner can describe it and confirm it is theirs</li>
          <li>{icon("check")}Never post ID numbers, bank card details or the contents of a phone</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="band">
      <div class="band__copy">
        <h2>May Allah reward your honesty</h2>
        <p>And make us among those who fulfil their trusts. Jazākumullāhu khayran.</p>
      </div>
      <div class="band__actions">
        <a class="btn btn--yellow" href="{D.JOIN}">Register as an AMSC Member</a>
        <a class="btn btn--line-light" href="{D.AMANAH_WA}" target="_blank" rel="noopener">Chat with the officer<span class="sr-only"> (opens WhatsApp)</span></a>
      </div>
    </div>
  </div>
</section>
'''

# ================================================================== 404
NOT_FOUND = f'''<section class="pagehead">
  <div class="wrap pagehead__inner">
    <h1>We could not find that page</h1>
    <p class="pagehead__lede">It may have moved when the site was updated. These pages are the most
    visited:</p>
    <div class="actions mt-m">
      <a class="btn btn--yellow" href="index.html">Home</a>
      <a class="btn btn--line-light" href="freshers.html">Freshers&rsquo; guide</a>
      <a class="btn btn--line-light" href="executive.html">Executive Committee</a>
      <a class="btn btn--line-light" href="contact.html">Contact</a>
    </div>
  </div>
</section>'''
