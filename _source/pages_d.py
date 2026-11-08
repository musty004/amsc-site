import data as D
import shell
from shell import icon, img, ar, pill, ext, band, pagehead, formspree_form, mail_link, soon
from pages_b import flyer

# ================================================================== GALLERY
def photo(name, alt, caption, pos=None, eager=False):
    style = f"object-position:{pos}" if pos else ""
    return f'<figure class="photo">{img(name, alt, "(min-width: 960px) 380px, (min-width: 640px) 50vw, 100vw", style=style, eager=eager)}<figcaption>{caption}</figcaption></figure>'

GALLERY = pagehead("Gallery",
  "Moments from AMSC programmes: lectures, the Musabaqatul Qur&rsquo;an, orientation, sports and "
  "community gatherings.") + f'''
<section class="section">
  <div class="wrap">
    <div class="sechead">
      <h2>Photographs by event</h2>
      <p class="lede">Moments from our programmes, grouped by event. Full albums open in Google Photos.</p>
    </div>
    <nav class="jump" aria-label="Events in the gallery"><ul>
      <li><a href="#g-orientation">Freshers&rsquo; Orientation</a></li>
      <li><a href="#g-musabaqah">Musabaqatul Qur&rsquo;an</a></li>
      <li><a href="#g-walimah">FYB Sendforth Walimah</a></li>
      <li><a href="#g-community">Community and sports</a></li>
      <li><a href="#flyers">Flyer archive</a></li>
    </ul></nav>

    <section class="gal-cat" id="g-orientation" aria-labelledby="g-orientation-h">
      <div class="gal-cat__head">
        <div><h3 id="g-orientation-h">Freshers&rsquo; Orientation</h3><p>Welcoming new Muslim students to AFIT each session.</p></div>
        {ext(D.ALBUM_ORIENTATION_2025, "2025/1447 album", "btn btn--blue btn--sm")}
      </div>
      <p class="gal-cat__year">{pill("2025/1447")} 8 November 2025, Mosugu Hall</p>
      <div class="photos photos--2">
        {photo("orientation-2025-sisters", "New sisters listening at the 2025/1447 Freshers' Orientation", "Sisters at the 2025/1447 orientation", eager=True)}
        {photo("orientation-2025-brothers", "New brothers seated in the hall at the 2025/1447 Freshers' Orientation", "Brothers at the 2025/1447 orientation")}
        {photo("orientation-2025-hall", "Brothers listening to a talk at the 2025/1447 Freshers' Orientation", "Taking in the talks")}
        {photo("orientation-2025-speaker", "A speaker addressing new students at the 2025/1447 Freshers' Orientation", "A speaker addresses the freshers", "50% 28%")}
      </div>
      <a class="album-card" href="{D.ALBUM_ORIENTATION_2025}" target="_blank" rel="noopener">
        {pill("2025/1447")}<span><b>See every photograph from the 2025/1447 orientation</b><span>The full album on Google Photos</span></span>{icon("external")}<span class="sr-only"> (opens in a new tab)</span>
      </a>
      <p class="gal-cat__year mt-l">{pill("2024/1446")}</p>
      <div class="photos photos--2">
        {photo("orientation-2024-sisters", "New sisters seated in the lecture hall at the 2024/1446 Freshers' Orientation", "Sisters at the 2024/1446 orientation")}
        {photo("orientation-2024-brothers", "New brothers seated in the lecture hall at the 2024/1446 Freshers' Orientation", "Brothers at the 2024/1446 orientation")}
        {photo("orientation-2024-hall", "A full lecture hall at the 2024/1446 Freshers' Orientation", "A full hall for the 2024/1446 orientation")}
        {photo("orientation-2024-front", "Brothers listening at the 2024/1446 Freshers' Orientation", "Listening to the orientation talks")}
      </div>
    </section>

    <section class="gal-cat" id="g-musabaqah" aria-labelledby="g-musabaqah-h">
      <div class="gal-cat__head">
        <div><h3 id="g-musabaqah-h">5th Annual Musabaqatul Qur&rsquo;an</h3><p>Preliminaries and the grand finale at the Ibrahim Alfa Hall, 9 May 2026.</p></div>
        {ext(D.ALBUM_MUSABAQAH, "Full album", "btn btn--blue btn--sm")}
      </div>
      <figure class="photo photo--feature">{img("musabaqah-finale", "The auditorium during the grand finale of the 5th Musabaqatul Qur'an, with the judges on stage and the Qur'an text on screen", "(min-width: 960px) 1140px, 100vw")}<figcaption>The grand finale: judges on stage, the Qur&rsquo;an text on screen, and a full hall</figcaption></figure>
      <div class="photos mt-s">
        {photo("musabaqah-award", "An award plaque presented to the chief judge at the Musabaqatul Qur'an", "An award for the chief judge")}
        {photo("musabaqah-team", "Brothers on the stage at the Musabaqatul Qur'an", "Brothers on the Musabaqah stage", "50% 40%")}
        {photo("musabaqah-judges", "The judging panel at the Musabaqatul Qur'an", "The judges at work")}
        {photo("musabaqah-sisters", "Sisters in the audience at the Musabaqatul Qur'an", "Sisters in the audience")}
        {photo("musabaqah-audience", "Sisters following the recitations at the Musabaqatul Qur'an", "Following the recitations")}
        {photo("quiz-mosque", "A recitation session in the mosque during the Musabaqah preliminaries", "Preliminary round in the mosque")}
      </div>
    </section>

    <section class="gal-cat" id="g-walimah" aria-labelledby="g-walimah-h">
      <div class="gal-cat__head">
        <div><h3 id="g-walimah-h">FYB Sendforth Walimah</h3><p>Sending forth our final-year brothers and sisters, with invited guests.</p></div>
        <a class="btn btn--line btn--sm" href="events.html#sendforth">About the Walimah</a>
      </div>
      <figure class="photo photo--feature">{img("walimah-group", "AMSC members and invited guests at the FYB Sendforth Walimah, photographed in front of the auditorium", "(min-width: 960px) 900px, 100vw")}<figcaption>Brothers (top) and sisters (bottom) with guests at the FYB Sendforth Walimah</figcaption></figure>
    </section>

    <section class="gal-cat" id="g-community" aria-labelledby="g-community-h">
      <div class="gal-cat__head">
        <div><h3 id="g-community-h">Community and sports</h3><p>Everyday moments across the session.</p></div>
        {ext(D.IG, "More on Instagram", "btn btn--line btn--sm")}
      </div>
      <div class="photos photos--2">
        {photo("community-group", "Brothers and sisters of AMSC standing together on campus", "Brothers and sisters of AMSC on campus")}
        {photo("football-team", "The AMSC football team on the pitch", "The AMSC football team", "50% 35%")}
      </div>
    </section>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="sechead">
      <h2>Albums and channels</h2>
      <p class="lede">Every photograph from our major programmes, and coverage as it happens.</p>
    </div>
    <div class="grid grid--4">
      <a class="card" href="{D.ALBUM_ORIENTATION_2025}" target="_blank" rel="noopener">{icon("camera")}<h3>Freshers&rsquo; Orientation 2025/1447</h3><p>The full album from the orientation on 8 November 2025.</p><span class="sr-only"> (opens in a new tab)</span></a>
      <a class="card" href="{D.ALBUM_MUSABAQAH}" target="_blank" rel="noopener">{icon("quran")}<h3>Musabaqatul Qur&rsquo;an</h3><p>The full album from the fifth edition, 9 May 2026.</p><span class="sr-only"> (opens in a new tab)</span></a>
      <a class="card" href="{D.IG}" target="_blank" rel="noopener">{icon("instagram")}<h3>Instagram</h3><p>Announcements, recaps and recitation highlights, {D.IG_HANDLE}.</p><span class="sr-only"> (opens in a new tab)</span></a>
      <a class="card" href="{D.FB}" target="_blank" rel="noopener">{icon("facebook")}<h3>Facebook</h3><p>Longer posts and event albums for the wider community.</p><span class="sr-only"> (opens in a new tab)</span></a>
    </div>
    <p class="note">Photographs of sisters are published only with the permission of the sisters photographed.</p>
  </div>
</section>

<section class="section" id="flyers">
  <div class="wrap">
    <div class="sechead">
      <h2>Flyer archive</h2>
      <p class="lede">Announcements designed by the AMSC media team.</p>
    </div>
    <div class="flyers">
      {flyer("flyer-welfare-officers", "Welcome to AFIT: welfare officers' contacts", "Welcome", "Welfare officers", "Contacts for new students.")}
      {flyer("flyer-freshers", "Freshers' Orientation flyer", "8 November 2025", "Freshers&rsquo; Orientation", "Navigating campus, guided by Islam in every step.")}
      {flyer("flyer-matriculation", "Congratulations on your matriculation flyer", "Milestones", "Matriculation", "Welcoming new students to the Institute.")}
      {flyer("flyer-idit", "IDIT 3.0 flyer", "December 2025", "IDIT 3.0", "Four tracks, four weeks, fully online.")}
      {flyer("flyer-idit-graduation", "IDIT graduation ceremony flyer", "21 February 2026", "IDIT graduation", "Beyond the Degree: positioning for the AI era.")}
      {flyer("flyer-hijabday", "World Hijab Day 2026 flyer", "February 2026", "World Hijab Day", "More Than A Scarf.")}
      {flyer("flyer-sisters-circle", "The Sisters Circle flyer", "Fridays", "Sisters Circle", "Vocational training, quizzes, games, picnics.")}
      {flyer("flyer-musabaqah", "5th Annual Musabaqatul Qur'an invitation", "9 May 2026", "5th Musabaqatul Qur&rsquo;an", "Grand finale, Ibrahim Alfa Hall.")}
      {flyer("flyer-sendforth", "FYB Sendforth Walimah flyer", "4 July 2026", "FYB Sendforth Walimah", "Networking, games, awards and giveaways.")}
      {flyer("flyer-convocation", "Convocation congratulations flyer", "Milestones", "Convocation", "Marking the graduation of AMSC members.")}
      {flyer("flyer-aman", "AMAN launch flyer", "Launch", "AMAN", "The AFIT Muslim Alumni Network.")}
      {flyer("flyer-pdfnest", "PDFNest partnership announcement", "Partnership", "PDFNest", "Partnered to make your studies better.", "academics.html#pdfnest")}
      {flyer("flyer-askbox", "Ask us that question on Islam flyer", "All session", "Ask a question", "Anonymous questions, answered in session.")}
    </div>
  </div>
</section>

<section class="section section--mist" id="brand">
  <div class="wrap split">
    <div>
      <h2>For designers</h2>
      <p>Making a flyer for an AMSC programme? Use the official palette and fonts. One community,
      one look: it is how people recognise an announcement as ours before they read a word.</p>
      <ul class="meta">
        <li>{icon("download")}Logo files, for light and dark backgrounds</li>
        <li>{icon("download")}Flyer and announcement templates</li>
        <li>{icon("download")}Certificate templates for the Musabaqah and IDIT</li>
      </ul>
      <div class="actions"><a class="btn btn--blue" href="mailto:{D.EMAIL}?subject=Request%20for%20the%20AMSC%20brand%20kit">Request the brand kit</a></div>
    </div>
    <div class="card">
      <h3>Palette and type</h3>
      <ul class="swatches">
        <li><span style="background:#0056CE"></span><b>Primary blue</b>#0056CE</li>
        <li><span style="background:#FCBA00"></span><b>Yellow</b>#FCBA00</li>
        <li><span style="background:#18C021"></span><b>Green</b>#18C021</li>
        <li><span style="background:#FFFFFF;box-shadow:inset 0 0 0 1px var(--line)"></span><b>White</b>#FFFFFF</li>
      </ul>
      <p class="mt-s"><strong class="type-sample">Clash Display</strong> for headlines.
      <strong>DM Sans</strong> for body text, at &minus;3% letter spacing.</p>
      <p class="mb-0">Blue leads. Yellow and green are accents.</p>
    </div>
  </div>
</section>

<section class="section section--blue">
  <div class="wrap split">
    <div>
      <h2>Before you post</h2>
      <p>Nobody is photographed for publication without knowing. No image of a sister is published
      without her explicit permission. Anyone can ask for a photograph of themselves to be taken down,
      and it comes down without argument.</p>
      <p>Photographs of guests and officials are cleared with them first, and no coverage of an
      Institute facility is published without the Institute&rsquo;s approval.</p>
    </div>
    <div class="card">
      {icon("camera")}
      <h3>Join the media team</h3>
      <p>Photographers, video editors, designers and developers. If you can hold a camera steady or
      push a commit, there is work for you here.</p>
      <div class="card__foot"><a class="link" href="join.html#volunteer">Volunteer</a></div>
    </div>
  </div>
</section>
'''

