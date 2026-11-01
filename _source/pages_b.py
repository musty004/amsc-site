import data as D
import shell
from shell import icon, img, pill, ext, band, pagehead, mail_link

# ================================================================== ACADEMICS
ACADEMICS = pagehead("Academics",
  "Tutorials, past questions, scholarship notices and exam support, run by the academics team "
  "for every level. Fostering academic excellence in Muslim students.") + f'''
<section class="section">
  <div class="wrap split split--sidebar">
    <div>
      <h2>Weekend tutorials</h2>
      <p>Tutorials are taught by students who have already passed the course, in lecture rooms the
      Institute allocates to us. Come with your notes and arrive on time: each room is booked for a
      fixed slot.</p>
      <div class="soon mt-m">
        {pill("Coming soon", "green")}
        <h3>Tutorial timetable for {D.SESSION}</h3>
        <p>The academics team is confirming courses, tutors and venues for this session. The
        timetable will be published here and shared with members as soon as it is ready.</p>
      </div>
      <h3 class="mt-l">Courses we usually cover</h3>
      <ul class="chips chips--mist">
        <li>Engineering Mathematics</li><li>Applied Mechanics</li><li>Applied Electricity</li>
        <li>Fluid Mechanics</li><li>Computer Programming</li><li>General Chemistry</li>
        <li>General Mathematics</li><li>Business Statistics</li>
      </ul>
      <p class="note">Tutorials usually hold on weekend afternoons. Need a course that is not listed? Ask for a tutorial.</p>
    </div>
    <aside class="stack">
      <div class="card">
        {icon("cap")}
        <h3>Tutor a course</h3>
        <p>Scored well in a course? Teach it to the level below you: one course, one session a week.</p>
        <div class="card__foot"><a class="link" href="join.html#volunteer">Volunteer as a tutor</a></div>
      </div>
      <div class="card">
        {icon("calendar")}
        <h3>Ask for a tutorial</h3>
        <p>If a difficult course has no tutorial, tell us. When five students ask, we find a tutor.</p>
        <div class="card__foot">{ext(D.wa_text("Assalamu alaykum, we need a tutorial for: "), "Request a tutorial", "link")}</div>
      </div>
      <div class="card card--yellow">
        {icon("book")}
        <h3>PDFNest partnership</h3>
        <p>AMSC has partnered with PDFNest: exam-recommended PDFs, quick polls and academic updates for students.</p>
        <div class="card__foot"><a class="link" href="#pdfnest">See what you get</a></div>
      </div>
    </aside>
  </div>
</section>

<section class="section section--blue" id="pdfnest">
  <div class="wrap partner">
    <div class="partner__media">
      <div class="framed">{img("flyer-pdfnest", "Partnership announcement: PDFNest and the AFIT Muslim Students' Community have officially partnered to make your studies better", "(min-width: 960px) 460px, 100vw")}</div>
    </div>
    <div>
      <p class="kicker">{pill("Official partner")}</p>
      <h2>PDFNest Students Hub</h2>
      <p class="partner__tag">Study smarter. Stay informed. Prepare better.</p>
      <p>PDFNest Students Hub gives students access to useful academic resources, and a community
      where they can stay informed and make better academic decisions. Administrators share
      resources and updates; students take part, vote and stay connected.</p>
      <ul class="benefits">
        <li>{icon("download")}<div><b>Exam-recommended PDFs</b><span>Study materials recommended by students who have actually used and reviewed them.</span></div></li>
        <li>{icon("check")}<div><b>Quick polls</b><span>Take part in polls and contribute to academic discussions.</span></div></li>
        <li>{icon("alert")}<div><b>Important updates</b><span>Stay informed about academic information and announcements.</span></div></li>
      </ul>
      <p class="partner__motto">Revise smart, not hard.</p>
      <div class="partner__actions">
        <div>
          <a class="btn btn--yellow" href="{D.PDFNEST_URL}" target="_blank" rel="noopener">Join PDFNest{icon("external")}<span class="sr-only"> (opens the PDFNest website in a new tab)</span></a>
          <p>Opens the PDFNest website, where you sign up.</p>
        </div>
        <div>
          <a class="btn btn--green" href="{D.PDFNEST_WA}" target="_blank" rel="noopener">{icon("whatsapp")}Get PDFNest Group Access<span class="sr-only"> (opens WhatsApp)</span></a>
          <p>Opens a WhatsApp chat with the PDFNest DCC, who can add you to the group.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--mist" id="pq">
  <div class="wrap split">
    <div>
      <h2>The past question bank</h2>
      <p class="lede">Past questions from departments across every level, organised in one shared
      folder and free for everyone.</p>
      <p>It is useful and it is incomplete: it only grows because students send in what they have.</p>
      <div class="actions">{ext(D.PQ, "Open the past question bank", "btn btn--blue")}</div>
    </div>
    <div class="card" id="contribute">
      {icon("download")}
      <h3>Send in papers</h3>
      <p>Typed or scanned are both fine. Name each file with the course code, session and semester,
      for example <em>GET209_2025-26_Rain.pdf</em>, and send it to the academics team.</p>
      <div class="card__foot actions">
        {ext(D.wa_text("Assalamu alaykum, I have past questions to contribute."), "Send on WhatsApp", "link")}
        <a class="link" href="mailto:{D.EMAIL}?subject=Past%20questions">Send by email</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="scholarships">
  <div class="wrap split">
    <div>
      <h2>Scholarships and attestation letters</h2>
      <p>The academics team shares scholarship openings for Nigerian Muslim students as they appear,
      with their deadlines. The MSFN scholarship, worth up to &#8358;120,000 a year for secondary and
      undergraduate students, is one we have supported members through.</p>
      <p>Most scholarship applications ask for a letter of attestation from your Islamic community,
      and AMSC issues these. Send the General Secretary your full name, department, level and the
      scholarship you are applying for, and allow a few days.</p>
      <div class="actions">
        <a class="btn btn--blue" href="mailto:{D.EMAIL}?subject=Request%20for%20an%20attestation%20letter">Request an attestation letter</a>
      </div>
    </div>
    <div class="card card--mist">
      <h3>Before you apply</h3>
      <ul class="meta">
        <li>{icon("clock")}Start a week before the deadline, not the night before</li>
        <li>{icon("book")}Have your results, admission letter and ID ready as clear scans</li>
        <li>{icon("pen")}Write the personal statement yourself, then ask someone to read it</li>
        <li>{icon("shield")}No genuine scholarship asks you to pay to apply</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--blue">
  <div class="wrap">
    <div class="sechead">
      <h2>When exams start</h2>
      <p class="lede">What the academics team runs through exam season.</p>
    </div>
    <div class="grid grid--4">
      <div class="card">{icon("calendar")}<h3>Revision plan</h3><p>A shared plan built back from the exam dates, with tutorial slots for the hardest papers.</p></div>
      <div class="card">{icon("book")}<h3>Group study</h3><p>Study sessions in an agreed room, with a rota so nobody revises alone late at night.</p></div>
      <div class="card">{icon("pen")}<h3>Past question drills</h3><p>Timed practice with questions from the past question bank before each paper.</p></div>
      <div class="card">{icon("cap")}<h3>Course clinics</h3><p>Senior students take your questions on the toughest courses in the days before the exam.</p></div>
    </div>
  </div>
</section>

{band("Doing well in your courses is part of the trust you carry",
      "Tutorials, past questions and study groups are open to every Muslim student at AFIT, member or not.",
      (D.PQ, "Open the past question bank"), ("join.html", "Register as a member"))}
'''

