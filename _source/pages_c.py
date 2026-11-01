import data as D
import shell
from shell import icon, img, pill, ext, band, pagehead, person, formspree_form, mail_link, soon

# ================================================================== SISTERS
sister_leads = "".join(person(D.holder(r, "s")) for r in ("Ameerah", "Naibatul", "Welfare Officer II", "Asst. Welfare Officer II"))

SISTERS = pagehead("Sisters",
  "The sisters&rsquo; wing of AMSC: the Sisters Circle, the online Ta&rsquo;alim, World Hijab Day, "
  "welfare, and a full share in everything the community does.") + f'''
<section class="section">
  <div class="wrap split split--sidebar">
    <div>
      <h2>A space of your own</h2>
      <p class="lede">The sisters&rsquo; wing has its own gatherings, its own teaching circle, its own
      leaders under the Ameerah, and its own part in every major event AMSC holds.</p>
      <p>Two things run every week. The <strong>Sisters Circle</strong> meets in person on Friday
      afternoons at the female section of the AFIT Masjid. The <strong>Ta&rsquo;alim</strong> meets
      online twice a week in the evening, so you can attend from the hostel or from home during the
      break.</p>
    </div>
    <aside class="card card--mist">
      <h3>This week</h3>
      <ul class="meta">
        <li>{icon("calendar")}<span><strong>Ta&rsquo;alim:</strong> Monday and Wednesday, 8:00pm, Google Meet</span></li>
        <li>{icon("calendar")}<span><strong>Sisters Circle:</strong> Friday, 4:00pm to 6:00pm, AFIT Masjid</span></li>
        <li>{icon("calendar")}<span><strong>Islamiyya:</strong> Saturday and Sunday, 10:00am</span></li>
      </ul>
      <div class="card__foot"><a class="btn btn--blue btn--sm" href="{D.JOIN}">Join AMSC</a></div>
    </aside>
  </div>
</section>

<section class="section section--mist" id="taalim">
  <div class="wrap grid grid--2">
    <div class="card">
      {icon("quran")}
      <h3>Sisters&rsquo; Ta&rsquo;alim</h3>
      <ul class="meta">
        <li>{icon("calendar")}Mondays and Wednesdays</li>
        <li>{icon("clock")}8:00pm prompt</li>
        <li>{icon("pin")}Google Meet, sisters only</li>
      </ul>
      <p>A teaching circle focused on Fiqh and Tawheed: the rulings you need and the foundations
      they rest on. Questions are welcome and nothing is too basic to ask.</p>
      <div class="card__foot"><a class="link" href="{D.JOIN}">Register to get the meeting link</a></div>
    </div>
    <div class="card" id="circle">
      {icon("users")}
      <h3>Sisters Circle</h3>
      <ul class="meta">
        <li>{icon("calendar")}Every Friday</li>
        <li>{icon("clock")}4:00pm to 6:00pm</li>
        <li>{icon("pin")}AFIT Masjid, female section</li>
      </ul>
      <p>A student club for Muslim sisters, designed to foster sisterhood, support, connection and
      personal development: vocational training, quizzes, games, interactive sessions and picnics.</p>
      <div class="card__foot"><a class="link" href="#programme">What the Circle covers</a></div>
    </div>
  </div>
</section>

<section class="section" id="leaders">
  <div class="wrap">
    <div class="sechead sechead--split">
      <div>
        <h2>Sisters&rsquo; leaders</h2>
        <p class="lede mb-0">Nominees for the {D.SESSION} session. Call or message them directly.</p>
      </div>
      <div><a class="link" href="executive.html">See the full Executive Committee</a></div>
    </div>
    <ul class="people grid grid--2">{sister_leads}</ul>
  </div>
</section>

<section class="section section--mist" id="hijabday">
  <div class="wrap feature">
    <div class="feature__media"><div class="framed">{img("flyer-hijabday", "World Hijab Day 2026 flyer: More Than A Scarf", "(min-width: 960px) 540px, 100vw")}</div></div>
    <div>
      <p class="kicker">{pill("World Hijab Day 2026")}</p>
      <h2>More Than A Scarf</h2>
      <p>Each year the sisters&rsquo; wing marks World Hijab Day with talks, conversation and a shared
      gathering, about what the hijab means, what it asks and what it is worth, told by the women who
      wear it.</p>
      <div class="actions"><a class="btn btn--blue" href="{D.JOIN}">Join the Circle</a></div>
    </div>
  </div>
</section>

<section class="section" id="programme">
  <div class="wrap">
    <div class="sechead">
      <h2>What the Circle covers</h2>
      <p class="lede">Across a semester, part learning, part skills and part simply being together.</p>
    </div>
    <div class="grid grid--3">
      <div class="card">{icon("book")}<h3>Fiqh for women</h3><p>Purity, prayer and fasting, hijab, and the questions people are shy to ask in a mixed room.</p></div>
      <div class="card">{icon("heart")}<h3>Health and wellbeing</h3><p>Sessions led by women with the right training, including how and where to get proper help.</p></div>
      <div class="card">{icon("briefcase")}<h3>Skills and enterprise</h3><p>Practical vocational sessions and small business basics, with space to sell what you make.</p></div>
      <div class="card">{icon("cap")}<h3>Study and career</h3><p>Managing demanding coursework, and hearing from Muslim women working in technical fields.</p></div>
      <div class="card">{icon("shield")}<h3>Safety</h3><p>Recognising harassment, documenting it, and the routes available for reporting and support.</p></div>
      <div class="card">{icon("star")}<h3>Company</h3><p>Games, quizzes, picnics, food and conversation. A community you enjoy is a community you keep.</p></div>
    </div>
  </div>
</section>

<section class="section section--blue">
  <div class="wrap split">
    <div>
      <h2>Part of everything AMSC does</h2>
      <p>Sisters compete in the Musabaqah, serve on the committees, run the indoor games during
      sports weeks, write for the blog, and sit on the Executive Committee through the Ameerah and
      her team.</p>
      <p>Sisters can reach the sisters&rsquo; welfare officers directly on WhatsApp.</p>
      <div class="actions"><a class="btn btn--yellow" href="{D.JOIN}">Register as a member</a></div>
    </div>
    <div class="card">
      {icon("lock")}
      <h3>Photographs and privacy</h3>
      <p>AMSC does not publish a photograph of a sister without her explicit permission. If an image
      of you has been shared and you want it removed, contact the media team and it comes down
      without discussion.</p>
      <div class="card__foot"><a class="link" href="contact.html">Contact the media team</a></div>
    </div>
  </div>
</section>

{band("Bring one sister with you",
      "The Circle grows the way it always has: someone tells a friend the room is warm and the company is good.",
      ("programmes.html", "See all programmes"), ("welfare.html", "Welfare support"))}
'''