# ================================================================== BLOG
def cat(ico, name, text, href):
    return f'<li><a href="{href}">{icon(ico)}<span><b>{name}</b><span>{text}</span></span></a></li>'

BLOG = pagehead("Blog",
  "Islamic reminders, student articles, community news, event reports and learning resources "
  "from the AFIT Muslim Students&rsquo; Community.") + f'''
<section class="section">
  <div class="wrap split">
    {soon("Publications coming soon", "Our publications and updates will be available soon. Until then, short reminders and recaps are below, and announcements go out on Instagram and the WhatsApp Community.")}
    <div class="prog-group">
      <h2>What you will find here</h2>
      <ul>
        {cat("quran", "Islamic reminders", "Short reminders for the days and seasons of the year.", "#reminders")}
        {cat("pen", "Student articles", "Reflections and essays written by members.", "#write")}
        {cat("cap", "Academic resources", "Study tips, past questions and scholarship notices.", "academics.html")}
        {cat("users", "Community news", "What AMSC is doing this session.", "events.html")}
        {cat("camera", "Event reports", "Recaps and photographs from our programmes.", "gallery.html")}
        {cat("book", "Qur&rsquo;an and Islamic learning", "Notes and reading lists.", "library.html")}
      </ul>
    </div>
  </div>
</section>

<section class="section section--mist" id="reminders">
  <div class="wrap split split--sidebar">
    <div class="stack">
      <h2>From the community</h2>
      <article class="card">
        <p class="kicker">{pill("Event report", "mist")}</p>
        <h3>Relive the 5th Annual Musabaqatul Qur&rsquo;an</h3>
        <p>From the recitations to the moments captured through the day: the full photo album from
        the grand finale at the Ibrahim Alfa Hall on 9 May 2026. May Allah reward everyone who took
        part and everyone who worked behind it.</p>
        <div class="card__foot">{ext(D.ALBUM_MUSABAQAH, "Browse the album", "link")}</div>
      </article>
      <article class="card">
        <p class="kicker">{pill("Reminder", "mist")}</p>
        <h3>The virtues and etiquette of Yawm al-Jumu&rsquo;ah</h3>
        <p>Friday is described as the best day on which the sun rises. The recommended practice is
        well documented: ghusl before setting out, going early, wearing your best clothes and
        perfume, not causing anyone difficulty, reciting Surah Al-Kahf, and listening attentively
        to the khutbah.</p>
        <div class="card__foot"><a class="link" href="salah.html">Friday at AFIT</a></div>
      </article>
      <article class="card">
        <p class="kicker">{pill("Reminder", "mist")}</p>
        <h3>The first ten days of Dhul-Hijjah</h3>
        <p>Among the days most beloved to Allah for righteous deeds. The recommended acts through
        the first nine days include fasting, especially the Day of Arafah for those not on Hajj,
        abundant takbir, tahlil and tahmid, and increasing every kind of good deed.</p>
        <div class="card__foot"><a class="link" href="library.html">Read more in the library</a></div>
      </article>
      <article class="card">
        <p class="kicker">{pill("Community news", "mist")}</p>
        <h3>The brotherhood outlives the campus</h3>
        <p>Pioneers and founding members of AMSC still meet years after graduation, in Abuja and
        elsewhere, while serving in different places. AMSC was never only a campus organisation; it
        follows its members wherever Allah places them.</p>
        <div class="card__foot"><a class="link" href="alumni.html">The AMAN alumni network</a></div>
      </article>
    </div>
    <aside class="stack" id="write">
      <div class="card">
        {icon("pen")}
        <h3>Write for AMSC</h3>
        <p>Event reports, reflections, interviews and reminders. If you can write clearly, this
        page is open to you.</p>
        <div class="card__foot"><a class="link" href="join.html#volunteer-form">Offer to write</a></div>
      </div>
      <div class="card">
        {icon("shield")}
        <h3>Editorial standard</h3>
        <p>Anything quoting the Qur&rsquo;an or hadith is checked and referenced before publication.
        Nothing is published in the community&rsquo;s name without an editor&rsquo;s review.</p>
      </div>
      <div class="card">
        {icon("whatsapp")}
        <h3>Announcements</h3>
        <p>What is on this week, reminders and academic updates go out on the AMSC WhatsApp Community.</p>
        <div class="card__foot"><a class="link" href="{D.JOIN}">Register to join</a></div>
      </div>
    </aside>
  </div>
</section>

{band("Sections waiting for writers",
      "Interviews with graduating members, department profiles, a poetry corner and a faith and technology column.",
      ("join.html#volunteer", "Write for the blog"), ("gallery.html", "See the gallery"))}
'''

