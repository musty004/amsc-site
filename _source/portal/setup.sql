-- =============================================================================
-- AMSC Islamiyyah Student Portal: database setup (Supabase)
--
-- How to use: Supabase dashboard > SQL Editor > New query > paste this whole
-- file > Run. It is safe to run again later: it updates what already exists
-- and never deletes student data.
--
-- What it creates
--   profiles        one row per portal account (student, teacher or admin)
--   groups          Qur'an and Arabic classes, by level
--   group_teachers  which teachers take which group
--   quran_logs      memorisation, revision and recitation records
--   assessments     teacher assessments and comments
--   resources       the digital library
--   announcements   notices for everyone, a wing, or one group
--   surahs          reference list of the 114 surahs
-- plus the security rules (row level security) that decide who sees what.
-- =============================================================================

create schema if not exists private;
grant usage on schema private to authenticated;

-- -----------------------------------------------------------------------------
-- Tables
-- -----------------------------------------------------------------------------
create table if not exists public.surahs (
  number   smallint primary key check (number between 1 and 114),
  name     text not null,
  meaning  text not null,
  name_ar  text not null,
  ayahs    smallint not null check (ayahs > 0)
);

create table if not exists public.groups (
  id          uuid primary key default gen_random_uuid(),
  name        text not null check (char_length(name) between 2 and 80),
  track       text not null check (track in ('quran', 'arabic')),
  level       text not null check (level in ('beginner', 'intermediate', 'advanced')),
  wing        text not null default 'mixed' check (wing in ('brothers', 'sisters', 'mixed')),
  created_at  timestamptz not null default now()
);

create table if not exists public.profiles (
  id                    uuid primary key references auth.users (id) on delete cascade,
  email                 text not null,
  full_name             text not null check (char_length(full_name) between 2 and 120),
  wing                  text check (wing in ('brothers', 'sisters')),
  phone                 text check (char_length(phone) <= 30),
  department            text check (char_length(department) <= 120),
  level                 text check (char_length(level) <= 20),
  role                  text not null default 'student' check (role in ('student', 'teacher', 'admin')),
  status                text not null default 'pending' check (status in ('pending', 'active', 'inactive')),
  quran_level           text check (quran_level in ('beginner', 'intermediate', 'advanced')),
  arabic_level          text check (arabic_level in ('beginner', 'intermediate', 'advanced')),
  quran_group           uuid references public.groups (id) on delete set null,
  arabic_group          uuid references public.groups (id) on delete set null,
  subjects              text check (char_length(subjects) <= 200),
  bio                   text check (char_length(bio) <= 500),
  must_change_password  boolean not null default false,
  consent_at            timestamptz,
  created_at            timestamptz not null default now(),
  updated_at            timestamptz not null default now()
);
create index if not exists profiles_quran_group_idx  on public.profiles (quran_group);
create index if not exists profiles_arabic_group_idx on public.profiles (arabic_group);
create index if not exists profiles_status_idx       on public.profiles (status);

-- Added later: which programme someone signed up for (false = Dawrah only, so they stay out of
-- the Islamiyyah approval list), and each Arabic class's place in its textbook.
alter table public.profiles add column if not exists joins_islamiyyah boolean not null default true;
alter table public.groups add column if not exists book text check (char_length(book) <= 120);
alter table public.groups add column if not exists current_lesson smallint check (current_lesson between 0 and 200);
alter table public.groups add column if not exists total_lessons smallint check (total_lessons between 1 and 200);
alter table public.groups add column if not exists progress_at timestamptz;

create table if not exists public.group_teachers (
  group_id    uuid not null references public.groups (id) on delete cascade,
  teacher_id  uuid not null references public.profiles (id) on delete cascade,
  primary key (group_id, teacher_id)
);
create index if not exists group_teachers_teacher_idx on public.group_teachers (teacher_id);

create table if not exists public.quran_logs (
  id           uuid primary key default gen_random_uuid(),
  student_id   uuid not null references public.profiles (id) on delete cascade,
  kind         text not null check (kind in ('memorisation', 'revision', 'recitation')),
  surah        smallint not null references public.surahs (number),
  from_ayah    smallint not null check (from_ayah >= 1),
  to_ayah      smallint not null,
  log_date     date not null default current_date,
  note         text check (char_length(note) <= 500),
  verified     boolean not null default false,
  verified_by  uuid references public.profiles (id) on delete set null,
  verified_at  timestamptz,
  created_by   uuid default auth.uid() references public.profiles (id) on delete set null,
  created_at   timestamptz not null default now(),
  check (to_ayah >= from_ayah)
);
create index if not exists quran_logs_student_idx on public.quran_logs (student_id, log_date desc);

create table if not exists public.assessments (
  id           uuid primary key default gen_random_uuid(),
  student_id   uuid not null references public.profiles (id) on delete cascade,
  track        text not null check (track in ('quran', 'arabic', 'books')),
  title        text not null check (char_length(title) between 2 and 120),
  assessed_on  date not null default current_date,
  score        numeric(5, 2) check (score between 0 and 100),
  comment      text check (char_length(comment) <= 1000),
  teacher_id   uuid default auth.uid() references public.profiles (id) on delete set null,
  teacher_name text,
  created_at   timestamptz not null default now()
);
alter table public.assessments add column if not exists teacher_name text;
create index if not exists assessments_student_idx on public.assessments (student_id, assessed_on desc);

create table if not exists public.resources (
  id           uuid primary key default gen_random_uuid(),
  title        text not null check (char_length(title) between 2 and 160),
  author       text check (char_length(author) <= 120),
  description  text check (char_length(description) <= 600),
  subject      text not null check (subject in ('quran', 'tajweed', 'arabic', 'aqeedah', 'fiqh', 'seerah', 'hadith', 'general')),
  level        text not null default 'all' check (level in ('all', 'beginner', 'intermediate', 'advanced')),
  file_path    text,
  url          text check (url ~* '^https?://'),
  file_type    text check (char_length(file_type) <= 20),
  file_size    bigint,
  added_by     uuid default auth.uid() references public.profiles (id) on delete set null,
  created_at   timestamptz not null default now(),
  check (file_path is not null or url is not null)
);

create table if not exists public.announcements (
  id           uuid primary key default gen_random_uuid(),
  title        text not null check (char_length(title) between 2 and 140),
  body         text not null check (char_length(body) between 2 and 2000),
  audience     text not null default 'all' check (audience in ('all', 'brothers', 'sisters', 'group')),
  group_id     uuid references public.groups (id) on delete cascade,
  pinned       boolean not null default false,
  author_id    uuid default auth.uid() references public.profiles (id) on delete set null,
  author_name  text,
  created_at   timestamptz not null default now(),
  check ((audience = 'group') = (group_id is not null))
);
create index if not exists announcements_created_idx on public.announcements (created_at desc);