# ================================================================== EVENTS
def flyer(name, alt, when, title, text, href=None):
    tag, end = (f'<a class="flyer" href="{href}">', '</a>') if href else ('<figure class="flyer">', '</figure>')
    cap_open, cap_close = ('<div class="flyer__body">', '</div>') if href else ('<figcaption>', '</figcaption>')
    return (f'{tag}{img(name, alt, "(min-width: 960px) 280px, 50vw")}{cap_open}'
            f'<span class="when">{when}</span><h3>{title}</h3><p>{text}</p>{cap_close}{end}')

EVENTS = pagehead("Events",
  "The programmes that anchor the AMSC year, what is coming up this session, and highlights "
  "from the last one.") + f'''
<section class="section">
  <div class="wrap split">
    <div>
      <h2>Coming up this session</h2>
      <p class="lede">Dates for the {D.SESSION} session are announced to registered members on the
      AMSC WhatsApp Community, and on Instagram, once each programme is approved.</p>
      <div class="actions">
        <a class="btn btn--blue" href="{D.JOIN}">{icon("whatsapp")}Join the WhatsApp Community</a>
        {ext(D.IG, f"Follow {D.IG_HANDLE}", "btn btn--line")}
      </div>
    </div>
    <ul class="tl">
      <li><span class="when">Start of session</span><h4>Freshers&rsquo; Orientation</h4><p>Date to be announced. Until then, new students can use the <a href="freshers.html">freshers&rsquo; guide</a>.</p></li>
      <li><span class="when">From the first weekend</span><h4>Weekly programmes resume</h4><p>Islamiyya, tutorials, the Sisters Circle, Ta&rsquo;alim, Musaffa and fixtures restart together.</p></li>
      <li><span class="when">Every Friday</span><h4>Jumu&rsquo;ah</h4><p>At the {D.JUMUAH_PLACE}.</p></li>
    </ul>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="sechead">
      <h2>The AMSC year</h2>
      <p class="lede">What happens, and roughly when, in a typical session.</p>
    </div>
    <div class="split">
      <ul class="tl">
        <li><span class="when">Start of session</span><h4>Freshers&rsquo; Orientation</h4><p>New students meet the community, tour the mosque and campus, receive an academic survival guide and are paired with a mentor.</p></li>
        <li><span class="when">First weeks</span><h4>Registration and dues</h4><p>The membership register opens, level groups form and semester dues are announced.</p></li>
        <li><span class="when">First semester</span><h4>Weekly programmes</h4><p>Islamiyya, tutorials, the Sisters Circle, Ta&rsquo;alim, Musaffa and fixtures set the rhythm early.</p></li>
        <li><span class="when">Holiday</span><h4>IDIT cohort</h4><p>Four weeks of online digital skills training, open beyond AFIT.</p></li>
        <li><span class="when">1 February</span><h4>World Hijab Day</h4><p>Talks and outreach led by the sisters&rsquo; wing.</p></li>
      </ul>
      <ul class="tl">
        <li><span class="when">During the session</span><h4>Da&rsquo;wah Week</h4><p>A week of Islamic outreach, learning, awareness and community engagement.</p></li>
        <li><span class="when">Ramadan</span><h4>Annual Ramadan Lecture and Iftar</h4><p>Lectures, reflection and a shared Iftar, with iftar for students on campus through the month, taraweeh and a Zakat al-Fitr drive.</p></li>
        <li><span class="when">Eid al-Fitr and Eid al-Adha</span><h4>Eid prayer</h4><p>Usually held at {D.EID_PLACE}. The time is announced by the Imam at the Base Mosque. A shared meal follows for students who could not travel home.</p></li>
        <li><span class="when">Second semester</span><h4>Annual Musabaqatul Qur&rsquo;an</h4><p>Preliminaries, then the grand finale, with certificates for every participant.</p></li>
        <li><span class="when">End of session</span><h4>FYB Sendforth Walimah</h4><p>The send-off for final-year students, the FYB awards and induction into AMAN, the alumni network.</p></li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sechead">
      <h2>Last session, 1447 AH</h2>
      <p class="lede">The flyers from the programmes we held in 2025 and 2026.</p>
    </div>
    <div class="flyers">
      {flyer("flyer-freshers", "Freshers' Orientation flyer", "8 November 2025", "Freshers&rsquo; Orientation", "Navigating campus, guided by Islam in every step. Mosugu Hall.", "#orientation")}
      {flyer("flyer-idit", "IDIT 3.0 flyer", "From 15 December 2025", "IDIT 3.0", "Four weeks of AI, data analysis, design and video, online.", "programmes.html#idit")}
      {flyer("flyer-idit-graduation", "IDIT graduation ceremony flyer", "21 February 2026", "IDIT graduation", "Beyond the Degree: positioning for global relevance in the AI era.", "programmes.html#idit")}
      {flyer("flyer-hijabday", "World Hijab Day 2026 flyer", "February 2026", "World Hijab Day", "Theme: More Than A Scarf.", "sisters.html#hijabday")}
      {flyer("flyer-musabaqah", "5th Annual Musabaqatul Qur'an invitation", "9 May 2026", "5th Musabaqatul Qur&rsquo;an", "Grand finale at the Ibrahim Alfa Hall.", "#musabaqah")}
      {flyer("flyer-sendforth", "FYB Sendforth Walimah flyer", "4 July 2026", "FYB Sendforth Walimah", "Mosugu Hall, behind the Ibrahim Alfa Auditorium.", "#sendforth")}
      {flyer("flyer-aman", "AMAN launch flyer", "Launched", "AMAN", "The AFIT Muslim Alumni Network, officially launched.", "alumni.html")}
      {flyer("flyer-askbox", "Ask us that question on Islam flyer", "All session", "Ask a question", "Anonymous questions on Islam, answered in session.", D.ASKBOX)}
    </div>
  </div>
</section>

<section class="section section--mist" id="musabaqah">
  <div class="wrap split">
    <div>
      <h2>Annual Musabaqatul Qur&rsquo;an</h2>
      <p class="lede">Our largest programme. The fifth edition was held at the Ibrahim Alfa Hall on
      9 May 2026.</p>
      <p>Students register in the category that matches how much they have memorised, compete in a
      preliminary round, and the qualifiers recite at the grand finale in front of the community.
      It is not only for huffaz: there is a category for anyone still building consistency, and
      every participant receives a certificate.</p>
      <div class="table-wrap mt-m">
        <table class="table">
          <thead><tr><th scope="col">Category</th><th scope="col">Scope</th></tr></thead>
          <tbody>
            <tr><td>2 Hizb</td><td>For those building consistency</td></tr>
            <tr><td>10 Hizb</td><td>Intermediate memorisation</td></tr>
            <tr><td>20 Hizb</td><td>Advanced memorisation</td></tr>
            <tr><td>40 Hizb</td><td>The complete Qur&rsquo;an</td></tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="stack">
      <div class="card">
        {icon("star")}
        <h3>How to take part</h3>
        <ul class="meta">
          <li>{icon("calendar")}Register before the published deadline</li>
          <li>{icon("mic")}Recite at the preliminary stage</li>
          <li>{icon("quran")}Qualifiers recite at the grand finale</li>
          <li>{icon("gift")}Certificates for every participant, prizes for the winners</li>
        </ul>
      </div>
      <figure class="framed mt-0">{img("musabaqah-finale", "The auditorium during the grand finale of the 5th Musabaqatul Qur'an", "(min-width: 960px) 540px, 100vw")}</figure>
      <div class="card">
        {icon("camera")}
        <h3>Relive the fifth edition</h3>
        <p>The full photo album from the preliminary stage and the grand finale.</p>
        <div class="card__foot">{ext(D.ALBUM_MUSABAQAH, "Open the photo album", "link")}</div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="sendforth">
  <div class="wrap split">
    <div>
      <h2>FYB Sendforth Walimah</h2>
      <p class="lede">The send-off for final-year students, held on 4 July 2026 at Mosugu Hall.</p>
      <p>Networking, games, Islamic films, inspiring sessions, giveaways and the FYB awards, closing
      with the finalists&rsquo; photo session and induction into AMAN, the alumni network.</p>
      <div class="table-wrap mt-m">
        <table class="table table--times">
          <caption class="sr-only">Order of the day</caption>
          <thead><tr><th scope="col">Time</th><th scope="col">Item</th></tr></thead>
          <tbody>
            <tr><td>9:00am</td><td>Registration and opening</td></tr>
            <tr><td>9:15am</td><td>Short film and popcorn</td></tr>
            <tr><td>10:00am</td><td>Keynote address</td></tr>
            <tr><td>10:20am</td><td>Impact panel discussion and questions</td></tr>
            <tr><td>11:20am</td><td>Games and refreshments</td></tr>
            <tr><td>12:45pm</td><td>FYB awards and closing</td></tr>
            <tr><td>1:00pm</td><td>Finalists&rsquo; photo session</td></tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="framed">{img("flyer-sendforth-agenda", "FYB Sendforth Walimah programme flyer", "(min-width: 960px) 540px, 100vw")}</div>
  </div>
</section>

<section class="section section--mist" id="orientation">
  <div class="wrap feature">
    <div class="feature__media">{img("orientation-2025-sisters", "New sisters listening at the 2025/1447 Freshers' Orientation", "(min-width: 960px) 540px, 100vw")}<p class="note">Freshers&rsquo; Orientation, 2025/1447.</p></div>
    <div>
      <h2>Freshers&rsquo; Orientation</h2>
      <p class="lede">Last held on 8 November 2025 at Mosugu Hall, themed <em>navigating campus,
      guided by Islam in every step</em>.</p>
      <p>New students meet the community, learn where to pray between lectures, receive the academic
      survival guide and are paired with a mentor. Feedback is collected anonymously afterwards so
      the next one is better.</p>
      <div class="actions"><a class="btn btn--blue" href="freshers.html">Read the freshers&rsquo; guide</a>{ext(D.ALBUM_ORIENTATION_2025, "2025/1447 photos", "btn btn--line")}</div>
    </div>
  </div>
</section>

<section class="section section--blue">
  <div class="wrap">
    <div class="sechead">
      <h2>How a programme gets approved</h2>
      <p class="lede">AFIT is a military institution. Every programme, guest and venue goes through
      proper clearance, and we treat that as part of doing the work well.</p>
    </div>
    <ol class="route route--4">
      <li><h3>Proposal</h3><p>Objective, date, venue, expected attendance and budget, written up by the organising team.</p></li>
      <li><h3>Speaker vetting</h3><p>Guest details and the lecture topic are submitted in advance.</p></li>
      <li><h3>Institute clearance</h3><p>A formal request through the right office, submitted weeks ahead.</p></li>
      <li><h3>Announcement</h3><p>Only after approval: flyers, the community announcement and this page, together.</p></li>
    </ol>
  </div>
</section>

{band("Every event needs hands before it needs an audience",
      "Set-up, registration, ushering, photography, catering and clean-up. Tell us which one you can do.",
      ("join.html#volunteer", "Volunteer for an event"), ("contact.html", "Propose an event"))}
'''