# ================================================================== GIVE
GIVE = pagehead("Give",
  "Semester dues, the welfare fund and support for specific projects, with an account of how "
  "funds are used.") + f'''
<section class="section" id="dues">
  <div class="wrap split split--sidebar">
    <div>
      <p class="kicker">{pill(D.SESSION + " session")} Once a semester</p>
      <h2>Pay your semester dues</h2>
      <p class="lede">Dues of <strong>{D.DUES_AMOUNT}</strong> keep the weekly programmes running and
      strengthen our community.</p>
      <section class="paycard" aria-labelledby="pay-h">
        <h3 id="pay-h" class="paycard__h">Payment details</h3>
        <dl class="paycard__list">
          <div><dt>Account number</dt>
            <dd class="paycard__num"><span id="dues-acct">{D.DUES_ACCOUNT_NUMBER}</span>
            <button type="button" class="btn btn--sm btn--blue paycard__copy" data-copy="{D.DUES_ACCOUNT_NUMBER}" aria-describedby="dues-acct">Copy<span class="sr-only"> account number</span></button></dd></div>
          <div><dt>Account name</dt><dd>{D.DUES_ACCOUNT_NAME}</dd></div>
          <div><dt>Bank</dt><dd>{D.DUES_BANK}</dd></div>
        </dl>
        <p class="paycard__note">The account belongs to the AMSC Financial Officer. Use your full name as the
        transfer description so the payment can be matched to you.</p>
      </section>
      <p>Prefer to pay with a card? Use the online payment link.</p>
      <div class="actions">{ext(D.DUES, "Pay dues online", "btn btn--line")}</div>
      <p class="mt-m">If dues are difficult for you this semester, your membership continues unchanged. Nobody is
      removed for not paying. {ar("جزاكم الله خيرا")}: may Allah reward you for your support.</p>
    </div>
    <figure class="framed give-flyer">{img("flyer-dues", f"Semester dues flyer. Payment details: account number {D.DUES_ACCOUNT_NUMBER}, account name {D.DUES_ACCOUNT_NAME}, {D.DUES_BANK}.", "(min-width: 960px) 400px, 92vw")}</figure>
  </div>
</section>

<section class="section section--tight section--flush">
  <div class="wrap grid grid--2">
    <div class="card" id="welfare">
      {icon("heart")}
      <h3>The welfare fund</h3>
      <p>Goes directly to students who need help with food, transport, medical care or academic
      costs. Any amount.</p>
      <div class="card__foot">{ext(D.DUES, "Give to welfare", "btn btn--blue btn--sm")}</div>
    </div>
    <div class="card">
      {icon("gift")}
      <h3>Sadaqah and zakat</h3>
      <p>Zakat is given only to eligible recipients, kept separate from general funds and accounted
      for separately.</p>
      <div class="card__foot"><a class="btn btn--line btn--sm" href="mailto:{D.EMAIL}?subject=Sadaqah%20and%20zakat">Speak to the finance team</a></div>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="sechead">
      <h2>What we are raising for</h2>
      <p class="lede">People give to specific things. Each project has a purpose, a target published
      when it opens, and a report when it is done.</p>
    </div>
    <div class="grid grid--3">
      <div class="card"><p class="kicker">{pill("Open")}</p><h3>Musabaqah prize fund</h3><p>Prizes and certificates for every category of the annual Qur&rsquo;an competition.</p></div>
      <div class="card"><p class="kicker">{pill("Open")}</p><h3>Islamiyyah materials</h3><p>Copies of the Qur&rsquo;an, whiteboards, printed notes and teaching materials for the weekend classes.</p></div>
      <div class="card"><p class="kicker">{pill("Open")}</p><h3>Ramadan iftar</h3><p>Daily iftar for students who stay on campus through the month, and the Annual Ramadan Lecture and Iftar.</p></div>
    </div>
  </div>
</section>

<section class="section" id="transparency">
  <div class="wrap split split--sidebar">
    <div>
      <h2>How funds are accounted for</h2>
      <p>Accounts are kept by the Financial Officer and the Financial Secretary and presented to
      members at the general meeting. Two signatures are needed for every disbursement above the
      agreed limit, and every payment has a receipt.</p>
      {soon("Accounts for " + D.SESSION, "Monthly statements of income, spending and balance will be published here.")}
      <h3 class="mt-l">How funds are used</h3>
      <ul>
        <li><strong>Programmes:</strong> Islamiyyah materials, tutorial printing and venue costs.</li>
        <li><strong>Welfare:</strong> direct support to members in need.</li>
        <li><strong>Events:</strong> the Musabaqah, orientation, Eid gatherings and the sendforth.</li>
        <li><strong>Media:</strong> printing, design and this website.</li>
      </ul>
    </div>
    <aside class="card card--mist">
      {icon("shield")}
      <h3>Our rules on money</h3>
      <ul class="meta">
        <li>{icon("users")}No single person can move funds alone</li>
        <li>{icon("pen")}Every disbursement is recorded with a receipt</li>
        <li>{icon("calendar")}Accounts published monthly, without being asked</li>
        <li>{icon("lock")}Welfare reported as totals only, never names</li>
        <li>{icon("star")}Zakat held and given out separately</li>
      </ul>
      <div class="card__foot"><a class="link" href="mailto:{D.EMAIL}?subject=Question%20about%20the%20accounts">Ask about an entry</a></div>
    </aside>
  </div>
</section>

{band("Graduates: keep the door open behind you",
      "A small standing contribution from alumni funds welfare and the Musabaqah more reliably than any single large gift.",
      ("alumni.html#giveback", "Alumni giving"), ("contact.html", "Contact us"))}
'''

