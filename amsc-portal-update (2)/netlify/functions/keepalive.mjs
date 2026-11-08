// Runs once a day on Netlify. It reads the portal's Supabase address from
// portal-config.js on the live site and makes one tiny read, so the free
// Supabase project counts as active and is not paused after 7 quiet days.
// Nothing to set up: it starts working once portal-config.js is filled in.
export default async () => {
  const site = (process.env.URL || 'https://afitmsc.com.ng').replace(/\/$/, '');
  try {
    const cfg = await (await fetch(`${site}/portal-config.js`, { headers: { 'cache-control': 'no-cache' } })).text();
    const url = (cfg.match(/supabaseUrl:\s*["']([^"']+)["']/) || [])[1];
    const key = (cfg.match(/supabaseKey:\s*["']([^"']+)["']/) || [])[1];
    if (!url || !key) {
      console.log('Portal not connected to Supabase yet; nothing to keep awake.');
      return new Response('not configured');
    }
    const res = await fetch(`${url.replace(/\/$/, '')}/rest/v1/surahs?select=number&limit=1`, { headers: { apikey: key } });
    console.log(`Supabase keep-alive: HTTP ${res.status}`);
    return new Response(`ok ${res.status}`);
  } catch (e) {
    console.log(`Supabase keep-alive failed: ${e.message}`);
    return new Response('failed', { status: 500 });
  }
};

export const config = { schedule: '@daily' };