# ================================================================== SALAH
SALAH = pagehead("Prayer times",
  "Today&rsquo;s prayer times for Kaduna, jama&rsquo;ah times, and where we pray: daily, on Fridays "
  "and on Eid.") + f'''
<section class="section section--tight">
  <div class="wrap">
    <h2 class="sr-only">Today in Kaduna</h2>
    <div class="salah-grid" id="salah-grid" aria-live="polite"></div>
    <noscript><p class="notice">Prayer times need JavaScript. Jama&rsquo;ah is held 15 minutes after each prayer time, except Dhuhr at 1:15pm.</p></noscript>
    <p class="note">Jama&rsquo;ah is held <strong>15 minutes after each prayer time</strong>, except
    <strong>Dhuhr, which is fixed at 1:15pm</strong>. Prayer times update each day and are saved on
    your device, so this page still works without data.</p>
  </div>
</section>

<section class="section" id="where">
  <div class="wrap">
    <div class="sechead">
      <h2>Where we pray</h2>
      <p class="lede">Daily prayers on campus, Jumu&rsquo;ah at the Base Central Mosque, and Eid at the
      Air Force Primary School.</p>
    </div>
    <div class="prayer-places">
      <article class="place place--jumuah" id="jumuah">
        {pill("Every Friday")}
        <h3>Jumu&rsquo;ah</h3>
        <p class="place__where">{icon("pin")}<span>{D.JUMUAH_PLACE}</span></p>
        <p>We observe Jumu&rsquo;ah together at the Base Central Mosque. Come early so you can find a
        place and listen to the khutbah from the beginning.</p>
      </article>
      <article class="place place--eid" id="eid">
        {pill("Eid al-Fitr and Eid al-Adha")}
        <h3>Eid prayer</h3>
        <p class="place__where">{icon("pin")}<span>Usually at the {D.EID_PLACE}</span></p>
        <p>The exact time for Eid prayer is announced by the Imam at the Base Mosque. It is also
        shared with members on the AMSC WhatsApp Community, so <a href="{D.JOIN}">register</a> to
        receive it.</p>
      </article>
    </div>

    <h3 class="mt-l">Daily prayers on campus</h3>
    <div class="grid grid--3 mt-s">
      <div class="card">
        {icon("mosque")}
        <h3>AFIT Mosque</h3>
        <ul class="meta">
          <li>{icon("users")}Brothers and sisters, separate sections</li>
          <li>{icon("clock")}All five daily prayers in congregation</li>
          <li>{icon("star")}Islamiyya and the Sisters Circle</li>
        </ul>
        <p>The main mosque on campus and the home of the community. Wudu facilities available.</p>
      </div>
      <div class="card">
        {icon("mosque")}
        <h3>Male Hostel Mosque</h3>
        <ul class="meta">
          <li>{icon("users")}Brothers</li>
          <li>{icon("clock")}Daily prayers, and Musaffa on Wednesdays</li>
        </ul>
        <p>The closest option for brothers in the hostel, especially for Fajr and Isha.</p>
      </div>
      <div class="card">
        {icon("compass")}
        <h3>Prayer spaces near lectures</h3>
        <ul class="meta">
          <li>{icon("clock")}Dhuhr and Asr between classes</li>
          <li>{icon("pin")}Ask any AMSC member for directions</li>
        </ul>
        <p>Know a space that should be listed here? Tell the media team and we will add it.</p>
      </div>
    </div>
    <div class="notice notice--blue mt-m">{icon("compass")}<p><strong>Qiblah at AFIT:</strong>
    roughly east-north-east. Every listed space is already aligned, so follow the lines on the mat
    rather than a phone compass indoors, where metal and walls throw the reading off.</p></div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap split">
    <div>
      <h2>The etiquette of Friday</h2>
      <p>Jumu&rsquo;ah is the gathering of the week. The recommended practice for the day: ghusl
      before setting out, clean or best clothes, perfume if you have it, arriving early, reciting
      Surah Al-Kahf, sending abundant salawat on the Prophet ﷺ, and listening to the khutbah without
      disturbing anyone.</p>
    </div>
    <div class="card">
      {icon("arch")}
      <h3>Jumu&rsquo;ah location</h3>
      <p>{D.JUMUAH_PLACE}.</p>
      <div class="card__foot"><a class="link" href="events.html">See what is coming up</a></div>
    </div>
  </div>
</section>

{band("Set the rhythm of your week around the five",
      "Every tutorial, circle and fixture on this site is scheduled around the prayer times above.",
      ("programmes.html#timetable", "See the weekly timetable"), (D.JOIN, "Join AMSC"))}
'''
