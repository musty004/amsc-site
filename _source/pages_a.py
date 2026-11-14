import data as D
import shell
from shell import icon, img, ar, pill, ext, band, pagehead, formspree_form, mail_link

# ================================================================== ABOUT
values = "".join(f'<div class="value"><h3>{v}</h3><p>{t}</p></div>' for v, t in D.VALUES)

ABOUT = pagehead("About AMSC",
  "A faith-driven community helping Muslim students at the Air Force Institute of Technology "
  "grow in deen, character and academic excellence.") + f'''
<section class="section">
  <div class="wrap split">
    <div>
      <h2>Who we are</h2>
      <p class="lede">The AFIT Muslim Students&rsquo; Community is a faith-driven body dedicated to
      fostering spiritual growth, unity and purpose among Muslim students at the Air Force
      Institute of Technology.</p>
      <p>Rooted in Islamic values and guided by sincerity, discipline, faith and brotherhood, the
      community provides a space for students to grow in deen and character through worship,
      service, learning and positive impact on campus.</p>
      <p>AMSC is more than a religious group. We run the Islamiyyah classes and the Qur&rsquo;an
      circles, and we also run weekend tutorials, digital skills training and a welfare network,
      so that no Muslim student at AFIT has to work out student life alone.</p>
      <p>Membership is open to every Muslim student of the Institute, whatever their department,
      level, state of origin or school of thought.</p>
    </div>
    <div class="card card--mist">
      <h3>At a glance</h3>
      <ul class="meta">
        <li>{icon("mosque")}Based at the AFIT Mosque, with activities at the male hostel mosque and in lecture rooms</li>
        <li>{icon("users")}A brothers&rsquo; wing and a sisters&rsquo; wing, each with its own programmes and leaders</li>
        <li>{icon("shield")}Led by an <a href="executive.html">Executive Committee</a> of students, renewed each session</li>
        <li>{icon("star")}AMAN, the <a href="alumni.html">AFIT Muslim Alumni Network</a>, for graduates</li>
        <li>{icon("book")}A study partnership with <a href="academics.html#pdfnest">PDFNest</a></li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--blue">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Our purpose</h2>
        <p class="lede">To help Muslim students at AFIT hold on to their deen while they excel in
        their studies: by teaching what they need to know, supporting them when things are hard,
        and building a brotherhood and sisterhood that lasts beyond graduation.</p>
      </div>
      <div>
        <h2>Where we are going</h2>
        <p class="lede">A community strong enough not to depend on any single set of students:
        established programmes, honest accounts, a real library, a working welfare fund, and an
        alumni network that carries the next generation.</p>
      </div>
    </div>
    <div class="messages mt-l">
      <p>{D.CORE}</p>
      <p>{D.KEY}</p>
      <p>{D.CAMPAIGN}</p>
    </div>
  </div>
</section>

<section class="section" id="values">
  <div class="wrap">
    <div class="sechead">
      <h2>Our values</h2>
      <p class="lede">Seven values guide how we work: a balance of faith, academic excellence,
      community and the discipline AFIT is known for.</p>
    </div>
    <div class="values-list">{values}</div>
  </div>
</section>

<section class="section section--mist" id="logo">
  <div class="wrap feature">
    <div class="feature__media">
      <div class="logo-arch arch"><img src="assets/img/logo-mark-384.webp" alt="The AMSC logo" width="384" height="384" loading="lazy" decoding="async"></div>
    </div>
    <div>
      <h2>What our logo means</h2>
      <p class="lede">Every part of the AMSC mark carries a meaning.</p>
      <ul class="symbols">
        <li>{icon("users")}<div><h3>Three figures</h3><p>Community, diversity and togetherness: unity among Muslim students.</p></div></li>
        <li>{icon("wheat")}<div><h3>Wheat</h3><p>Growth and barakah (blessing), spiritual nourishment, development and flourishing.</p></div></li>
        <li>{icon("wings")}<div><h3>Wings</h3><p>AFIT&rsquo;s military foundation and the Air Force: ambition, progress and elevation.</p></div></li>
        <li>{icon("arch")}<div><h3>Mosque arch</h3><p>The mihrab, a sacred Islamic space: prayer, spiritual direction and the Qiblah.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sechead">
      <h2>How we work</h2>
      <p class="lede">Four commitments we hold ourselves to.</p>
    </div>
    <div class="grid grid--4">
      <div class="card">{icon("users")}<h3>Open to all</h3><p>No faction and no gatekeeping. Differences of madhhab are handled with adab, and nobody is turned away.</p></div>
      <div class="card">{icon("shield")}<h3>Accountable</h3><p>Dues and donations are recorded and reported to members, with two signatures on every disbursement.</p></div>
      <div class="card">{icon("cap")}<h3>Academically serious</h3><p>A student who fails out cannot serve anyone. Tutorials and the past question bank are core work, not extras.</p></div>
      <div class="card">{icon("heart")}<h3>Quietly helpful</h3><p>Welfare is confidential by design. Nobody&rsquo;s need becomes public information.</p></div>
    </div>
  </div>
</section>

<section class="section section--mist" id="committees">
  <div class="wrap">
    <div class="sechead sechead--split">
      <div>
        <h2>Leadership and committees</h2>
        <p class="lede mb-0">The <a href="executive.html">Executive Committee</a> leads AMSC for one
        session. Committees of volunteers do most of the work, and every one of them welcomes new hands.</p>
      </div>
      <div><a class="btn btn--blue" href="executive.html">Meet the Executive Committee</a></div>
    </div>
    <div class="grid grid--3">
      <div class="card">{icon("quran")}<h3>Da&rsquo;wah</h3><p>Islamiyyah, reminders, lectures, Da&rsquo;wah Week and the anonymous question-and-answer sessions.</p></div>
      <div class="card">{icon("cap")}<h3>Academics</h3><p>Schedules tutorials, recruits tutors and maintains the past question bank.</p></div>
      <div class="card">{icon("heart")}<h3>Welfare</h3><p>Helps new students settle in, visits members who are unwell and keeps in touch with students across the session.</p></div>
      <div class="card">{icon("camera")}<h3>Media and public relations</h3><p>Design, photography, video, announcements, the social channels and this website.</p></div>
      <div class="card">{icon("calendar")}<h3>Organising</h3><p>Venues, set-up, registration and logistics for every programme and event.</p></div>
      <div class="card">{icon("users")}<h3>Sisters&rsquo; committee</h3><p>The Sisters Circle, Ta&rsquo;alim, sisters&rsquo; welfare and the sisters&rsquo; side of every major event.</p></div>
    </div>
  </div>
</section>

{band("Serve where you are useful",
      "Tell us what you can do: teach, tutor, design, film, organise or code. We will find you a place.",
      ("join.html#volunteer", "Volunteer with AMSC"), ("contact.html", "Contact us"))}
'''

