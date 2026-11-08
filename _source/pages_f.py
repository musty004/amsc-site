"""The Islamiyyah programme page and the Student Portal page."""
import data as D
from shell import icon, img, ar, pill, ext, band, pagehead

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def t12(t):
    h, m = map(int, t.split(":"))
    return f"{h % 12 or 12}:{m:02d}{'am' if h < 12 else 'pm'}"


rows = "".join(
    f'<tr><td>{DAYS[d]}</td><td>{t12(a)} to {t12(b)}</td><td>{title}</td><td>{who}</td></tr>'
    for d, a, b, title, who in D.ISLAMIYYAH_TIMETABLE)

books = "".join(
    f'<li><span class="book-ar">{ar(a)}</span><strong>{t}</strong><span class="book-sub">{subj}</span>'
    f'<span class="book-about">An introduction to {about}.</span></li>'
    for a, t, subj, about in D.ISLAMIYYAH_BOOKS)

ISLAMIYYAH = pagehead(
    "Islamiyyah",
    "Weekend Islamic education for AFIT students: Qur&rsquo;an, Arabic and Islamic book studies, "
    "taught by students for students.") + f'''
<section class="section">
  <div class="wrap split split--sidebar">
    <div>
      <p class="kicker">{pill("2026/2027 session")} Prepared by the Islamiyyah Committee</p>
      <h2>Learn, improve and strengthen your connection with Islam</h2>
      <p class="lede">The Islamiyyah gives students structured Qur&rsquo;anic, Arabic and Islamic
      studies alongside their regular academic work.</p>
      <p>Improve your recitation and memorisation, build your Arabic, and study foundational texts
      on belief, worship and the life of the Prophet &#xFDFA;. Classes are grouped by ability, so
      a complete beginner and a student completing their Hifz both learn at the right level.</p>
      <ul class="meta">
        <li>{icon("calendar")}{D.ISLAMIYYAH_DAYS}</li>
        <li>{icon("clock")}{D.ISLAMIYYAH_HOURS}</li>
        <li>{icon("pin")}{D.ISLAMIYYAH_VENUE}</li>
      </ul>
      <div class="actions">
        <a class="btn btn--blue" href="{D.PORTAL}">Student Portal</a>
        {ext(D.portal_help_wa(), "Ask the Mudeer a question", "link")}
      </div>
    </div>
    <figure class="framed islamiyyah-flyer">{img("flyer-islamiyyah", "Islamiyyah classes are back: Qur’an recitation, revision, Arabic, Hadith and Islamic studies, Saturdays and Sundays, 9:00am to 12:30pm, AFIT Mosque", "(min-width: 960px) 400px, 92vw")}</figure>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="grid grid--2">
      <article class="card">{icon("star")}<h3>Vision</h3>
        <p>To develop students with strong Qur&rsquo;anic knowledge, sound Arabic ability,
        understanding of Islamic teachings, and excellent character.</p></article>
      <article class="card">{icon("compass")}<h3>Mission</h3>
        <p>To provide consistent weekend Islamic education through Qur&rsquo;an, Tajweed, Hifz,
        Arabic, Aqeedah, Fiqh, Seerah and Islamic studies, while encouraging discipline, good
        manners, responsibility, peer learning and continuous personal improvement.</p></article>
    </div>
  </div>
</section>

<section class="section section--tight" id="timetable">
  <div class="wrap">
    <div class="sechead">
      <h2>Weekend timetable</h2>
      <p class="lede">Every class holds at the {D.ISLAMIYYAH_VENUE}.</p>
    </div>
    <div class="table-wrap">
      <table class="table table--times">
        <thead><tr><th scope="col">Day</th><th scope="col">Time</th><th scope="col">Session</th><th scope="col">Who</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="grid grid--2">
      <article class="card">{icon("quran")}<h3>Qur&rsquo;an: Musaffa, Tajweed and Hifz</h3>
        <p>Saturday and Sunday, 9:00 to 11:00am. Sessions cover recitation, Tajweed, memorisation
        and revision, and follow each student&rsquo;s progress.</p>
        <ul class="levels">
          <li><strong>Beginner</strong><span>Foundational Qur&rsquo;an reading and basic improvement</span></li>
          <li><strong>Intermediate</strong><span>Continued memorisation, recitation and Tajweed</span></li>
          <li><strong>Advanced / Hifz</strong><span>Higher-level memorisation, revision and recitation</span></li>
        </ul></article>
      <article class="card">{icon("pen")}<h3>Arabic Language</h3>
        <p>Saturday, 11:00am to 12:30pm, using {ar(D.ARABIC_TEXT[0])} ({D.ARABIC_TEXT[1]}). The aim
        is functional Arabic that opens up Islamic texts.</p>
        <ul class="levels">
          <li><strong>Beginner</strong><span>Basic Arabic language</span></li>
          <li><strong>Intermediate</strong><span>Reading, comprehension and language development</span></li>
          <li><strong>Advanced</strong><span>Higher-level Arabic and engagement with Islamic learning</span></li>
        </ul></article>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="sechead">
      <h2>Islamic Book Studies</h2>
      <p class="lede">Sunday, 11:00am to 12:30pm. Unlike the Qur&rsquo;an and Arabic classes, all
      students gather together. The texts rotate flexibly through the session.</p>
    </div>
    <ul class="books">{books}</ul>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap split split--center">
    <div>
      <h2>Taught by students, for students</h2>
      <p class="lede">AMSC students teach and coordinate the Islamiyyah themselves.</p>
      <p>Those who have learned share beneficial knowledge, support fellow students in their
      Qur&rsquo;an, help those who need extra guidance, and grow in confidence presenting Islamic
      knowledge. If you can help teach, tell the Mudeer.</p>
      <div class="actions">{ext(D.portal_help_wa(), "Offer to help teach", "link")}</div>
    </div>
    <blockquote class="hadith">
      <p class="hadith__ar">{ar("مَنْ سَلَكَ طَرِيقًا يَلْتَمِسُ فِيهِ عِلْمًا، سَهَّلَ اللَّهُ لَهُ بِهِ طَرِيقًا إِلَى الْجَنَّةِ")}</p>
      <p>&ldquo;Whoever follows a path in pursuit of knowledge, Allah will make easy for him a path
      to Paradise.&rdquo;</p>
      <footer>Sahih Muslim 2699</footer>
    </blockquote>
  </div>
</section>

{band("The Islamiyyah Student Portal",
      "Log in to track your Qur’an memorisation and revision, download books and notes, see your class, teachers and timetable, and read announcements. New students create an account, and the committee approves it.",
      (D.PORTAL, "Log in or create an account"), (D.portal_help_wa(), "Get help on WhatsApp"))}
'''


PORTAL = f'''
<div class="portal-head">
  <div class="wrap portal-head__inner">
    <div><h1>Islamiyyah Student Portal</h1><p>Qur&rsquo;an progress, books and notes, classes and announcements.</p></div>
    <a href="islamiyyah.html">About the Islamiyyah</a>
  </div>
</div>
<div class="portal-wrap">
  <div class="wrap">
    <div id="portal" aria-busy="true">
      <div class="pt-loading" role="status"><span class="pt-spin" aria-hidden="true"></span>Opening the portal&hellip;</div>
      <noscript><div class="pt-auth"><div class="pt-auth__card"><h2>JavaScript is needed</h2>
        <p>The Student Portal needs JavaScript. Turn it on in your browser settings, or use another browser.</p></div></div></noscript>
    </div>
    <p id="portal-live" class="sr-only" aria-live="polite"></p>
  </div>
</div>
'''
