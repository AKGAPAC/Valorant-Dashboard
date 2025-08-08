-- Table: teams
create table if not exists teams (
  id serial primary key,
  name text not null,
  logo_url text
);

-- Table: players
create table if not exists players (
  id serial primary key,
  name text not null,
  rank text,
  team_id integer references teams(id) on delete cascade,
  kills integer default 0,
  deaths integer default 0,
  assists integer default 0,
  headshots integer default 0,
  damage integer default 0,
  games_played integer default 0,
  wins integer default 0,
  kd_ratio float,
  hs_percent float,
  adr float,
  win_rate float,
  acs float
);

-- Enable RLS if needed (optional)
-- alter table teams enable row level security;
-- alter table players enable row level security;

-- Create public bucket for logos (manual step in Supabase UI)