# ================================================================== PROGRAMMES
def prog(href, ico, name, text):
    return f'<li><a href="{href}">{icon(ico)}<span><b>{name}</b><span>{text}</span></span></a></li>'

PROGRAMMES = pagehead("Programmes",
  "Weekly classes, academic support, digital skills training and the annual programmes that "
  "bring the whole community together.") + f'''
<section class="section section--tight">
  <div class="wrap">
    <div class="prog-index">
      <div class="prog-group">
        <h2>Every week</h2>
        <ul>
          {prog("#islamiyya", "quran", "Islamiyyah", "Classes in Qur&rsquo;an, Arabic, Fiqh, Tawheed and Islamic knowledge.")}
          {prog("#tutorials", "cap", "Tutorials", "Academic support for students who may be struggling with their studies.")}
          {prog("#sisters-circle", "users", "Sisters Circle", "A club for Muslim sisters: sisterhood, support, connection and personal development.")}
        </ul>
      </div>
      <div class="prog-group prog-group--yellow">
        <h2>Skills</h2>
        <ul>
          {prog("#idit", "chip", "IDIT", "Technology and digital skills training designed to empower students.")}
        </ul>
      </div>
      <div class="prog-group">
        <h2>Every year</h2>
        <ul>
          {prog("#musabaqah", "star", "Annual Musabaqatul Qur&rsquo;an", "Our annual Qur&rsquo;an recitation competition.")}
          {prog("#dawah-week", "mic", "Da&rsquo;wah Week", "A week of Islamic outreach, learning, awareness and community engagement.")}
          {prog("#ramadan", "mosque", "Annual Ramadan Lecture and Iftar", "Lectures, reflection, and a shared Iftar meal for the community.")}
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight" id="timetable">
  <div class="wrap">
    <div class="sechead">
      <h2>Weekly timetable</h2>
      <p class="lede">Days, times and venues as announced by the community. If a session moves, the
      change goes out on the WhatsApp Community first.</p>
    </div>
    <div class="table-wrap">
      <table class="table">
        <thead><tr><th scope="col">Programme</th><th scope="col">Day</th><th scope="col">Time</th><th scope="col">Venue</th><th scope="col">Open to</th></tr></thead>
        <tbody>
          <tr><td><a href="islamiyyah.html">Islamiyyah</a></td><td>Saturday and Sunday</td><td>9:00am to 12:30pm</td><td>AFIT Mosque</td><td>Everyone</td></tr>
          <tr><td><a href="#tutorials">Tutorials</a></td><td>Weekends</td><td>Timetable coming soon</td><td>Lecture rooms, announced</td><td>By level</td></tr>
          <tr><td><a href="#sisters-circle">Sisters Circle</a></td><td>Friday</td><td>4:00pm to 6:00pm</td><td>AFIT Masjid, female section</td><td>Sisters</td></tr>
          <tr><td><a href="#taalim">Sisters&rsquo; Ta&rsquo;alim</a></td><td>Monday and Wednesday</td><td>8:00pm</td><td>Online (Google Meet)</td><td>Sisters</td></tr>
          <tr><td><a href="#musaffa">Musaffa</a></td><td>Wednesday</td><td>Between Maghrib and Isha</td><td>Male Hostel Mosque</td><td>All students</td></tr>
          <tr><td><a href="#sports">Football</a></td><td>Weekly fixture</td><td>4:30pm</td><td>MTC Field</td><td>Brothers</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section" id="islamiyya">
  <div class="wrap split">
    <div>
      <p class="kicker">{pill("Every weekend")} {D.ISLAMIYYAH_VENUE}</p>
      <h2>Islamiyyah</h2>
      <p class="lede">Weekend Islamic education: Qur&rsquo;an, Arabic and Islamic book studies,
      taught by students for students.</p>
      <p>Qur&rsquo;an sessions cover Musaffa, Tajweed and Hifz, with students grouped by ability.
      Arabic is taught at three levels, and on Sunday everyone studies selected texts on
      Tawheed, Fiqh and Seerah together. Registered students track their Qur&rsquo;an progress
      and download class materials in the Student Portal.</p>
      <ul class="meta">
        <li>{icon("calendar")}{D.ISLAMIYYAH_DAYS}</li>
        <li>{icon("clock")}{D.ISLAMIYYAH_HOURS}</li>
        <li>{icon("pin")}{D.ISLAMIYYAH_VENUE}</li>
      </ul>
      <div class="actions"><a class="btn btn--blue" href="islamiyyah.html">About the Islamiyyah</a>
        <a class="btn btn--line" href="{D.PORTAL}">Student Portal</a></div>
    </div>
    <div class="card card--mist">
      <h3>The weekend timetable</h3>
      <ul class="meta">
        <li>{icon("quran")}Saturday and Sunday, 9:00 to 11:00am: Musaffa, Tajweed and Hifz</li>
        <li>{icon("pen")}Saturday, 11:00am to 12:30pm: Arabic Language</li>
        <li>{icon("book")}Sunday, 11:00am to 12:30pm: Islamic Book Studies</li>
      </ul>
      <div class="card__foot"><a class="link" href="islamiyyah.html#timetable">Levels and texts</a></div>
    </div>
  </div>
</section>

<section class="section section--tight section--flush" id="dawrah">
  <div class="wrap">
    <div class="partner-strip">
      <div class="partner-strip__copy">
        <p class="kicker">{pill("Registration open")} {D.DAWRAH_VENUE}</p>
        <h2>Dawrah: {D.DAWRAH_TITLE}</h2>
        <p>{D.DAWRAH_SUBJECT}, at the {D.DAWRAH_VENUE} {D.DAWRAH_WHEN[0].lower() + D.DAWRAH_WHEN[1:]}, for {D.DAWRAH_LENGTH.lower()}.
        {D.DAWRAH_DAYS}. Each class comes with a recording and short questions, and there is a final exam.</p>
        <div class="actions"><a class="btn btn--blue" href="{D.DAWRAH_PAGE}#register">Register for the Dawrah</a>
          <a class="link" href="{D.DAWRAH_PAGE}">About the Dawrah</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--mist" id="tutorials">
  <div class="wrap split">
    <div>
      <p class="kicker">{pill("Weekends")} Timetable coming soon</p>
      <h2>Tutorials</h2>
      <p class="lede">Academic support for students who may be struggling with their studies.</p>
      <p>Tutorials are taught by students who have already passed the course: Engineering
      Mathematics, Applied Mechanics, Fluid Mechanics, Programming, Chemistry and more. Come with
      your notes; the rooms are booked for fixed slots. The timetable for this session is being prepared.</p>
      <div class="actions"><a class="btn btn--blue" href="academics.html">Academic support</a></div>
    </div>
    <div class="card">
      <h3>Also from the academics team</h3>
      <ul class="meta">
        <li>{icon("book")}A free <a href="academics.html#pq">past question bank</a></li>
        <li>{icon("star")}Letters of attestation for scholarship applications</li>
        <li>{icon("calendar")}Exam-season revision plans and group study</li>
        <li>{icon("chip")}Study materials through our partnership with <a href="academics.html#pdfnest">PDFNest</a></li>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="sisters-circle">
  <div class="wrap feature">
    <div class="feature__media"><div class="arch" style="aspect-ratio:4/5;max-width:420px">{img("flyer-sisters-circle", "The Sisters Circle flyer: vocational training, quizzes, games, interactive sessions and picnics", "(min-width: 960px) 420px, 90vw")}</div></div>
    <div>
      <p class="kicker">{pill("Fridays")} 4:00pm to 6:00pm, AFIT Masjid (female section)</p>
      <h2>Sisters Circle</h2>
      <p class="lede">A student club for Muslim sisters, designed to foster sisterhood, support,
      connection and personal development.</p>
      <p>Each week brings vocational training, quizzes, games, interactive sessions and the
      occasional picnic. Alongside the Circle, the sisters&rsquo; <strong id="taalim">Ta&rsquo;alim</strong>
      meets online on Mondays and Wednesdays at 8:00pm for Fiqh and Tawheed, so sisters can join
      from the hostel or from home.</p>
      <div class="actions"><a class="btn btn--blue" href="sisters.html">The sisters&rsquo; page</a></div>
    </div>
  </div>
</section>

<section class="section section--blue" id="idit">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="kicker">Islamic Digital and IT Training</p>
        <h2>IDIT</h2>
        <p class="lede">Technology and digital skills training designed to empower students.</p>
        <p>A four-week online programme run during the holidays, designed for complete beginners
        and open beyond AFIT. The third cohort, IDIT 3.0, began on 15 December 2025 and graduated
        on 21 February 2026 with a ceremony themed <em>Beyond the Degree: Strategic Positioning
        for Global Relevance in the AI Era</em>.</p>
        <p>A &#8358;500 commitment fee secures a place, with an optional &#8358;1,000 for a
        certificate of completion. Dates for the next cohort are announced on the WhatsApp Community.</p>
      </div>
      <div class="grid grid--2">
        <div class="card">{icon("chip")}<h3>AI Mastery</h3><p>Practical use of AI tools for study, research and work.</p></div>
        <div class="card">{icon("cap")}<h3>Data analysis</h3><p>From zero to reading, cleaning and charting real data.</p></div>
        <div class="card">{icon("pen")}<h3>Graphic design</h3><p>Layout, type and brand basics, built into a portfolio.</p></div>
        <div class="card">{icon("camera")}<h3>Video editing</h3><p>Cutting, sound and export for social media and events.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="annual">
  <div class="wrap">
    <div class="sechead">
      <h2>Every year</h2>
      <p class="lede">Three programmes bring the whole community together each session.</p>
    </div>
    <div class="annual" id="musabaqah">
      <div>
        <h3>Annual Musabaqatul Qur&rsquo;an</h3>
        <p>Our annual Qur&rsquo;an competition. Students register in the category that matches how
        much they have memorised, compete in a preliminary round, and the qualifiers recite at the
        grand finale. The fifth edition was held at the Ibrahim Alfa Hall on 9 May 2026.</p>
        <p>It is not only for huffaz. There is a category for anyone still building consistency,
        and every participant receives a certificate.</p>
        <a class="link" href="events.html#musabaqah">Categories and how to take part</a>
      </div>
      <div class="framed">{img("musabaqah-finale", "The auditorium during the grand finale of the 5th Musabaqatul Qur'an", "(min-width: 960px) 520px, 100vw")}</div>
    </div>
    <div class="annual" id="dawah-week">
      <div>
        <h3>Da&rsquo;wah Week</h3>
        <p>A week dedicated to Islamic outreach, learning, awareness and community engagement,
        run by the Da&rsquo;wah team with lectures and activities across the week.</p>
        <p>Dates and the programme for the week are announced on the WhatsApp Community and
        Instagram.</p>
        <a class="link" href="events.html">See the events calendar</a>
      </div>
      <div class="annual__panel">{icon("mic")}<p>Questions about Islam can be sent in anonymously at any time and are answered in the community&rsquo;s question-and-answer sessions.</p>{ext(D.ASKBOX, "Ask a question anonymously", "link")}</div>
    </div>
    <div class="annual" id="ramadan">
      <div>
        <h3>Annual Ramadan Lecture and Iftar</h3>
        <p>A Ramadan programme featuring lectures, spiritual reflection, a community gathering and
        a shared Iftar meal.</p>
        <p>Through the month, AMSC also arranges iftar for students who stay on campus, taraweeh,
        tafsir sessions and a Zakat al-Fitr drive.</p>
      </div>
      <div class="annual__panel">{icon("mosque")}<p>The month&rsquo;s iftar for students on campus is funded by members and alumni. Every contribution feeds a fasting student.</p><a class="link" href="give.html">Support Ramadan iftar</a></div>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="sechead">
      <h2>Also running</h2>
      <p class="lede">Smaller circles and activities that run alongside the main programmes.</p>
    </div>
    <div class="grid grid--2">
      <div class="card" id="musaffa">{icon("quran")}<h3>Musaffa</h3>
        <p>A Qur&rsquo;an recitation and correction circle on Wednesdays between Maghrib and Isha at
        the Male Hostel Mosque. It moves steadily through the Qur&rsquo;an from Surah Al-Baqarah, and
        the week&rsquo;s stopping point is posted to the community so nobody arrives lost.</p></div>
      <div class="card" id="sports">{icon("ball")}<h3>Sports</h3>
        <p>Football for the brothers at 4:30pm on fixture days at the MTC Field, and indoor games for
        the sisters alongside the Circle. During major events the fixtures become an
        inter-department tournament.</p></div>
      <div class="card" id="qa">{icon("mic")}<h3>Islamic Q&amp;A</h3>
        <p>Questions about Islam are submitted anonymously, then answered in a session on the
        community group. Only questions about Islam are taken, and every one gets an answer.</p>
        <div class="card__foot">{ext(D.ASKBOX, "Submit a question", "link")}</div></div>
      <div class="card" id="amanah">{icon("compass")}<h3>Amanah Desk</h3>
        <p>The AMSC lost-and-found. Report an item you have lost or found so it can be recorded and
        returned to its owner, guided by the principle of amanah.</p>
        <div class="card__foot"><a class="link" href="amanah.html">Go to the Amanah Desk</a></div></div>
    </div>
  </div>
</section>

{band("New programmes start when someone offers to run them",
      "Arabic conversation, a hifz cohort, a debate club, a coding circle: each is waiting for a coordinator.",
      ("join.html#volunteer", "Offer to run one"), ("contact.html", "Suggest a programme"))}
'''

