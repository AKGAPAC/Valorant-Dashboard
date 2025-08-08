# Valorant Competitive Dashboard (Streamlit + Supabase)

This project is a fully customizable Valorant team dashboard with:

- Blue–Black–Purple esports theme
- Supabase database (teams, players, logos)
- File upload support for team logos
- Inline stat entry (no CSVs needed)
- Pro-level metrics (K/D, ADR, ACS, HS%, Win%)
- Password-protected Admin Panel

---

## 🚀 Getting Started

### 1. Create Supabase Project
- Go to https://supabase.com/
- Create a new project
- Get your **Project URL** and **Anon Public Key** from:

### 2. Run SQL
- In Supabase → SQL Editor
- Paste and run contents of `sql_schema.sql`

### 3. Create a Storage Bucket
- Go to **Storage → Create Bucket**
- Name it: `team-logos`
- Set **public access** enabled

---

## 💻 Local Development

1. Clone this repo
2. Install dependencies:
3. Create a `.streamlit/secrets.toml` with:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
SUPABASE_STORAGE_BUCKET = "team-logos"
ADMIN_PASSWORD = "Admin123"
streamlit run streamlit_dashboard.py
