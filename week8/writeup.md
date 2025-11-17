# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Alfred YU** \
SUNet ID: **ayu1001** \
Citations: **Windsurf, Bolt**

This assignment took me about **5** hours to do.


## App Concept
Friend Finder is a simple app that helps recent grads (21–26) meet new friends through brief profiles and shared-interest matching. Users create a short bio with interests, activities, and availability, then browse others with overlapping tags. Matching is rule-based and transparent, showing people with the most shared interests first. Users can view profiles, filter by interests or location, and send or receive connection requests. Accepted requests become “matched friends” for easy follow-up. The goal is to help new grads quickly meet 1–2 compatible people with minimal friction. For the purposes of the assignment, most of the tests were done with dummy data, and the main functionality is that users can sign-in and that their information is stored in the backend.


## Version #1 Description
```
APP DETAILS:
===============
Folder name: `week8/friend-finder` (Supabase migration in `week8/supabase`)
AI app generation platform: Bolt.new
Tech Stack: React 18 SPA + Express 4 API + Node 18 + Supabase PostgreSQL
Persistence: Supabase Postgres (profiles, interests, activities, connections tables with RLS)
Frameworks/Libraries Used: React Router, Fetch API, Express, @supabase/supabase-js, cors, dotenv
(Optional but recommended) Screenshots of core flows:
REFLECTIONS:
===============
a. There weren't that many errors - I felt the app was functional when tested! The web app in its current state is not very appealing to look at though.


b. Prompting (e.g. what required additional guidance; what worked poorly/wel): I created a PRD that I discussed and refined with GPT, then, I submitted that PRD with Bolt to use as an initial plan. I think creating that PRD was helpful for Bolt to get an understanding of what was happening.

c. Approximate time-to-first-run and time-to-feature metrics: ~8 minutes from first Bolt prompt to running the generated React + Express dev servers. Most of the features were implemented by Bolt (albeit some features may still need tuning, like sending users emails).
```

## Version #2 Description
```
APP DETAILS:
===============
Folder name: friend-finder-app
AI app generation platform: Claude Code and Windsurf
Tech Stack: Ruby on Rails
Persistence: SQLite (ActiveRecord + db/seeds.rb in development, Postgres-ready migration set for production)
Frameworks/Libraries Used: Rails 7.2, Stimulus.js, Tailwind CSS, ActiveRecord, Action Cable (scaffolded)
(Optional but recommended) Screenshots of core flows:

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: It was difficult getting Claude Code to figure out proper versions to install wihtout dependency issues. Also, there was a bit of issue with the sign in and sign-on onboarding flow - this was resolved by additional prompting on the error messages.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): It required additional prompting to get the onboarding flow set up well. I think another difficulty is that this app inherently needs many users right now (my fault with creating an app spec that isn't fully testable without a large userbase), so there's no toy data that's in right now, which likely tripped up the app as well. This likely could have been streamlined with usage of a CLAUDE.md and other subagents, but I did direct prompting.

c. Approximate time-to-first-run and time-to-feature metrics: 30-45 minutes - the general feature flow took around 30-45 minutes, it took an additional 20 minutes or so to get the sign-in and sign-on onboarding flow working.
```

## Version #3 Description
```
APP DETAILS:
===============
Folder name: `friend-finder-minimal`
AI app generation platform: Built on Bolt.now
Tech Stack: Flask 3 backend + SQLite + vanilla HTML/CSS/JavaScript (no bundler)
Persistence: Local SQLite database (`friend_finder.db`, auto-created/seeded via `demo.py`)
Frameworks/Libraries Used: Flask, Flask-CORS on the backend; native Fetch API/DOM APIs on the frontend
(Optional but recommended) Screenshots of core flows:

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: There weren't many issues that happened on this stack luckily - I mainly coded this out with Bolt and had it resolve most of the errors that occurred (leveraging the PRD that was used previously for BOLT as well).

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): I coded this out with Bolt, and focused on making a simple, barebones version that would be easy to work with and implement. I explicitly wanted a simple, minimalistic version of the app to make it easier to test and implement as opposed to the other versions, which took longer to work with.

c. Approximate time-to-first-run and time-to-feature metrics: It took around 8 minutes to get the code for the app to finish.
```
