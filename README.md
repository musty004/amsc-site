# AMSC Website and Student Portal

The official website of the AFIT Muslim Students' Community (AMSC), Air Force Institute of Technology, Kaduna, with a student portal for the Islamiyyah classes and the Dawrah.

**Live site:** [afitmsc.com.ng](https://afitmsc.com.ng) &nbsp;·&nbsp; **Student Portal:** [afitmsc.com.ng/portal](https://afitmsc.com.ng/portal)

Designed, built and maintained by **Muhammadmustapha Yusuf**.

![AMSC website home page](screenshots/website.jpg)

## The website

More than 20 pages for the community: programmes, events, the executive committee, a freshers' guide, gallery, blog, sisters' and welfare pages, and contact.

- Live prayer times for Kaduna in the top bar, with a countdown to the next prayer
- Registration forms (membership and Dawrah) embedded in the page, so nobody has to leave the site
- Dues payment details with a one-tap copy button
- Islamiyyah books available to download as PDFs
- Designed for phones first, since that is how most students visit

![The website on a phone](screenshots/website-mobile.png)

## The Student Portal

Students, teachers and admins each get their own area, and people only see the programme they belong to.

**Students** record what they memorise and revise in the Qur'an and see their progress by juz and by surah. They can also follow their Arabic class's progress through the textbook, see the timetable, their teachers and classmates, and read announcements.

![Student portal on a phone](screenshots/portal-student.png)

**Teachers** verify their students' Qur'an records, give assessments with feedback, update their Arabic class's progress and post notices to their groups.

![Teacher view](screenshots/portal-teacher.png)

**Admins** approve new accounts, create classes, assign teachers and manage the library.

![Admin overview](screenshots/portal-admin.png)

**The Dawrah** (an intensive hadith course) has its own section. Registered students listen to each class recording and answer two short questions that are marked straight away. The right answers show after they submit, and there is a final exam at the end.

![Dawrah student view](screenshots/portal-dawrah.png)

The Dawrah team gets a follow-up table showing who has logged in and who is falling behind. It has a WhatsApp button with a ready-written reminder for each student and a spreadsheet export.

![Dawrah follow-up table](screenshots/portal-dawrah-admin.png)

*Screenshots use made-up demo students.*

## How it is built

- **HTML, CSS and JavaScript**, with no framework. Pages are generated from Python templates in `_source/`, so the header, footer, menus and shared details live in one place.
- **Supabase** (PostgreSQL, authentication and file storage) powers the portal. Access rules are enforced inside the database with row-level security, so a student can only read their own records, and classmates see names only.
- **Netlify** hosts the site on a custom domain with HTTPS. Every push to this repository goes live automatically.
- **Light and fast** on low-end phones and slow mobile data: small pages, no heavy libraries, optimised images and long-term caching.
- **Accessible:** keyboard navigation, screen-reader labels and colour contrast checked against WCAG 2.1 AA.

## Project structure

```
_source/           Python templates and site content (edit here, then rebuild)
_source/portal/    Database setup for the Student Portal (setup.sql)
assets/            Styles, scripts, images and downloadable books
*.html             Generated pages (do not edit by hand)
netlify.toml       Hosting settings
```

To rebuild the pages after a change:

```
cd _source
python3 build.py
```

## About AMSC

AMSC is a faith-driven student body that supports Muslim students at AFIT through worship, learning, welfare and service. Together in Faith and Purpose.

Instagram: [@afitmsc](https://instagram.com/afitmsc) &nbsp;·&nbsp; Email: Afitmssn@gmail.com

Please do not publish photographs of sisters without their permission.

## Work with me

I build websites and web apps for schools, communities and businesses, from simple sites to portals with logins and dashboards.

WhatsApp: [+234 708 411 1381](https://wa.me/2347084111381) &nbsp;·&nbsp; GitHub: [@musty004](https://github.com/musty004)
