// Islamiyyah Student Portal: connection to the Supabase database.
// Paste the two values from Supabase > Project Settings > API (or "Connect")
// between the quotes, then save. Both are safe to publish: the database's
// security rules decide who can see what.
window.AMSC_PORTAL = {
  supabaseUrl: "https://gxvcgaxflwyedvakjyop.supabase.co",
  supabaseKey: "sb_publishable_SdfAzPLqaasolMCGzUJoug_mFDpS-kG",
  emailReset: false  // change to true only after setting up email (custom SMTP) in Supabase
};