-- -----------------------------------------------------------------------------
-- Surah reference data (114 surahs, 6,236 ayahs)
-- -----------------------------------------------------------------------------
-- BEGIN SURAHS (written by _source/build.py from _source/quran.py)
insert into public.surahs (number, name, meaning, name_ar, ayahs) values
  (1, 'Al-Faatiha', 'The Opening', 'الفاتحة', 7),
  (2, 'Al-Baqara', 'The Cow', 'البقرة', 286),
  (3, 'Aal-i-Imraan', 'The Family of Imraan', 'آل عمران', 200),
  (4, 'An-Nisaa', 'The Women', 'النساء', 176),
  (5, 'Al-Maaida', 'The Table', 'المائدة', 120),
  (6, 'Al-An''aam', 'The Cattle', 'الأنعام', 165),
  (7, 'Al-A''raaf', 'The Heights', 'الأعراف', 206),
  (8, 'Al-Anfaal', 'The Spoils of War', 'الأنفال', 75),
  (9, 'At-Tawba', 'The Repentance', 'التوبة', 129),
  (10, 'Yunus', 'Jonas', 'يونس', 109),
  (11, 'Hud', 'Hud', 'هود', 123),
  (12, 'Yusuf', 'Joseph', 'يوسف', 111),
  (13, 'Ar-Ra''d', 'The Thunder', 'الرعد', 43),
  (14, 'Ibrahim', 'Abraham', 'إبراهيم', 52),
  (15, 'Al-Hijr', 'The Rock', 'الحجر', 99),
  (16, 'An-Nahl', 'The Bee', 'النحل', 128),
  (17, 'Al-Israa', 'The Night Journey', 'الإسراء', 111),
  (18, 'Al-Kahf', 'The Cave', 'الكهف', 110),
  (19, 'Maryam', 'Mary', 'مريم', 98),
  (20, 'Taa-Haa', 'Taa-Haa', 'طه', 135),
  (21, 'Al-Anbiyaa', 'The Prophets', 'الأنبياء', 112),
  (22, 'Al-Hajj', 'The Pilgrimage', 'الحج', 78),
  (23, 'Al-Muminoon', 'The Believers', 'المؤمنون', 118),
  (24, 'An-Noor', 'The Light', 'النور', 64),
  (25, 'Al-Furqaan', 'The Criterion', 'الفرقان', 77),
  (26, 'Ash-Shu''araa', 'The Poets', 'الشعراء', 227),
  (27, 'An-Naml', 'The Ant', 'النمل', 93),
  (28, 'Al-Qasas', 'The Stories', 'القصص', 88),
  (29, 'Al-Ankaboot', 'The Spider', 'العنكبوت', 69),
  (30, 'Ar-Room', 'The Romans', 'الروم', 60),
  (31, 'Luqman', 'Luqman', 'لقمان', 34),
  (32, 'As-Sajda', 'The Prostration', 'السجدة', 30),
  (33, 'Al-Ahzaab', 'The Clans', 'الأحزاب', 73),
  (34, 'Saba', 'Sheba', 'سبإ', 54),
  (35, 'Faatir', 'The Originator', 'فاطر', 45),
  (36, 'Yaseen', 'Yaseen', 'يس', 83),
  (37, 'As-Saaffaat', 'Those drawn up in Ranks', 'الصافات', 182),
  (38, 'Saad', 'The letter Saad', 'ص', 88),
  (39, 'Az-Zumar', 'The Groups', 'الزمر', 75),
  (40, 'Al-Ghaafir', 'The Forgiver', 'غافر', 85),
  (41, 'Fussilat', 'Explained in detail', 'فصلت', 54),
  (42, 'Ash-Shura', 'Consultation', 'الشورى', 53),
  (43, 'Az-Zukhruf', 'Ornaments of gold', 'الزخرف', 89),
  (44, 'Ad-Dukhaan', 'The Smoke', 'الدخان', 59),
  (45, 'Al-Jaathiya', 'Crouching', 'الجاثية', 37),
  (46, 'Al-Ahqaf', 'The Dunes', 'الأحقاف', 35),
  (47, 'Muhammad', 'Muhammad', 'محمد', 38),
  (48, 'Al-Fath', 'The Victory', 'الفتح', 29),
  (49, 'Al-Hujuraat', 'The Inner Apartments', 'الحجرات', 18),
  (50, 'Qaaf', 'The letter Qaaf', 'ق', 45),
  (51, 'Adh-Dhaariyat', 'The Winnowing Winds', 'الذاريات', 60),
  (52, 'At-Tur', 'The Mount', 'الطور', 49),
  (53, 'An-Najm', 'The Star', 'النجم', 62),
  (54, 'Al-Qamar', 'The Moon', 'القمر', 55),
  (55, 'Ar-Rahmaan', 'The Beneficent', 'الرحمن', 78),
  (56, 'Al-Waaqia', 'The Inevitable', 'الواقعة', 96),
  (57, 'Al-Hadid', 'The Iron', 'الحديد', 29),
  (58, 'Al-Mujaadila', 'The Pleading Woman', 'المجادلة', 22),
  (59, 'Al-Hashr', 'The Exile', 'الحشر', 24),
  (60, 'Al-Mumtahana', 'She that is to be examined', 'الممتحنة', 13),
  (61, 'As-Saff', 'The Ranks', 'الصف', 14),
  (62, 'Al-Jumu''a', 'Friday', 'الجمعة', 11),
  (63, 'Al-Munaafiqoon', 'The Hypocrites', 'المنافقون', 11),
  (64, 'At-Taghaabun', 'Mutual Disillusion', 'التغابن', 18),
  (65, 'At-Talaaq', 'Divorce', 'الطلاق', 12),
  (66, 'At-Tahrim', 'The Prohibition', 'التحريم', 12),
  (67, 'Al-Mulk', 'The Sovereignty', 'الملك', 30),
  (68, 'Al-Qalam', 'The Pen', 'القلم', 52),
  (69, 'Al-Haaqqa', 'The Reality', 'الحاقة', 52),
  (70, 'Al-Ma''aarij', 'The Ascending Stairways', 'المعارج', 44),
  (71, 'Nooh', 'Noah', 'نوح', 28),
  (72, 'Al-Jinn', 'The Jinn', 'الجن', 28),
  (73, 'Al-Muzzammil', 'The Enshrouded One', 'المزمل', 20),
  (74, 'Al-Muddaththir', 'The Cloaked One', 'المدثر', 56),
  (75, 'Al-Qiyaama', 'The Resurrection', 'القيامة', 40),
  (76, 'Al-Insaan', 'Man', 'الإنسان', 31),
  (77, 'Al-Mursalaat', 'The Emissaries', 'المرسلات', 50),
  (78, 'An-Naba', 'The Announcement', 'النبإ', 40),
  (79, 'An-Naazi''aat', 'Those who drag forth', 'النازعات', 46),
  (80, 'Abasa', 'He frowned', 'عبس', 42),
  (81, 'At-Takwir', 'The Overthrowing', 'التكوير', 29),
  (82, 'Al-Infitaar', 'The Cleaving', 'الانفطار', 19),
  (83, 'Al-Mutaffifin', 'Defrauding', 'المطففين', 36),
  (84, 'Al-Inshiqaaq', 'The Splitting Open', 'الانشقاق', 25),
  (85, 'Al-Burooj', 'The Constellations', 'البروج', 22),
  (86, 'At-Taariq', 'The Morning Star', 'الطارق', 17),
  (87, 'Al-A''laa', 'The Most High', 'الأعلى', 19),
  (88, 'Al-Ghaashiya', 'The Overwhelming', 'الغاشية', 26),
  (89, 'Al-Fajr', 'The Dawn', 'الفجر', 30),
  (90, 'Al-Balad', 'The City', 'البلد', 20),
  (91, 'Ash-Shams', 'The Sun', 'الشمس', 15),
  (92, 'Al-Lail', 'The Night', 'الليل', 21),
  (93, 'Ad-Dhuhaa', 'The Morning Hours', 'الضحى', 11),
  (94, 'Ash-Sharh', 'The Consolation', 'الشرح', 8),
  (95, 'At-Tin', 'The Fig', 'التين', 8),
  (96, 'Al-Alaq', 'The Clot', 'العلق', 19),
  (97, 'Al-Qadr', 'The Power, Fate', 'القدر', 5),
  (98, 'Al-Bayyina', 'The Evidence', 'البينة', 8),
  (99, 'Az-Zalzala', 'The Earthquake', 'الزلزلة', 8),
  (100, 'Al-Aadiyaat', 'The Chargers', 'العاديات', 11),
  (101, 'Al-Qaari''a', 'The Calamity', 'القارعة', 11),
  (102, 'At-Takaathur', 'Competition', 'التكاثر', 8),
  (103, 'Al-Asr', 'The Declining Day, Epoch', 'العصر', 3),
  (104, 'Al-Humaza', 'The Traducer', 'الهمزة', 9),
  (105, 'Al-Fil', 'The Elephant', 'الفيل', 5),
  (106, 'Quraish', 'Quraysh', 'قريش', 4),
  (107, 'Al-Maa''un', 'Almsgiving', 'الماعون', 7),
  (108, 'Al-Kawthar', 'Abundance', 'الكوثر', 3),
  (109, 'Al-Kaafiroon', 'The Disbelievers', 'الكافرون', 6),
  (110, 'An-Nasr', 'Divine Support', 'النصر', 3),
  (111, 'Al-Masad', 'The Palm Fibre', 'المسد', 5),
  (112, 'Al-Ikhlaas', 'Sincerity', 'الإخلاص', 4),
  (113, 'Al-Falaq', 'The Dawn', 'الفلق', 5),
  (114, 'An-Naas', 'Mankind', 'الناس', 6)