# ================================================================== ALUMNI
alumni_form = formspree_form(D.FORMSPREE_ALUMNI, '''
  <div class="field--2">
    <div class="field"><label for="an">Full name</label><input type="text" id="an" name="name" autocomplete="name" required></div>
    <div class="field"><label for="ay">Year you left AFIT</label><input type="text" id="ay" name="year" inputmode="numeric" required></div>
  </div>
  <div class="field--2">
    <div class="field"><label for="ad">Department</label><input type="text" id="ad" name="department"></div>
    <div class="field"><label for="ac">City you live in</label><input type="text" id="ac" name="city"></div>
  </div>
  <div class="field--2">
    <div class="field"><label for="af">Field of work or service</label><input type="text" id="af" name="field" placeholder="e.g. Aerospace, NYSC, postgraduate study"></div>
    <div class="field"><label for="ap">Phone or WhatsApp</label><input id="ap" name="phone" type="tel" autocomplete="tel" required></div>
  </div>
  <div class="field"><label for="ah">How would you like to stay involved?</label>
    <select id="ah" name="involvement"><option>Mentor a student</option><option>Give regularly</option><option>Speak at an event</option><option>Share job and internship openings</option><option>Keep me on the list for now</option></select></div>
  <button class="btn btn--blue" type="submit">Join the register</button>''',
  "Welcome to AMAN",
  "JazakAllahu khayran. You are now on the AFIT Muslim Alumni Network register, and the team will be in touch.",
  "New AMAN alumni registration")