# ================================================================== WELFARE
def officer(role, wing, label):
    p = D.holder(role, wing)
    name, dept, level, r, phone, _ = p
    return f'''<article class="officer">
  <span class="mono{' mono--sister' if wing == 's' else ''}" aria-hidden="true">{D.initials(name)}</span>
  <p class="kicker">{pill(label)}</p>
  <h3>{name}</h3>
  <p class="officer__meta">{r}, {dept}, {level}</p>
  <div class="actions">
    <a class="btn btn--green" href="{D.officer_wa(role, wing)}" target="_blank" rel="noopener">{icon("whatsapp")}Chat on WhatsApp<span class="sr-only"> with {name} (opens WhatsApp)</span></a>
    <a class="btn btn--line" href="tel:{D.tel(phone)}">{icon("phone")}Call {D.pretty_phone(phone)}</a>
  </div>
</article>'''

assistants = "".join(person(D.holder(r, w), show_wing=True) for r, w in (("Asst. Welfare Officer I", "b"), ("Asst. Welfare Officer II", "s")))

WELFARE = pagehead("Welfare",
  "Your welfare officers help students settle in and find their way through campus life. "
  "Reach them directly on WhatsApp.") + f'''
<section class="section">
  <div class="wrap">
    <div class="sechead">
      <h2>Talk to a welfare officer</h2>
      <p class="lede">To help students with day-to-day life in the school environment, the welfare
      officers are available to assist to the best of their capacity. Brothers can message the
      brothers&rsquo; officer and sisters the sisters&rsquo; officer.</p>
    </div>
    <div class="officers">
      {officer("Welfare Officer I", "b", "For brothers")}
      {officer("Welfare Officer II", "s", "For sisters")}
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="sechead sechead--split">
      <div>
        <h2>Assistant welfare officers</h2>
        <p class="lede mb-0">If the welfare officer is unavailable, call an assistant.</p>
      </div>
      <p class="muted">Nominees for the {D.SESSION} session.</p>
    </div>
    <ul class="people grid grid--2">{assistants}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sechead">
      <h2>How the welfare team helps</h2>
      <p class="lede">Looking out for one another is part of being one community.</p>
    </div>
    <div class="grid grid--4">
      <div class="card">{icon("compass")}<h3>Settling in</h3><p>Guidance for new students on clearance, hostels, where to pray and how campus works.</p></div>
      <div class="card">{icon("heart")}<h3>Sick visits</h3><p>If a member is admitted or unwell in the hostel, tell a welfare officer so the community can visit.</p></div>
      <div class="card">{icon("gift")}<h3>Ramadan and Eid</h3><p>Iftar for students on campus, and a shared Eid meal for everyone who could not travel home.</p></div>
      <div class="card">{icon("shield")}<h3>The right help</h3><p>For anything beyond the team, the officers point you to the right office or professional.</p></div>
    </div>
    <div class="notice mt-m">{icon("alert")}<p><strong>Medical emergency?</strong> Go straight to the
    Institute&rsquo;s health facility first, then let a welfare officer know.</p></div>
  </div>
</section>

{band("Know a new student who could use a guide?",
      "Point them to a welfare officer. A short WhatsApp message is all it takes.",
      (D.officer_wa("Welfare Officer I", "b"), "Brothers&rsquo; officer on WhatsApp"),
      (D.officer_wa("Welfare Officer II", "s"), "Sisters&rsquo; officer on WhatsApp"))}
'''

