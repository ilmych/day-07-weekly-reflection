# Weekly Reflection Journal

> A calming space for weekly reflections and personal growth tracking.

Built as part of [30 Days of Vibe Code](https://github.com/ilmych/vibe-coding-challenge).

## What it does

A journaling app that helps you reflect on your week with guided prompts:
- What went well this week?
- What didn't go as planned?
- What did you learn?
- What's one thing to focus on next week?

Rate your week, track your streak, and see your patterns over time.

## Demo

[Try it live](https://weekly-reflection.streamlit.app) *(coming soon)*

## Features

- **Email authentication** - Your reflections are private
- **Cloud sync** - Access from any device
- **Weekly prompts** - Guided reflection questions
- **5-point rating** - Track how your weeks are going
- **Stats** - Streak tracking, average rating, total entries
- **Calming UI** - Soft colors, clean design

## Stack

- **Frontend**: Streamlit
- **Backend**: Supabase (Auth + Postgres)
- **Hosting**: Streamlit Community Cloud

## How I built it

- **Time**: ~1.5 hours
- **AI assist**: Claude Code
- **Iterations**: Started with local JSON storage, added Supabase auth

## Run locally

1. Clone the repo
2. Create a Supabase project and run the SQL schema (see below)
3. Create `.env` file:
   ```
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_anon_key
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run:
   ```bash
   streamlit run app.py
   ```

## Database Schema

Run this in Supabase SQL Editor:

```sql
CREATE TABLE reflections (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  week_key TEXT NOT NULL,
  went_well TEXT DEFAULT '',
  challenges TEXT DEFAULT '',
  learned TEXT DEFAULT '',
  focus TEXT DEFAULT '',
  rating TEXT DEFAULT '3',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, week_key)
);

ALTER TABLE reflections ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own reflections" ON reflections FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own reflections" ON reflections FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own reflections" ON reflections FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own reflections" ON reflections FOR DELETE USING (auth.uid() = user_id);
```

---

*Day 7 of #30DaysOfVibeCode*