ALUMNI = pagehead("AMAN alumni network",
  "The AFIT Muslim Alumni Network brings together all AFIT Muslim graduates to foster brotherhood, "
  "unity and networking.") + f'''
<section class="section">
  <div class="wrap feature">
    <div class="feature__media"><div class="framed">{img("flyer-aman", "AMAN, the AFIT Muslim Alumni Network, officially launches", "(min-width: 960px) 540px, 100vw")}</div></div>
    <div>
      <p class="kicker">{pill("Officially launched")}</p>
      <h2>A bond that follows you</h2>
      <p>The connection between AMSC members travels far. Pioneers and founding members of the
      community still meet in Abuja and elsewhere, years after leaving Kaduna, while serving in
      different places.</p>
      <p>AMAN makes that deliberate: a register, a way to reach one another, and a way for graduates
      to keep supporting the students who came after them.</p>
    </div>
  </div>
</section>

<section class="section section--blue section--tight">
  <div class="wrap split">
    <div>
      <h2>Brotherhood, unity, networking</h2>
      <p>Three words from the launch, and the whole purpose. Members are AFIT Muslim graduates
      wherever they now are: in service, in postgraduate study, at work or at home.</p>
    </div>
    <div class="card">
      <h3>What alumni do for AMSC</h3>
      <ul class="meta">
        <li>{icon("users")}Mentor students in their own department or field</li>
        <li>{icon("gift")}Support welfare, the Musabaqah and Ramadan iftar</li>
        <li>{icon("mic")}Speak at orientation, career sessions and the sendforth</li>
        <li>{icon("briefcase")}Pass on internships, NYSC advice and job openings</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--mist" id="register">
  <div class="wrap split split--sidebar">
    <div>
      <h2>Join the alumni register</h2>
      <p>Graduating members are inducted at the FYB Sendforth Walimah, and the register is open to
      anyone who passed through AMSC at any point.</p>
      {alumni_form}
    </div>
    <aside class="stack">
      <div class="card" id="mentorship">
        {icon("users")}
        <h3>Mentor a student</h3>
        <p>One student, one conversation a month, matched by department and by what they need.</p>
        <div class="card__foot"><a class="link" href="#register">Sign up to mentor</a></div>
      </div>
      <div class="card" id="jobs">
        {icon("briefcase")}
        <h3>Jobs and internships</h3>
        <p>Openings shared by alumni go to the community. If you can place a student somewhere,
        tell us.</p>
        <div class="card__foot"><a class="link" href="mailto:{D.EMAIL}?subject=Opening%20for%20AMSC%20students">Share an opening</a></div>
      </div>
      <div class="card" id="giveback">
        {icon("gift")}
        <h3>Give back</h3>
        <p>A standing contribution, however small, is worth more to the welfare fund than one large
        gift a year.</p>
        <div class="card__foot"><a class="link" href="give.html">Ways to give</a></div>
      </div>
    </aside>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sechead">
      <h2>How members are sent forth</h2>
      <p class="lede">The FYB Sendforth Walimah closes each session for final-year students.</p>
    </div>
    <div class="grid grid--4">
      <div class="card"><h3>Networking</h3><p>Final-year students, the community they served with, and invited guests.</p></div>
      <div class="card"><h3>Inspiring sessions</h3><p>A keynote address and an impact panel discussion, with time for questions.</p></div>
      <div class="card"><h3>FYB awards</h3><p>Recognition for the finalists, followed by games, refreshments and giveaways.</p></div>
      <div class="card"><h3>Into AMAN</h3><p>Induction into the alumni network, with contact details recorded on the day.</p></div>
    </div>
  </div>
</section>

{band("Wherever Allah has placed you, you are still AMSC",
      "Add yourself to the register and tell us what you can offer the students who are where you were.",
      ("#register", "Join the alumni register"), ("blog.html", "Read Blog"))}
'''

