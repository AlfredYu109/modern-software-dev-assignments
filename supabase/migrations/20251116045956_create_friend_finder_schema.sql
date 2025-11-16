/*
  # Friend Finder Lite Database Schema

  1. New Tables
    - `profiles`
      - `id` (uuid, primary key)
      - `name` (text, required)
      - `bio` (text)
      - `city` (text)
      - `neighborhood` (text)
      - `availability` (text - weekday/weekend/both)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    
    - `interests`
      - `id` (uuid, primary key)
      - `profile_id` (uuid, foreign key to profiles)
      - `tag` (text, required)
      - `created_at` (timestamptz)
    
    - `activities`
      - `id` (uuid, primary key)
      - `profile_id` (uuid, foreign key to profiles)
      - `activity` (text, required)
      - `created_at` (timestamptz)
    
    - `connections`
      - `id` (uuid, primary key)
      - `sender_id` (uuid, foreign key to profiles)
      - `receiver_id` (uuid, foreign key to profiles)
      - `status` (text - pending/accepted/declined)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)

  2. Security
    - Enable RLS on all tables
    - For simplicity, allow public read/write access (no auth for MVP)
    - Add constraints to prevent invalid data
*/

-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL CHECK (length(name) > 0),
  bio text,
  city text,
  neighborhood text,
  availability text CHECK (availability IN ('weekday', 'weekend', 'both')),
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);

-- Create interests table
CREATE TABLE IF NOT EXISTS interests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  tag text NOT NULL CHECK (length(tag) > 0),
  created_at timestamptz DEFAULT now() NOT NULL
);

-- Create activities table
CREATE TABLE IF NOT EXISTS activities (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  activity text NOT NULL CHECK (length(activity) > 0),
  created_at timestamptz DEFAULT now() NOT NULL
);

-- Create connections table
CREATE TABLE IF NOT EXISTS connections (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  sender_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  receiver_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined')),
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL,
  CHECK (sender_id != receiver_id),
  UNIQUE(sender_id, receiver_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_interests_profile_id ON interests(profile_id);
CREATE INDEX IF NOT EXISTS idx_interests_tag ON interests(tag);
CREATE INDEX IF NOT EXISTS idx_activities_profile_id ON activities(profile_id);
CREATE INDEX IF NOT EXISTS idx_connections_sender ON connections(sender_id);
CREATE INDEX IF NOT EXISTS idx_connections_receiver ON connections(receiver_id);
CREATE INDEX IF NOT EXISTS idx_connections_status ON connections(status);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE interests ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE connections ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (no authentication for MVP)
-- Profiles policies
CREATE POLICY "Anyone can read profiles"
  ON profiles FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Anyone can create profiles"
  ON profiles FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Anyone can update profiles"
  ON profiles FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Anyone can delete profiles"
  ON profiles FOR DELETE
  TO anon, authenticated
  USING (true);

-- Interests policies
CREATE POLICY "Anyone can read interests"
  ON interests FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Anyone can create interests"
  ON interests FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Anyone can delete interests"
  ON interests FOR DELETE
  TO anon, authenticated
  USING (true);

-- Activities policies
CREATE POLICY "Anyone can read activities"
  ON activities FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Anyone can create activities"
  ON activities FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Anyone can delete activities"
  ON activities FOR DELETE
  TO anon, authenticated
  USING (true);

-- Connections policies
CREATE POLICY "Anyone can read connections"
  ON connections FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Anyone can create connections"
  ON connections FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Anyone can update connections"
  ON connections FOR UPDATE
  TO anon, authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Anyone can delete connections"
  ON connections FOR DELETE
  TO anon, authenticated
  USING (true);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at
CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_connections_updated_at
  BEFORE UPDATE ON connections
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
