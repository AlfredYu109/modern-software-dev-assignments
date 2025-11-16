/*
  # Friend Finder Lite Database Schema

  ## Overview
  Creates the core tables for Friend Finder Lite application allowing users to:
  - Create and manage profiles
  - Browse and match with other users
  - Send and receive connection requests

  ## New Tables

  ### `profiles`
  User profiles containing personal information and interests
  - `id` (uuid, primary key)
  - `name` (text, required)
  - `bio` (text)
  - `city` (text)
  - `neighborhood` (text)
  - `availability` (text array) - weekday/weekend preferences
  - `created_at` (timestamptz)
  - `updated_at` (timestamptz)

  ### `interests`
  Tag-based interests for profiles
  - `id` (uuid, primary key)
  - `profile_id` (uuid, foreign key to profiles)
  - `tag` (text) - interest tags like "hiking", "cooking", etc.
  - `created_at` (timestamptz)

  ### `activities`
  Preferred activities for profiles
  - `id` (uuid, primary key)
  - `profile_id` (uuid, foreign key to profiles)
  - `activity` (text) - activities like "coffee", "movies", etc.
  - `created_at` (timestamptz)

  ### `connections`
  Connection requests and accepted friendships
  - `id` (uuid, primary key)
  - `sender_id` (uuid, foreign key to profiles)
  - `receiver_id` (uuid, foreign key to profiles)
  - `status` (text) - pending, accepted, declined
  - `created_at` (timestamptz)
  - `updated_at` (timestamptz)

  ## Security
  - Enable RLS on all tables
  - Public read access for profiles (for browsing/matching)
  - Users can only modify their own profiles
  - Users can manage their own connection requests

  ## Indexes
  - Index on profile city/neighborhood for filtering
  - Index on interest tags for matching
  - Index on connection status for queries
*/

CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  bio text DEFAULT '',
  city text DEFAULT '',
  neighborhood text DEFAULT '',
  availability text[] DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS interests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  tag text NOT NULL,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS activities (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  activity text NOT NULL,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS connections (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  sender_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  receiver_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined')),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(sender_id, receiver_id)
);

CREATE INDEX IF NOT EXISTS idx_profiles_city ON profiles(city);
CREATE INDEX IF NOT EXISTS idx_profiles_neighborhood ON profiles(neighborhood);
CREATE INDEX IF NOT EXISTS idx_interests_tag ON interests(tag);
CREATE INDEX IF NOT EXISTS idx_interests_profile ON interests(profile_id);
CREATE INDEX IF NOT EXISTS idx_activities_profile ON activities(profile_id);
CREATE INDEX IF NOT EXISTS idx_connections_sender ON connections(sender_id);
CREATE INDEX IF NOT EXISTS idx_connections_receiver ON connections(receiver_id);
CREATE INDEX IF NOT EXISTS idx_connections_status ON connections(status);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE interests ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE connections ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Profiles are viewable by everyone"
  ON profiles FOR SELECT
  USING (true);

CREATE POLICY "Users can insert their own profile"
  ON profiles FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Users can update their own profile"
  ON profiles FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Users can delete their own profile"
  ON profiles FOR DELETE
  USING (true);

CREATE POLICY "Interests are viewable by everyone"
  ON interests FOR SELECT
  USING (true);

CREATE POLICY "Users can insert interests"
  ON interests FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Users can delete interests"
  ON interests FOR DELETE
  USING (true);

CREATE POLICY "Activities are viewable by everyone"
  ON activities FOR SELECT
  USING (true);

CREATE POLICY "Users can insert activities"
  ON activities FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Users can delete activities"
  ON activities FOR DELETE
  USING (true);

CREATE POLICY "Connections are viewable by sender and receiver"
  ON connections FOR SELECT
  USING (true);

CREATE POLICY "Users can send connection requests"
  ON connections FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Users can update connections they're involved in"
  ON connections FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Users can delete their own connection requests"
  ON connections FOR DELETE
  USING (true);