# ================================================================== LIBRARY
LIBRARY = pagehead("Library",
  "Notes, reading lists and reference material from AMSC programmes, kept in one place "
  "so nothing is lost when a session ends.") + f'''
<section class="section">
  <div class="wrap">
    <div class="sechead">
      <h2>What is in the library</h2>
    </div>
    <div class="grid grid--3">
      <article class="card">{icon("book")}<h3>Islamiyya notes</h3>
        <p>Notes from the weekend classes, by subject: Tawheed, Fiqh, Seerah and Arabic. Useful if you
        missed a week or want to revise.</p>
        <div class="card__foot">{ext(D.mudeer_wa(), "Ask the Mudeer for access", "link")}</div></article>
      <article class="card">{icon("quran")}<h3>Qur&rsquo;an resources</h3>
        <p>Tajwid guides, memorisation plans and the Musaffa reading schedule.</p>
        <div class="card__foot"><a class="link" href="programmes.html#musaffa">About Musaffa</a></div></article>
      <article class="card">{icon("cap")}<h3>Past questions</h3>
        <p>The academic collection lives in its own shared folder, sorted by department and level.</p>
        <div class="card__foot">{ext(D.PQ, "Open the past question bank", "link")}</div></article>
      <article class="card">{icon("pen")}<h3>Reading lists</h3>
        <p>Short, checked lists for people at different stages: three books, not thirty, so you might
        finish one.</p>
        <div class="card__foot"><a class="link" href="#reading">See the lists</a></div></article>
      <article class="card">{icon("mosque")}<h3>Book shelf</h3>
        <p>Donated books held by the community and lent to members on a signed register. Return what
        you borrow.</p>
        <div class="card__foot"><a class="link" href="#contribute">Donate a book</a></div></article>
    </div>
  </div>
</section>

<section class="section section--mist" id="reading">
  <div class="wrap">
    <div class="sechead">
      <h2>Reading lists by stage</h2>
      <p class="lede">Specific titles are recommended by the Da&rsquo;wah team and the Islamiyya
      teachers, and checked before anything is added.</p>
    </div>
    <div class="grid grid--3">
      <div class="card"><p class="kicker">{pill("New to studying", "mist")}</p><h3>Foundations</h3>
        <ul class="meta"><li>{icon("book")}A clear translation of the Qur&rsquo;an with brief commentary</li><li>{icon("book")}A short, reliable text on the basics of belief</li><li>{icon("book")}A concise Seerah of the Prophet ﷺ</li></ul></div>
      <div class="card"><p class="kicker">{pill("Building", "mist")}</p><h3>Practice and character</h3>
        <ul class="meta"><li>{icon("book")}A fiqh manual covering purification and prayer</li><li>{icon("book")}A collection of forty hadith with explanation</li><li>{icon("book")}A work on purification of the heart</li></ul></div>
      <div class="card"><p class="kicker">{pill("Going further", "mist")}</p><h3>Depth</h3>
        <ul class="meta"><li>{icon("book")}Tafsir of selected surahs</li><li>{icon("book")}Arabic grammar for readers of the Qur&rsquo;an</li><li>{icon("book")}Islamic history beyond the early period</li></ul></div>
    </div>
  </div>
</section>

<section class="section" id="contribute">
  <div class="wrap split">
    <div>
      <h2>Help the library grow</h2>
      <p>The fastest way to make this collection useful is for members to add to it. Two things are
      always welcome:</p>
      <ul>
        <li><strong>Notes:</strong> if you take good notes at Islamiyya, send a scan.</li>
        <li><strong>Books:</strong> physical copies you have finished with, for the shelf.</li>
      </ul>
      <div class="actions"><a class="btn btn--blue" href="join.html#volunteer-form">Offer to contribute</a></div>
    </div>
    <div class="card card--mist">
      {icon("shield")}
      <h3>How material is checked</h3>
      <p>Nothing is added on a whim. Anything that teaches religion is reviewed by the Da&rsquo;wah team
      first, and where scholars differ, the collection presents the mainstream positions rather than
      a single verdict.</p>
      <p>If you think something in the library is wrong or poorly sourced, tell us and it will be
      looked at properly.</p>
      <div class="card__foot"><a class="link" href="contact.html">Flag an item</a></div>
    </div>
  </div>
</section>

{band("Knowledge that is not written down leaves with the class of that year",
      "Every note and reading list here exists because a student took ten minutes to send it in.",
      ("#contribute", "Add to the library"), ("blog.html", "Read Blog"))}
'''