on conflict (number) do update set name = excluded.name, meaning = excluded.meaning,
  name_ar = excluded.name_ar, ayahs = excluded.ayahs;
-- END SURAHS

-- -----------------------------------------------------------------------------
-- Helper functions used by the security rules. They live in a private schema,
-- so the website cannot call them directly.
-- -----------------------------------------------------------------------------
create or replace function private.is_active() returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.profiles
                 where id = (select auth.uid()) and status = 'active');
$$;

create or replace function private.is_staff() returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.profiles
                 where id = (select auth.uid()) and status = 'active' and role in ('teacher', 'admin'));
$$;

create or replace function private.is_admin() returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.profiles
                 where id = (select auth.uid()) and status = 'active' and role = 'admin');
$$;

create or replace function private.my_wing() returns text
language sql stable security definer set search_path = '' as $$
  select wing from public.profiles where id = (select auth.uid());
$$;

-- true when the signed-in teacher takes one of the student's groups
create or replace function private.teaches(student uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select private.is_staff() and exists (
    select 1
    from public.profiles s
    join public.group_teachers gt on gt.group_id in (s.quran_group, s.arabic_group)
    where s.id = student and gt.teacher_id = (select auth.uid())
  );
$$;

create or replace function private.teaches_group(g uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select private.is_staff() and exists (
    select 1 from public.group_teachers where group_id = g and teacher_id = (select auth.uid()));
$$;

create or replace function private.member_of(g uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.profiles
                 where id = (select auth.uid()) and status = 'active' and g in (quran_group, arabic_group));
$$;

revoke all on all functions in schema private from public, anon;
grant execute on all functions in schema private to authenticated;

-- -----------------------------------------------------------------------------
-- New accounts: every sign-up gets a profile, always as a pending student.
-- -----------------------------------------------------------------------------
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = '' as $$
declare
  m jsonb := coalesce(new.raw_user_meta_data, '{}'::jsonb);
  nm text := nullif(trim(m->>'full_name'), '');
  w  text := m->>'wing';
begin
  insert into public.profiles (id, email, full_name, wing, phone, department, level, consent_at, joins_islamiyyah)
  values (
    new.id,
    coalesce(new.email, ''),
    left(coalesce(nm, split_part(coalesce(new.email, 'New member'), '@', 1)), 120),
    case when w in ('brothers', 'sisters') then w end,
    left(nullif(trim(m->>'phone'), ''), 30),
    left(nullif(trim(m->>'department'), ''), 120),
    left(nullif(trim(m->>'level'), ''), 20),
    case when m->>'consent' = 'true' then now() end,
    coalesce(m->>'programme', '') <> 'dawrah'
  )
  on conflict (id) do nothing;
  return new;
end;
$$;
revoke all on function public.handle_new_user() from public, anon, authenticated;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- Only an admin may change role, status, wing, levels or groups.
create or replace function private.guard_profile() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  if (select auth.uid()) is null then          -- SQL Editor or a server task
    new.updated_at := now();
    return new;
  end if;
  new.id := old.id;
  new.email := old.email;
  new.created_at := old.created_at;
  new.consent_at := old.consent_at;
  if private.is_admin() then
    if new.id = (select auth.uid()) and (new.role <> 'admin' or new.status <> 'active') then
      raise exception 'You cannot remove your own admin access. Ask another admin.';
    end if;
  elsif new.role <> old.role
     or new.status <> old.status
     or new.wing is distinct from old.wing
     or new.quran_level is distinct from old.quran_level
     or new.arabic_level is distinct from old.arabic_level
     or new.quran_group is distinct from old.quran_group
     or new.arabic_group is distinct from old.arabic_group
     or (new.must_change_password and not old.must_change_password)
     or (old.joins_islamiyyah and not new.joins_islamiyyah) then
    raise exception 'Only an admin can change that.' using errcode = '42501';
  end if;
  new.updated_at := now();
  return new;
end;
$$;
drop trigger if exists guard_profile on public.profiles;
create trigger guard_profile before update on public.profiles
  for each row execute function private.guard_profile();

-- Qur'an records: the ayah range must exist, the date cannot be in the future,
-- and verification is stamped with who verified it.
create or replace function private.check_quran_log() returns trigger
language plpgsql security definer set search_path = '' as $$
declare n smallint;
begin
  select ayahs into n from public.surahs where number = new.surah;
  if n is null or new.to_ayah > n then
    raise exception 'Surah % has % ayahs.', new.surah, n using errcode = '22023';
  end if;
  if new.log_date > current_date + 1 then
    raise exception 'The date cannot be in the future.' using errcode = '22023';
  end if;
  if tg_op = 'UPDATE' then
    new.student_id := old.student_id;
    new.created_by := old.created_by;
    new.created_at := old.created_at;
  end if;
  if new.verified and (tg_op = 'INSERT' or not old.verified) then
    new.verified_by := (select auth.uid());
    new.verified_at := now();
  elsif not new.verified then
    new.verified_by := null;
    new.verified_at := null;
  end if;
  return new;
end;
$$;
drop trigger if exists check_quran_log on public.quran_logs;
create trigger check_quran_log before insert or update on public.quran_logs
  for each row execute function private.check_quran_log();

create or replace function private.stamp_author() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  if tg_op = 'UPDATE' then
    new.author_id := old.author_id;
    new.author_name := old.author_name;
    new.created_at := old.created_at;
  else
    new.author_id := (select auth.uid());
    new.author_name := (select full_name from public.profiles where id = (select auth.uid()));
  end if;
  return new;
end;
$$;
drop trigger if exists stamp_author on public.announcements;
create trigger stamp_author before insert or update on public.announcements
  for each row execute function private.stamp_author();

create or replace function private.stamp_teacher() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  if tg_op = 'UPDATE' then
    new.student_id := old.student_id;
    new.teacher_id := old.teacher_id;
    new.teacher_name := old.teacher_name;
    new.created_at := old.created_at;
  else
    new.teacher_id := (select auth.uid());
    new.teacher_name := (select full_name from public.profiles where id = (select auth.uid()));
  end if;
  return new;
end;
$$;
drop trigger if exists stamp_teacher on public.assessments;
create trigger stamp_teacher before insert or update on public.assessments
  for each row execute function private.stamp_teacher();

-- -----------------------------------------------------------------------------
-- Security rules
-- -----------------------------------------------------------------------------
alter table public.surahs         enable row level security;
alter table public.groups         enable row level security;
alter table public.profiles       enable row level security;
alter table public.group_teachers enable row level security;
alter table public.quran_logs     enable row level security;
alter table public.assessments    enable row level security;
alter table public.resources      enable row level security;
alter table public.announcements  enable row level security;

-- Visitors who are not signed in get nothing except the surah list.
revoke all on public.groups, public.profiles, public.group_teachers, public.quran_logs,
              public.assessments, public.resources, public.announcements from anon;
grant select on public.surahs to anon, authenticated;
grant select, insert, update, delete on public.groups, public.profiles, public.group_teachers,
      public.quran_logs, public.assessments, public.resources, public.announcements to authenticated;

drop policy if exists surahs_read on public.surahs;
create policy surahs_read on public.surahs for select to anon, authenticated using (true);

-- profiles: you see yourself; teachers see the students they teach; admins see everyone.
drop policy if exists profiles_read   on public.profiles;
drop policy if exists profiles_update on public.profiles;
drop policy if exists profiles_delete on public.profiles;
create policy profiles_read on public.profiles for select to authenticated
  using (id = (select auth.uid()) or (select private.is_admin()) or private.teaches(id));
create policy profiles_update on public.profiles for update to authenticated
  using (id = (select auth.uid()) or (select private.is_admin()))
  with check (id = (select auth.uid()) or (select private.is_admin()));
create policy profiles_delete on public.profiles for delete to authenticated
  using ((select private.is_admin()) and id <> (select auth.uid()));

-- groups and their teachers: any approved member can read; only admins change them.
drop policy if exists groups_read  on public.groups;
drop policy if exists groups_write on public.groups;
create policy groups_read  on public.groups for select to authenticated using ((select private.is_active()));
create policy groups_write on public.groups for all to authenticated
  using ((select private.is_admin())) with check ((select private.is_admin()));

drop policy if exists group_teachers_read  on public.group_teachers;
drop policy if exists group_teachers_write on public.group_teachers;
create policy group_teachers_read  on public.group_teachers for select to authenticated using ((select private.is_active()));
create policy group_teachers_write on public.group_teachers for all to authenticated
  using ((select private.is_admin())) with check ((select private.is_admin()));

-- Qur'an records: students add their own (unverified); their teachers and admins
-- add verified records, verify, correct and remove.
drop policy if exists quran_logs_read   on public.quran_logs;
drop policy if exists quran_logs_insert on public.quran_logs;
drop policy if exists quran_logs_update on public.quran_logs;
drop policy if exists quran_logs_delete on public.quran_logs;
create policy quran_logs_read on public.quran_logs for select to authenticated
  using (student_id = (select auth.uid()) or (select private.is_admin()) or private.teaches(student_id));
create policy quran_logs_insert on public.quran_logs for insert to authenticated
  with check (
    created_by = (select auth.uid()) and (
      (student_id = (select auth.uid()) and (select private.is_active()) and verified = false)
      or (select private.is_admin())
      or private.teaches(student_id)));
create policy quran_logs_update on public.quran_logs for update to authenticated
  using ((select private.is_admin()) or private.teaches(student_id))
  with check ((select private.is_admin()) or private.teaches(student_id));
create policy quran_logs_delete on public.quran_logs for delete to authenticated
  using ((student_id = (select auth.uid()) and verified = false)
         or (select private.is_admin()) or private.teaches(student_id));

-- assessments: the student reads their own; their teachers and admins write.
drop policy if exists assessments_read   on public.assessments;
drop policy if exists assessments_insert on public.assessments;
drop policy if exists assessments_update on public.assessments;
drop policy if exists assessments_delete on public.assessments;
create policy assessments_read on public.assessments for select to authenticated
  using (student_id = (select auth.uid()) or (select private.is_admin()) or private.teaches(student_id));
create policy assessments_insert on public.assessments for insert to authenticated
  with check (teacher_id = (select auth.uid()) and ((select private.is_admin()) or private.teaches(student_id)));
create policy assessments_update on public.assessments for update to authenticated
  using ((select private.is_admin()) or (teacher_id = (select auth.uid()) and private.teaches(student_id)))
  with check ((select private.is_admin()) or (teacher_id = (select auth.uid()) and private.teaches(student_id)));
create policy assessments_delete on public.assessments for delete to authenticated
  using ((select private.is_admin()) or (teacher_id = (select auth.uid()) and private.teaches(student_id)));

-- library: approved members read; teachers and admins add; the person who added
-- an item, or an admin, can edit or remove it.
drop policy if exists resources_read   on public.resources;
drop policy if exists resources_insert on public.resources;
drop policy if exists resources_change on public.resources;
drop policy if exists resources_delete on public.resources;
create policy resources_read on public.resources for select to authenticated using ((select private.is_active()));
create policy resources_insert on public.resources for insert to authenticated
  with check ((select private.is_staff()) and added_by = (select auth.uid()));
create policy resources_change on public.resources for update to authenticated
  using ((select private.is_admin()) or ((select private.is_staff()) and added_by = (select auth.uid())))
  with check ((select private.is_admin()) or ((select private.is_staff()) and added_by = (select auth.uid())));
create policy resources_delete on public.resources for delete to authenticated
  using ((select private.is_admin()) or ((select private.is_staff()) and added_by = (select auth.uid())));

-- announcements: members see notices for everyone, their wing and their groups.
-- Admins post to anyone; teachers post to the groups they teach.
drop policy if exists announcements_read   on public.announcements;
drop policy if exists announcements_insert on public.announcements;
drop policy if exists announcements_change on public.announcements;
drop policy if exists announcements_delete on public.announcements;
create policy announcements_read on public.announcements for select to authenticated
  using ((select private.is_active()) and (
    audience = 'all'
    or (select private.is_staff())
    or (audience in ('brothers', 'sisters') and audience = (select private.my_wing()))
    or (audience = 'group' and private.member_of(group_id))));
create policy announcements_insert on public.announcements for insert to authenticated
  with check ((select private.is_admin()) or (audience = 'group' and private.teaches_group(group_id)));
create policy announcements_change on public.announcements for update to authenticated
  using ((select private.is_admin()) or author_id = (select auth.uid()))
  with check ((select private.is_admin()) or (audience = 'group' and private.teaches_group(group_id)));
create policy announcements_delete on public.announcements for delete to authenticated
  using ((select private.is_admin()) or author_id = (select auth.uid()));

-- -----------------------------------------------------------------------------
-- Functions the portal calls
-- -----------------------------------------------------------------------------

-- The teachers of your groups (names and subjects only).
create or replace function public.my_teachers()
returns table (teacher_id uuid, full_name text, wing text, subjects text, bio text,
               group_id uuid, group_name text, track text, level text)
language sql stable security definer set search_path = '' as $$
  select t.id, t.full_name, t.wing, t.subjects, t.bio, g.id, g.name, g.track, g.level
  from public.profiles me
  join public.groups g on g.id in (me.quran_group, me.arabic_group)
  join public.group_teachers gt on gt.group_id = g.id
  join public.profiles t on t.id = gt.teacher_id and t.status = 'active'
  where me.id = (select auth.uid()) and me.status = 'active'
  order by g.track, t.full_name;
$$;

-- Classmates: names only, same group and same wing.
create or replace function public.my_classmates()
returns table (full_name text, group_name text, track text)
language sql stable security definer set search_path = '' as $$
  select s.full_name, g.name, g.track
  from public.profiles me
  join public.groups g on g.id in (me.quran_group, me.arabic_group)
  join public.profiles s on g.id in (s.quran_group, s.arabic_group)
  where me.id = (select auth.uid()) and me.status = 'active'
    and s.id <> me.id and s.status = 'active' and s.wing = me.wing
  order by g.track, s.full_name;
$$;

-- Arabic class progress: the class's teachers (or an admin) record the current lesson.
create or replace function public.set_group_progress(g uuid, lesson int, total int, book_name text)
returns void
language plpgsql security definer set search_path = '' as $$
begin
  if not (private.is_admin() or private.teaches_group(g)) then
    raise exception 'Only this class''s teachers can update its progress.' using errcode = '42501';
  end if;
  if not exists (select 1 from public.groups where id = g and track = 'arabic') then
    raise exception 'Class progress is for Arabic classes.';
  end if;
  if lesson is null or lesson < 0 or lesson > 200 then raise exception 'Enter the lesson number.'; end if;
  if total is not null and (total < 1 or total > 200) then raise exception 'Enter how many lessons the book has.'; end if;
  if total is not null and lesson > total then raise exception 'The current lesson cannot be after the last lesson.'; end if;
  update public.groups
     set current_lesson = lesson, total_lessons = total,
         book = left(nullif(trim(book_name), ''), 120), progress_at = now()
   where id = g;
end;
$$;

-- Admin: set a temporary password for a member who has forgotten theirs.
create or replace function public.admin_set_password(target uuid, new_password text)
returns void
language plpgsql security definer set search_path = '' as $$
begin
  if not private.is_admin() then
    raise exception 'Only an admin can reset passwords.' using errcode = '42501';
  end if;
  if char_length(coalesce(new_password, '')) < 8 then
    raise exception 'The password must be at least 8 characters.' using errcode = '22023';
  end if;
  update auth.users
     set encrypted_password = extensions.crypt(new_password, extensions.gen_salt('bf')),
         updated_at = now()
   where id = target;
  if not found then
    raise exception 'Account not found.' using errcode = 'P0002';
  end if;
  update public.profiles set must_change_password = true where id = target;
end;
$$;

-- Admin: delete an account and everything recorded for it.
create or replace function public.admin_delete_user(target uuid)
returns void
language plpgsql security definer set search_path = '' as $$
begin
  if not private.is_admin() then
    raise exception 'Only an admin can delete accounts.' using errcode = '42501';
  end if;
  if target = (select auth.uid()) then
    raise exception 'You cannot delete your own account.' using errcode = '22023';
  end if;
  delete from auth.users where id = target;
end;
$$;

revoke all on function public.my_teachers(), public.my_classmates(), public.set_group_progress(uuid, int, int, text),
  public.admin_set_password(uuid, text), public.admin_delete_user(uuid) from public, anon;
grant execute on function public.my_teachers(), public.my_classmates(), public.set_group_progress(uuid, int, int, text),
  public.admin_set_password(uuid, text), public.admin_delete_user(uuid) to authenticated;

-- -----------------------------------------------------------------------------
-- File storage for the library (private: only approved members can download)
-- -----------------------------------------------------------------------------
insert into storage.buckets (id, name, public, file_size_limit)
values ('materials', 'materials', false, 52428800)
on conflict (id) do nothing;

drop policy if exists "materials: members download" on storage.objects;
drop policy if exists "materials: staff upload"     on storage.objects;
drop policy if exists "materials: staff remove"     on storage.objects;
create policy "materials: members download" on storage.objects for select to authenticated
  using (bucket_id = 'materials' and (select private.is_active()));
create policy "materials: staff upload" on storage.objects for insert to authenticated
  with check (bucket_id = 'materials' and (select private.is_staff()));
create policy "materials: staff remove" on storage.objects for delete to authenticated
  using (bucket_id = 'materials' and (select private.is_staff()));

-- =============================================================================
-- DAWRAH (short courses such as Dawratul-Hadith)
--   dawrah_terms     one row per Dawrah term; exactly one is "current"
--   dawrah_roster    students registered for a term (pasted from the registration sheet)
--   dawrah_admins    people who run the Dawrah (portal admins are included automatically)
--   dawrah_lessons   one row per class: recording link and notes
--   dawrah_questions the two questions after each class, and the exam questions
--   dawrah_attempts  each student's answers and score (one try per class, one exam)
--   dawrah_views     when a student opened a class
-- A student gets into the Dawrah by signing up on the portal with the same email
-- they used on the registration form.
-- =============================================================================
create table if not exists public.dawrah_terms (
  id          uuid primary key default gen_random_uuid(),
  title       text not null check (char_length(title) between 2 and 160),
  schedule    text check (char_length(schedule) <= 200),
  venue       text check (char_length(venue) <= 120),
  book_url    text check (book_url ~* '^(https?://|assets/)'),
  exam_title  text not null default 'Final exam' check (char_length(exam_title) between 2 and 120),
  exam_open   boolean not null default false,
  is_current  boolean not null default false,
  created_at  timestamptz not null default now()
);
create unique index if not exists dawrah_terms_one_current on public.dawrah_terms (is_current) where is_current;
insert into public.dawrah_terms (title, schedule, venue, is_current)
select 'Dawratul-Hadith: The 40 Hadith of Imam An-Nawawi', 'Between Maghrib and Isha. The days will be announced soon', 'AFIT Masjid', true
where not exists (select 1 from public.dawrah_terms);
update public.dawrah_terms set schedule = 'Between Maghrib and Isha. The days will be announced soon'
 where schedule = 'Three days a week, between Maghrib and Isha';

create table if not exists public.dawrah_admins (
  user_id    uuid primary key references public.profiles (id) on delete cascade,
  full_name  text,
  email      text,
  added_at   timestamptz not null default now()
);
alter table public.dawrah_admins add column if not exists full_name text;
alter table public.dawrah_admins add column if not exists email text;

create table if not exists public.dawrah_roster (
  term_id        uuid not null references public.dawrah_terms (id) on delete cascade,
  email          text not null check (email = lower(email) and email ~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$'),
  full_name      text check (char_length(full_name) <= 120),
  phone          text check (char_length(phone) <= 30),
  written_score  numeric(5, 2) check (written_score between 0 and 100),
  added_at       timestamptz not null default now(),
  primary key (term_id, email)
);

create table if not exists public.dawrah_lessons (
  id           uuid primary key default gen_random_uuid(),
  term_id      uuid not null references public.dawrah_terms (id) on delete cascade,
  day_number   smallint not null check (day_number between 1 and 300),
  title        text not null check (char_length(title) between 2 and 160),
  lesson_date  date not null default current_date,
  audio_url    text check (audio_url ~* '^https?://'),
  notes        text check (char_length(notes) <= 600),
  created_at   timestamptz not null default now()
);
create index if not exists dawrah_lessons_term_idx on public.dawrah_lessons (term_id, day_number);

create table if not exists public.dawrah_questions (
  id         uuid primary key default gen_random_uuid(),
  term_id    uuid not null references public.dawrah_terms (id) on delete cascade,
  lesson_id  uuid references public.dawrah_lessons (id) on delete cascade,   -- empty = an exam question
  position   smallint not null default 1,
  prompt     text not null check (char_length(prompt) between 2 and 500),
  options    text[] not null check (array_length(options, 1) between 2 and 6),
  correct    smallint not null check (correct >= 0),
  check (correct < array_length(options, 1))
);
create index if not exists dawrah_questions_lesson_idx on public.dawrah_questions (lesson_id, position);

create table if not exists public.dawrah_attempts (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null references public.profiles (id) on delete cascade,
  term_id       uuid not null references public.dawrah_terms (id) on delete cascade,
  lesson_id     uuid references public.dawrah_lessons (id) on delete cascade,  -- empty = the exam
  score         smallint not null,
  total         smallint not null,
  answers       jsonb not null default '{}'::jsonb,
  submitted_at  timestamptz not null default now()
);
create unique index if not exists dawrah_attempts_one_quiz on public.dawrah_attempts (user_id, lesson_id) where lesson_id is not null;
create unique index if not exists dawrah_attempts_one_exam on public.dawrah_attempts (user_id, term_id) where lesson_id is null;

create table if not exists public.dawrah_views (
  user_id    uuid not null references public.profiles (id) on delete cascade,
  lesson_id  uuid not null references public.dawrah_lessons (id) on delete cascade,
  first_at   timestamptz not null default now(),
  last_at    timestamptz not null default now(),
  primary key (user_id, lesson_id)
);

-- ---------- helpers
create or replace function private.my_email() returns text
language sql stable security definer set search_path = '' as $$
  select lower(email) from public.profiles where id = (select auth.uid());
$$;

create or replace function private.dawrah_admin() returns boolean
language sql stable security definer set search_path = '' as $$
  select private.is_admin()
      or exists (select 1 from public.dawrah_admins where user_id = (select auth.uid()));
$$;

create or replace function private.dawrah_student(term uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.dawrah_roster r
                 where r.term_id = term and r.email = private.my_email());
$$;

create or replace function private.dawrah_current() returns uuid
language sql stable security definer set search_path = '' as $$
  select id from public.dawrah_terms where is_current limit 1;
$$;

revoke all on all functions in schema private from public, anon;
grant execute on all functions in schema private to authenticated;

-- ---------- security rules
alter table public.dawrah_terms     enable row level security;
alter table public.dawrah_admins    enable row level security;
alter table public.dawrah_roster    enable row level security;
alter table public.dawrah_lessons   enable row level security;
alter table public.dawrah_questions enable row level security;
alter table public.dawrah_attempts  enable row level security;
alter table public.dawrah_views     enable row level security;

revoke all on public.dawrah_terms, public.dawrah_admins, public.dawrah_roster, public.dawrah_lessons,
              public.dawrah_questions, public.dawrah_attempts, public.dawrah_views from anon;
grant select, insert, update, delete on public.dawrah_terms, public.dawrah_admins, public.dawrah_roster,
      public.dawrah_lessons, public.dawrah_questions to authenticated;
grant select, delete on public.dawrah_attempts, public.dawrah_views to authenticated;
revoke insert, update on public.dawrah_attempts, public.dawrah_views from authenticated;

drop policy if exists dawrah_terms_read  on public.dawrah_terms;
drop policy if exists dawrah_terms_write on public.dawrah_terms;
create policy dawrah_terms_read on public.dawrah_terms for select to authenticated
  using ((select private.dawrah_admin()) or private.dawrah_student(id));
create policy dawrah_terms_write on public.dawrah_terms for all to authenticated
  using ((select private.dawrah_admin())) with check ((select private.dawrah_admin()));

drop policy if exists dawrah_admins_all on public.dawrah_admins;
create policy dawrah_admins_all on public.dawrah_admins for all to authenticated
  using ((select private.dawrah_admin())) with check ((select private.dawrah_admin()));

drop policy if exists dawrah_roster_read  on public.dawrah_roster;
drop policy if exists dawrah_roster_write on public.dawrah_roster;
create policy dawrah_roster_read on public.dawrah_roster for select to authenticated
  using ((select private.dawrah_admin()) or email = (select private.my_email()));
create policy dawrah_roster_write on public.dawrah_roster for all to authenticated
  using ((select private.dawrah_admin())) with check ((select private.dawrah_admin()));

drop policy if exists dawrah_lessons_read  on public.dawrah_lessons;
drop policy if exists dawrah_lessons_write on public.dawrah_lessons;
create policy dawrah_lessons_read on public.dawrah_lessons for select to authenticated
  using ((select private.dawrah_admin()) or private.dawrah_student(term_id));
create policy dawrah_lessons_write on public.dawrah_lessons for all to authenticated
  using ((select private.dawrah_admin())) with check ((select private.dawrah_admin()));

-- Students never read questions directly (the answers are in this table);
-- they get them without answers through dawrah_questions_for().
drop policy if exists dawrah_questions_admin on public.dawrah_questions;
create policy dawrah_questions_admin on public.dawrah_questions for all to authenticated
  using ((select private.dawrah_admin())) with check ((select private.dawrah_admin()));

drop policy if exists dawrah_attempts_read   on public.dawrah_attempts;
drop policy if exists dawrah_attempts_delete on public.dawrah_attempts;
create policy dawrah_attempts_read on public.dawrah_attempts for select to authenticated
  using (user_id = (select auth.uid()) or (select private.dawrah_admin()));
create policy dawrah_attempts_delete on public.dawrah_attempts for delete to authenticated
  using ((select private.dawrah_admin()));

drop policy if exists dawrah_views_read on public.dawrah_views;
create policy dawrah_views_read on public.dawrah_views for select to authenticated
  using (user_id = (select auth.uid()) or (select private.dawrah_admin()));

-- ---------- functions the portal calls
-- Who am I in the Dawrah?
create or replace function public.dawrah_me() returns jsonb
language sql stable security definer set search_path = '' as $$
  select jsonb_build_object(
    'admin', private.dawrah_admin(),
    'student', coalesce(private.dawrah_student(t.id), false),
    'term', case when private.dawrah_admin() or private.dawrah_student(t.id) then to_jsonb(t) end)
  from (select 1) one
  left join public.dawrah_terms t on t.is_current;
$$;

-- Questions without their answers: a class's two questions, or the exam (exam = null lesson).
create or replace function public.dawrah_questions_for(lesson uuid)
returns table (id uuid, q_position smallint, prompt text, options text[])
language plpgsql stable security definer set search_path = '' as $$
declare t uuid;
begin
  if lesson is null then
    select dt.id into t from public.dawrah_terms dt where dt.is_current;
    if not private.dawrah_admin() and not (
         private.dawrah_student(t) and exists (select 1 from public.dawrah_terms where dawrah_terms.id = t and exam_open)) then
      raise exception 'The exam is not open.' using errcode = '42501';
    end if;
  else
    select l.term_id into t from public.dawrah_lessons l where l.id = lesson;
    if t is null or not (private.dawrah_admin() or private.dawrah_student(t)) then
      raise exception 'You are not registered for this Dawrah.' using errcode = '42501';
    end if;
  end if;
  return query
    select q.id, q.position, q.prompt, q.options from public.dawrah_questions q
    where q.term_id = t and q.lesson_id is not distinct from lesson
    order by q.position, q.id;
end;
$$;

-- Submit answers once. answers = {"<question id>": <chosen option index>, ...}
-- Returns the score; for a class it also returns the right answers.
create or replace function public.dawrah_submit(lesson uuid, answers jsonb) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare
  t uuid; me uuid := (select auth.uid()); sc int := 0; tot int := 0; q record; res jsonb := '[]'::jsonb; pick int;
begin
  if lesson is null then
    select dt.id into t from public.dawrah_terms dt where dt.is_current and dt.exam_open;
    if t is null then raise exception 'The exam is not open.' using errcode = '42501'; end if;
  else
    select l.term_id into t from public.dawrah_lessons l where l.id = lesson;
  end if;
  if t is null or not private.dawrah_student(t) then
    raise exception 'You are not registered for this Dawrah.' using errcode = '42501';
  end if;
  if exists (select 1 from public.dawrah_attempts a where a.user_id = me and a.term_id = t
             and a.lesson_id is not distinct from lesson) then
    raise exception 'You have already answered these questions.' using errcode = '23505';
  end if;
  for q in select * from public.dawrah_questions dq where dq.term_id = t
           and dq.lesson_id is not distinct from lesson order by dq.position, dq.id loop
    tot := tot + 1;
    pick := case when jsonb_typeof(answers -> q.id::text) = 'number' then (answers ->> q.id::text)::int end;
    if pick = q.correct then sc := sc + 1; end if;
    res := res || jsonb_build_object('id', q.id, 'chosen', pick, 'correct', q.correct);
  end loop;
  if tot = 0 then raise exception 'There are no questions yet.' using errcode = '22023'; end if;
  insert into public.dawrah_attempts (user_id, term_id, lesson_id, score, total, answers)
  values (me, t, lesson, sc, tot, coalesce(answers, '{}'::jsonb));
  return jsonb_build_object('score', sc, 'total', tot, 'results', case when lesson is null then null else res end);
end;
$$;

-- After answering a class's questions: see them with the right answers.
create or replace function public.dawrah_review(lesson uuid)
returns table (id uuid, q_position smallint, prompt text, options text[], correct smallint, chosen int)
language sql stable security definer set search_path = '' as $$
  select q.id, q.position, q.prompt, q.options, q.correct, (a.answers ->> q.id::text)::int
  from public.dawrah_questions q
  join public.dawrah_attempts a on a.lesson_id = q.lesson_id and a.user_id = (select auth.uid())
  where q.lesson_id = lesson
  order by q.position, q.id;
$$;

-- Record that a student opened a class's recording.
create or replace function public.dawrah_opened(lesson uuid) returns void
language plpgsql security definer set search_path = '' as $$
declare t uuid;
begin
  select l.term_id into t from public.dawrah_lessons l where l.id = lesson;
  if t is null or not private.dawrah_student(t) then return; end if;
  insert into public.dawrah_views (user_id, lesson_id) values ((select auth.uid()), lesson)
  on conflict (user_id, lesson_id) do update set last_at = now();
end;
$$;

-- The follow-up table for Dawrah admins: one row per registered student.
create or replace function public.dawrah_tracker()
returns table (email text, full_name text, phone text, user_id uuid, signed_up boolean,
               classes_done int, quiz_score int, quiz_total int, opened int,
               exam_score int, exam_total int, written_score numeric, last_active timestamptz)
language plpgsql stable security definer set search_path = '' as $$
declare t uuid := private.dawrah_current();
begin
  if not private.dawrah_admin() then
    raise exception 'Only Dawrah admins can see this.' using errcode = '42501';
  end if;
  return query
    select r.email, coalesce(p.full_name, r.full_name), coalesce(nullif(r.phone, ''), p.phone), p.id, p.id is not null,
      (select count(*)::int from public.dawrah_attempts a where a.user_id = p.id and a.term_id = t and a.lesson_id is not null),
      (select coalesce(sum(a.score), 0)::int from public.dawrah_attempts a where a.user_id = p.id and a.term_id = t and a.lesson_id is not null),
      (select coalesce(sum(a.total), 0)::int from public.dawrah_attempts a where a.user_id = p.id and a.term_id = t and a.lesson_id is not null),
      (select count(*)::int from public.dawrah_views v join public.dawrah_lessons l on l.id = v.lesson_id where v.user_id = p.id and l.term_id = t),
      (select a.score::int from public.dawrah_attempts a where a.user_id = p.id and a.term_id = t and a.lesson_id is null),
      (select a.total::int from public.dawrah_attempts a where a.user_id = p.id and a.term_id = t and a.lesson_id is null),
      r.written_score,
      greatest((select max(a.submitted_at) from public.dawrah_attempts a where a.user_id = p.id and a.term_id = t),
               (select max(v.last_at) from public.dawrah_views v join public.dawrah_lessons l on l.id = v.lesson_id where v.user_id = p.id and l.term_id = t))
    from public.dawrah_roster r
    left join public.profiles p on lower(p.email) = r.email
    where r.term_id = t
    order by coalesce(p.full_name, r.full_name, r.email);
end;
$$;

-- The current term's classes for the student (or admin) asking, with their own result.
-- Students see a class from its date; admins see every class.
create or replace function public.dawrah_my_classes()
returns table (id uuid, day_number smallint, title text, lesson_date date, audio_url text, notes text,
               questions int, score int, total int, opened boolean)
language sql stable security definer set search_path = '' as $$
  select l.id, l.day_number, l.title, l.lesson_date, l.audio_url, l.notes,
    (select count(*)::int from public.dawrah_questions q where q.lesson_id = l.id),
    a.score::int, a.total::int,
    exists (select 1 from public.dawrah_views v where v.lesson_id = l.id and v.user_id = (select auth.uid()))
  from public.dawrah_lessons l
  left join public.dawrah_attempts a on a.lesson_id = l.id and a.user_id = (select auth.uid())
  where l.term_id = private.dawrah_current()
    and (private.dawrah_admin()
         or (private.dawrah_student(l.term_id) and l.lesson_date <= (now() at time zone 'Africa/Lagos')::date))
  order by l.day_number, l.lesson_date;
$$;

-- Add a Dawrah admin by the email they signed up with.
create or replace function public.dawrah_add_admin(admin_email text) returns text
language plpgsql security definer set search_path = '' as $$
declare who uuid; nm text;
begin
  if not private.dawrah_admin() then
    raise exception 'Only Dawrah admins can add admins.' using errcode = '42501';
  end if;
  select id, full_name into who, nm from public.profiles where lower(email) = lower(trim(admin_email));
  if who is null then
    raise exception 'No portal account uses that email yet. Ask them to create one first.' using errcode = 'P0002';
  end if;
  insert into public.dawrah_admins (user_id, full_name, email) values (who, nm, lower(trim(admin_email)))
  on conflict (user_id) do update set full_name = excluded.full_name, email = excluded.email;
  return nm;
end;
$$;

revoke all on function public.dawrah_me(), public.dawrah_questions_for(uuid), public.dawrah_submit(uuid, jsonb),
  public.dawrah_review(uuid), public.dawrah_opened(uuid), public.dawrah_tracker(), public.dawrah_add_admin(text),
  public.dawrah_my_classes() from public, anon;
grant execute on function public.dawrah_me(), public.dawrah_questions_for(uuid), public.dawrah_submit(uuid, jsonb),
  public.dawrah_review(uuid), public.dawrah_opened(uuid), public.dawrah_tracker(), public.dawrah_add_admin(text),
  public.dawrah_my_classes() to authenticated;

-- Done. Next: sign up on the portal, then make yourself the first admin with
--   update public.profiles set role = 'admin', status = 'active' where email = 'you@example.com';