# ================================================================== JOIN
from shell import formspree_form, gform

volunteer_form = formspree_form(D.FORMSPREE_CONTACT, """
  <input type="hidden" name="topic" value="Volunteering">
  <div class="field--2">
    <div class="field"><label for="vname">Full name</label><input type="text" id="vname" name="name" autocomplete="name" required></div>
    <div class="field"><label for="vphone">Phone or WhatsApp</label><input id="vphone" name="phone" type="tel" autocomplete="tel" required></div>
  </div>
  <div class="field--2">
    <div class="field"><label for="vdept">Department and level</label><input type="text" id="vdept" name="department_level" placeholder="e.g. Mechatronics, 300L" required></div>
    <div class="field"><label for="vrole">How would you like to help?</label>
      <select id="vrole" name="role"><option>Tutor a course</option><option>Design flyers</option><option>Photography and video</option><option>Writing for the blog</option><option>Ushering at events</option><option>Qur&rsquo;an tutoring</option><option>Welfare visits</option><option>Website and tech</option><option>Library contributions</option><option>Run a new programme</option><option>Something else</option></select></div>
  </div>
  <div class="field"><label for="vmsg">Anything else? <span class="opt">(optional)</span></label><textarea id="vmsg" name="message" rows="3" placeholder="Course you can tutor, skills, days you are free"></textarea></div>
  <button class="btn btn--blue" type="submit">Send</button>""",
  "Thank you for offering to help",
  "JazakAllahu khayran. Your details have reached the AMSC team, and someone will contact you about where you can serve.",
  "Volunteer offer from the AMSC website")

