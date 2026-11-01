import json
import data as D
from shell import icon, img, ar, pill, ext, band, soon, person, mail_link

JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": D.ORG,
    "alternateName": D.SHORT,
    "url": D.SITE_URL + "/",
    "logo": D.SITE_URL + "/assets/img/icon-512.png",
    "email": D.EMAIL,
    "slogan": D.TAGLINE_EN,
    "parentOrganization": {"@type": "CollegeOrUniversity", "name": "Air Force Institute of Technology",
                           "address": {"@type": "PostalAddress", "addressLocality": "Kaduna", "addressCountry": "NG"}},
    "sameAs": [D.IG, D.FB],
}, ensure_ascii=False)
EXTRA_HEAD = f'<script type="application/ld+json">{JSONLD}</script>\n'

values = "".join(f'<li>{pill(v, "mist")}</li>' for v, _ in D.VALUES)

lead = [D.holder("Ameer", "b"), D.holder("Ameerah", "s"), D.holder("Naibul", "b"), D.holder("Naibatul", "s")]
leaders = "".join(person(p, compact=True, show_wing=True) for p in lead)

INDEX = f'''
<section class="hero">
  <div class="wrap hero__inner">
    <div class="hero__copy">
      <p class="mb-0">{ar(D.TAGLINE_AR, "hero__ar")}</p>
      <span class="hero__en">{D.TAGLINE_EN}</span>
      <h1>Building brotherhood and purpose through faith</h1>
      <p class="hero__lede">A community helping Muslim students at the Air Force Institute of
      Technology grow in faith, character, academics and service.</p>
      <div class="actions">
        <a class="btn btn--yellow" href="{D.JOIN}">Join our community</a>
        <a class="btn btn--line-light" href="programmes.html">Explore our programmes</a>
      </div>
    </div>
    <div class="hero__media">
      <div class="hero__frame" aria-hidden="true"></div>
      <div class="arch hero__arch">{img("community-group", "Brothers and sisters of AMSC standing together on the AFIT campus", "(min-width: 960px) 480px, 92vw", eager=True)}</div>
      <a class="hero__note" href="freshers.html">
        <span class="hero__note-dot">{icon("cap")}</span>
        <span><b>New at AFIT?</b><span>Read the freshers&rsquo; clearance guide</span></span>
      </a>
    </div>
  </div>
</section>

<div class="strip">
  <div class="strip__inner">
    <span>Welcome to the {D.SESSION} session.</span>
    <a href="{D.JOIN}">Register to join the AMSC WhatsApp Community</a>
  </div>
</div>

<section class="section">
  <div class="wrap intro">
    <h2 class="statement"><span>One Ummah.</span><span>One Campus.</span></h2>
    <div>
      <p class="lede">The AFIT Muslim Students&rsquo; Community is a faith-driven body dedicated to
      fostering spiritual growth, unity and purpose among Muslim students at the Air Force
      Institute of Technology.</p>
      <p>Rooted in Islamic values and guided by sincerity, discipline, faith and brotherhood, we
      give students a place to grow in deen and character through worship, service, learning and
      positive impact on campus. We are more than a religious group: we help one another succeed
      academically, socially and personally.</p>
      <ul class="values">{values}</ul>
      <a class="link" href="about.html">Read about AMSC</a>
    </div>
  </div>
</section>

<section class="section section--tight" style="padding-top:0">
  <div class="wrap">
    <div class="sechead sechead--split">
      <h2>Faith, knowledge, skills and care</h2>
      <p class="lede">Our programmes cover four areas of student life. Each is run by its own
      team of student volunteers.</p>
    </div>
    <div class="areas">
      <article class="area area--photo">
        <div class="area__img">{img("quiz-mosque", "Students reciting the Qur'an in the mosque", "(min-width: 960px) 680px, 100vw")}</div>
        <div class="area__body">
          <h3>Faith and the Qur&rsquo;an</h3>
          <p>Weekly Islamiyya classes in Qur&rsquo;an, Arabic, Fiqh and Tawheed, a recitation
          circle, Da&rsquo;wah Week and the annual Musabaqatul Qur&rsquo;an.</p>
          <ul class="chips"><li>Islamiyya</li><li>Musaffa</li><li>Da&rsquo;wah Week</li><li>Musabaqatul Qur&rsquo;an</li></ul>
          <a class="link link--light" href="programmes.html#islamiyya">See faith programmes</a>
        </div>
      </article>
      <article class="area area--side">
        {icon("cap")}
        <h3>Academic excellence</h3>
        <p>Weekend tutorials taught by students who have passed the course, a shared past
        question bank, and study materials through our partnership with PDFNest.</p>
        <ul class="chips"><li>Tutorials</li><li>Past questions</li><li>PDFNest</li></ul>
        <a class="link" href="academics.html">Academic support</a>
      </article>
      <article class="area area--side area--yellow">
        {icon("chip")}
        <h3>Digital skills</h3>
        <p>IDIT, our Islamic Digital and IT Training, runs four-week online cohorts in AI, data
        analysis, graphic design and video editing. Beginners are welcome.</p>
        <ul class="chips"><li>AI Mastery</li><li>Data analysis</li><li>Design</li><li>Video</li></ul>
        <a class="link" href="programmes.html#idit">About IDIT</a>
      </article>
      <article class="area area--photo area--wide">
        <div class="area__img">{img("walimah-group", "AMSC members and guests at the FYB Sendforth Walimah, in front of the AFIT auditorium", "(min-width: 960px) 680px, 100vw", style="object-position:50% 88%")}</div>
        <div class="area__body">
          <h3>Sisterhood, brotherhood and care</h3>
          <p>The Sisters Circle, sports, the Ramadan Lecture and Iftar, and welfare officers who
          help students settle in and find their way.</p>
          <ul class="chips"><li>Sisters Circle</li><li>Ramadan Lecture and Iftar</li><li>Welfare</li></ul>
          <a class="link link--light" href="programmes.html">All programmes</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section section--tight" style="padding-top:0">
  <div class="wrap">
    <div class="partner-strip">
      <div class="partner-strip__img">{img("flyer-pdfnest", "Partnership announcement: PDFNest and the AFIT Muslim Students' Community", "(min-width: 960px) 220px, 40vw")}</div>
      <div class="partner-strip__copy">
        <p class="kicker">{pill("Official partner")}</p>
        <h2>PDFNest Students Hub</h2>
        <p>Exam-recommended PDFs, quick polls and important academic updates. Study smarter. Stay informed. Prepare better.</p>
        <div class="actions">
          <a class="btn btn--blue" href="{D.PDFNEST_URL}" target="_blank" rel="noopener">Join PDFNest{icon("external")}<span class="sr-only"> (opens in a new tab)</span></a>
          <a class="btn btn--green" href="{D.PDFNEST_WA}" target="_blank" rel="noopener">{icon("whatsapp")}Get PDFNest Group Access<span class="sr-only"> (opens WhatsApp)</span></a>
          <a class="link" href="academics.html#pdfnest">About the partnership</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap split split--center">
    <div>
      <h2>Led by students, for students</h2>
      <p class="lede">The Executive Committee plans the session, oversees our programmes and
      makes sure AMSC&rsquo;s goals are carried out.</p>
      <p>Its members are students who give their time and skills alongside their own studies,
      across a brothers&rsquo; wing and a sisters&rsquo; wing.</p>
      <p class="kicker">{pill("Nominees")} {D.SESSION} session</p>
      <a class="btn btn--blue" href="executive.html">Meet the Executive Committee</a>
    </div>
    <ul class="leaders">{leaders}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sechead sechead--split">
      <h2>Latest updates</h2>
      <p class="lede">News, reminders, student articles and event reports from the community.</p>
    </div>
    <div class="soon">
      {pill("Coming soon", "green")}
      <h3>Our publications and updates will be available soon.</h3>
      <p>Until then, reminders and recaps are on the blog, and announcements go out on
      Instagram and the AMSC WhatsApp Community.</p>
      <div class="actions mt-m">
        <a class="btn btn--blue" href="blog.html">Read Blog</a>
        {ext(D.IG, f"Follow {D.IG_HANDLE} on Instagram", "link")}
      </div>
    </div>
  </div>
</section>

{band("Be part of AMSC this session",
      f"Register once to become a member and join the AMSC WhatsApp Community, or write to us at {D.EMAIL}.",
      (D.JOIN, "Join our community"), ("contact.html", "Contact us"))}
'''