# ================================================================== CONTACT
def both(role_b, role_s=None):
    b = D.holder(role_b, "b")
    names = b[0]
    if role_s:
        s = D.holder(role_s, "s")
        names += f" and {s[0]}"
    return names

contact_form = formspree_form(D.FORMSPREE_CONTACT, '''
  <div class="field--2">
    <div class="field"><label for="cn">Name</label><input type="text" id="cn" name="name" autocomplete="name" required></div>
    <div class="field"><label for="cp">Email or phone</label><input type="text" id="cp" name="contact" required></div>
  </div>
  <div class="field"><label for="ct">What is this about?</label>
    <select id="ct" name="topic"><option>Joining AMSC</option><option>A programme or event</option><option>Academics</option><option>Welfare</option><option>Giving and dues</option><option>Media and the website</option><option>Partnership or invitation</option><option>Something else</option></select></div>
  <div class="field"><label for="cm">Message</label><textarea id="cm" name="message" rows="5" required></textarea></div>
  <button class="btn btn--blue" type="submit">Send message</button>''',
  "Thank you. Your message has been sent.",
  "It has reached the AMSC team, and we will reply by email or phone.",
  "Message from the AMSC website")

CONTACT = pagehead("Contact",
  "Write to AMSC, join the WhatsApp Community, or reach the officer responsible for what you need.") + f'''
<section class="section">
  <div class="wrap">
    <div class="contact-main">
      <div class="contact-email">
        {icon("mail")}
        <h2>Email</h2>
        <p>The official address for correspondence, partnerships and anything formal.</p>
        <a class="contact-email__addr" href="mailto:{D.EMAIL}">{D.EMAIL}</a>
      </div>
      <div class="contact-wa">
        {icon("whatsapp")}
        <h2>WhatsApp Community</h2>
        <p>Announcements, academic updates, clearance guides and peer support. Register with AMSC
        and an admin will add you to the community.</p>
        <div class="actions mt-s"><a class="btn btn--yellow" href="{D.JOIN}">Register to join</a></div>
      </div>
    </div>
    <div class="grid grid--3 mt-m">
      <div class="card">
        {icon("instagram")}
        <h3>Instagram</h3>
        <p>Event coverage, announcements and recitation highlights.</p>
        <div class="card__foot">{ext(D.IG, D.IG_HANDLE, "link")}</div>
      </div>
      <div class="card">
        {icon("facebook")}
        <h3>Facebook</h3>
        <p>Longer posts and event albums for the wider community.</p>
        <div class="card__foot">{ext(D.FB, "AMSC on Facebook", "link")}</div>
      </div>
      <div class="card">
        {icon("pin")}
        <h3>Find us</h3>
        <p>AFIT Mosque, Air Force Institute of Technology, Kaduna. Easiest after any congregational prayer.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="sechead">
      <h2>Reach the right person</h2>
      <p class="lede">Nominees for the {D.SESSION} session. Phone numbers are on the
      <a href="executive.html">Executive Committee</a> page.</p>
    </div>
    <div class="table-wrap">
      <table class="table">
        <thead><tr><th scope="col">If you need</th><th scope="col">Ask</th><th scope="col">Where</th></tr></thead>
        <tbody>
          <tr><td>To register as a member</td><td>General Secretaries: {both("Gen Secretary I", "Gen Secretary II")}</td><td><a href="join.html#register">Registration form</a></td></tr>
          <tr><td>A letter of attestation</td><td>General Secretaries</td><td>{mail_link()}</td></tr>
          <tr><td>Tutorials or past questions</td><td>Academics Coordinators: {both("Academics Coordinator I", "Academics Coordinator II")}</td><td><a href="academics.html">Academics</a></td></tr>
          <tr><td>Welfare support</td><td>Welfare Officers: {both("Welfare Officer I", "Welfare Officer II")}</td><td><a href="welfare.html">Welfare</a></td></tr>
          <tr><td>Dues or the accounts</td><td>{both("Financial Officer", "Financial Secretary II")}</td><td><a href="give.html">Give</a></td></tr>
          <tr><td>Anything on the sisters&rsquo; side</td><td>Ameerah: {D.holder("Ameerah", "s")[0]}</td><td><a href="sisters.html">Sisters</a></td></tr>
          <tr><td>A question about Islam</td><td>Da&rsquo;wah Coordinators: {both("Da’wah Coordinator", "Da’wah Coordinator II")}</td><td>{ext(D.ASKBOX, "Anonymous question box")}</td></tr>
          <tr><td>Programmes and logistics</td><td>Chief Organizers: {both("Chief Organizer I", "Chief Organizer II")}</td><td><a href="programmes.html">Programmes</a></td></tr>
          <tr><td>Photos, design or this website</td><td>Media Coordinators: {both("Media Coordinator I", "Media Coordinator II")}</td><td><a href="gallery.html">Gallery</a></td></tr>
          <tr><td>A lost or found item</td><td>Amanah Desk Officer</td><td><a href="amanah.html">Amanah Desk</a></td></tr>
          <tr><td>Partnerships and invitations</td><td>Ameer: {D.holder("Ameer", "b")[0]}</td><td>{mail_link()}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--sidebar">
    <div>
      <h2>Send a message</h2>
      <p>Messages go to the AMSC team and are answered by email or phone.</p>
      {contact_form}
    </div>
    <aside class="stack">
      <div class="card">
        {icon("shield")}
        <h3>Raising a concern</h3>
        <p>If something in the community needs to be raised confidentially, contact the Ameer or
        Ameerah directly. Concerns about conduct are taken seriously and handled discreetly.</p>
      </div>
      <div class="card">
        {icon("whatsapp")}
        <h3>Community WhatsApp line</h3>
        <p>For quick questions, message {D.WA_LINE_DISPLAY} and you will be pointed to the right person.</p>
        <div class="card__foot">{ext(D.wa_text("Assalamu alaykum, I would like to know more about AMSC."), "Message the line", "link")}</div>
      </div>
    </aside>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <h2>Frequently asked</h2>
    <div class="mt-m">
      <details class="faq"><summary>What does AMSC stand for?</summary><p>The AFIT Muslim Students&rsquo; Community: the body serving Muslim students at the Air Force Institute of Technology, Kaduna.</p></details>
      <details class="faq"><summary>Who can join?</summary><p>Every Muslim student of the Institute, at any level and in any department. The IDIT training cohorts are also open to people outside AFIT.</p></details>
      <details class="faq"><summary>How do I pay my dues?</summary><p>By bank transfer to the account on the <a href="give.html#dues">Give</a> page, or online with a card through the payment link on the same page. Dues are &#8358;1,000 and above per semester.</p></details>
      <details class="faq"><summary>Can I get a letter of attestation for a scholarship?</summary><p>Yes. Email the General Secretaries at {D.EMAIL} with your name, department, level and the scholarship, and allow a few days.</p></details>
      <details class="faq"><summary>How do I invite AMSC to an event or propose a partnership?</summary><p>Email {D.EMAIL}, addressed to the Ameer. Programmes involving external guests go through Institute clearance, so allow time.</p></details>
    </div>
  </div>
</section>
'''