JOIN = pagehead("Join AMSC",
  "Register once to become a member and be added to the AMSC WhatsApp Community. It takes about three minutes.") + f'''
<section class="section" id="register">
  <div class="wrap split split--sidebar">
    <div>
      <h2>Registration form</h2>
      <p>Fill in the form below. Once you have registered, you will be added to the AMSC WhatsApp
      Community, our hub for announcements, academic updates, clearance guides and peer support.</p>
      {gform()}
    </div>
    <aside class="stack">
      <div class="card card--mist">
        <h3>What happens next</h3>
        <ol class="steps steps--compact">
          <li><b>You submit the form</b><span>A copy of your answers is sent to your email.</span></li>
          <li><b>You are added to the WhatsApp Community</b><span>An AMSC admin adds you using the number you gave.</span></li>
          <li><b>You receive every update</b><span>Programmes, tutorials, events and announcements.</span></li>
        </ol>
      </div>
      <div class="card">
        <h3>What membership gives you</h3>
        <ul class="meta">
          <li>{icon("cap")}Weekend tutorials and the past question bank</li>
          <li>{icon("quran")}Islamiyyah, Musaffa and the Ta&rsquo;alim circles</li>
          <li>{icon("heart")}Welfare officers to help you settle in</li>
          <li>{icon("star")}Attestation letters for scholarship applications</li>
          <li>{icon("users")}Mentorship from senior students and alumni</li>
          <li>{icon("chip")}Priority places on IDIT cohorts</li>
        </ul>
      </div>
      <div class="card">
        <h3>New to AFIT?</h3>
        <p>Read the clearance and registration guide before you start.</p>
        <div class="card__foot"><a class="link" href="freshers.html">Freshers&rsquo; guide</a></div>
      </div>
    </aside>
  </div>
</section>

<section class="section section--mist" id="dues">
  <div class="wrap split">
    <div>
      <h2>Semester dues</h2>
      <p>Dues are <strong>&#8358;1,000 and above</strong> per semester, paid by bank transfer to
      {D.DUES_ACCOUNT_NUMBER} ({D.DUES_ACCOUNT_NAME}, {D.DUES_BANK}). They pay for Islamiyyah
      materials, tutorial venues and printing, and events like the Musabaqah. You can also pay
      online with a card.</p>
      <p>If dues are difficult for you this semester, your membership continues unchanged.
      Nobody is removed for not paying.</p>
      <div class="actions">
        <a class="btn btn--blue" href="give.html#dues">Payment details</a>
        {ext(D.DUES, "Pay online", "btn btn--line")}
      </div>
    </div>
    <div class="card">
      <h3>Where the money goes</h3>
      <ul class="meta">
        <li>{icon("quran")}Islamiyyah and Da&rsquo;wah programmes</li>
        <li>{icon("cap")}Tutorials, printing and past question digitisation</li>
        <li>{icon("heart")}Welfare activities</li>
        <li>{icon("calendar")}The Musabaqah, orientation and the sendforth</li>
      </ul>
      <div class="card__foot"><a class="link" href="give.html#transparency">How funds are accounted for</a></div>
    </div>
  </div>
</section>

<section class="section" id="volunteer">
  <div class="wrap">
    <div class="sechead">
      <h2>Volunteer</h2>
      <p class="lede">AMSC runs on students doing small things reliably. These roles are usually
      needed. Pick one and send the form.</p>
    </div>
    <div class="grid grid--4">
      <div class="card"><h3>Tutors</h3><p>Teach one course, once a week, to the level below you.</p></div>
      <div class="card"><h3>Designers</h3><p>Flyers and announcement graphics for programmes.</p></div>
      <div class="card"><h3>Photo and video</h3><p>Cover events and keep the community&rsquo;s record.</p></div>
      <div class="card"><h3>Writers</h3><p>Event reports and articles for the blog.</p></div>
      <div class="card"><h3>Ushers</h3><p>Set-up, registration and crowd control at major events.</p></div>
      <div class="card"><h3>Qur&rsquo;an tutors</h3><p>Help beginners with reading and tajwid at Islamiyyah.</p></div>
      <div class="card"><h3>Welfare visitors</h3><p>Visit members who are unwell and welcome new students.</p></div>
      <div class="card"><h3>Developers</h3><p>Maintain this website and build the tools we still need.</p></div>
    </div>
    <div class="split mt-l" id="volunteer-form">
      <div>
        <h3>Offer to help</h3>
        <p>Tell us what you can do and when you are free. The team will contact you on the number you give.</p>
      </div>
      {volunteer_form}
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap split">
    <div>
      <h2>Take part</h2>
      <p class="lede">You do not need to wait to come along. Every programme is open to Muslim
      students at AFIT.</p>
      <div class="actions"><a class="btn btn--blue" href="programmes.html">See programmes</a><a class="btn btn--line" href="events.html">See events</a></div>
    </div>
    <div>
      <h2 class="sr-only">Questions</h2>
      <details class="faq"><summary>Do I have to be very knowledgeable to join?</summary><p>No. Islamiyyah exists because people start from different places. Beginners&rsquo; Qur&rsquo;an reading is one of our best-attended classes.</p></details>
      <details class="faq"><summary>Is AMSC tied to one school of thought?</summary><p>No. AMSC serves every Muslim student at AFIT. Differences of opinion are discussed with adab and never used to exclude anyone.</p></details>
      <details class="faq"><summary>How do I get into the WhatsApp Community?</summary><p>Fill in the registration form above. An AMSC admin adds you with the phone number you give.</p></details>
      <details class="faq"><summary>Can sisters take part fully?</summary><p>Yes. The sisters&rsquo; wing has its own Circle, Ta&rsquo;alim and leaders, and a share in every major event. See the <a href="sisters.html">sisters&rsquo; page</a>.</p></details>
      <details class="faq"><summary>Can students from outside AFIT join anything?</summary><p>The IDIT training cohorts are open to people outside AFIT. Campus programmes are for AFIT students.</p></details>
    </div>
  </div>
</section>
'''
