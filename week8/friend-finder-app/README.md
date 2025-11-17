# Friend Finder - Ruby on Rails Version

A full-stack web application built with Ruby on Rails for helping college new grads (ages 21-26) build real, lasting friendships in their new city.

## Tech Stack

- **Backend:** Ruby on Rails 7.2.2
- **Frontend:** ERB templates with Tailwind CSS 4.1
- **JavaScript:** Vanilla JS with Stimulus.js
- **Database:** SQLite (development), PostgreSQL-ready (production)
- **Ruby Version:** 3.3.6

## Features

### Core Functionality (CRUD)
- ✅ **User Management** - Create, read, update user accounts
- ✅ **Profile Management** - Create, read, update user profiles with interests/vibes
- ✅ **Match Management** - Create matches, read match lists, update match status (accept/reject)
- ✅ **Event Management** - Full CRUD for social events
- ✅ **Message Management** - Create and read chat messages between matched users

### Key Features
- **Voice-based Profile Creation** - Uses Web Speech API for voice input
- **AI-Powered Matching Algorithm** - Compatibility scoring based on interests, social energy, location, and vibes
- **Real-time Chat** - Message system between matched users
- **Event System** - Create and join hangout events
- **Friendship Garden** - Visual health score tracking friendship activity

## Prerequisites

- Ruby 3.3.6 (installed via rbenv)
- rbenv (Ruby version manager)
- Bundler
- SQLite3

## Installation & Setup

### 1. Install Ruby 3.3.6 with rbenv

```bash
# Install rbenv (if not already installed)
brew install rbenv ruby-build

# Install Ruby 3.3.6
rbenv install 3.3.6
rbenv global 3.3.6

# Verify installation
ruby --version  # Should show ruby 3.3.6
```

### 2. Navigate to Project Directory

```bash
cd path/to/week8/friend-finder-app
```

### 3. Install Dependencies

```bash
# Initialize rbenv in your shell
eval "$(rbenv init - zsh)"  # or bash if using bash

# Install gems
bundle install
```

### 4. Setup Database

```bash
# Create database
rails db:create

# Run migrations
rails db:migrate

# Load seed data (creates 5 test users with profiles, matches, events)
rails db:seed
```

## Running the Application

### Start the Rails Server

```bash
eval "$(rbenv init - zsh)"
rails server
```

The application will be available at: **http://localhost:3000**

## Test Accounts

The seed data creates 5 test users you can login with:

| Email | Password | Profile |
|-------|----------|---------|
| alex@example.com | password123 | Likes hiking, coffee, board games |
| jordan@example.com | password123 | Likes music, concerts, cooking |
| sam@example.com | password123 | Likes gaming, tech, books |
| taylor@example.com | password123 | Likes hiking, photography, art |
| morgan@example.com | password123 | Likes cooking, board games, movies |

## Testing the Application

1. **Login:** Go to http://localhost:3000, use alex@example.com / password123
2. **View Dashboard:** See friendship garden and stats
3. **Check Matches:** Click "Matches" to view pending and accepted matches
4. **Send Message:** Click "View Chat" on any accepted match
5. **Join Event:** Click "Events" and join one
6. **New User:** Logout, click "Sign up", create account, try voice intake

## Project Structure

```
app/
├── controllers/      # Request handlers
├── models/           # Data models (User, Profile, Match, etc.)
└── views/            # HTML templates
db/
├── migrate/          # Database migrations
└── seeds.rb          # Test data
config/
└── routes.rb         # URL routing
```

## Known Issues

1. **Voice Recognition:** Requires Chrome/Edge browser
2. **AI Processing:** Currently simulated - production should use OpenAI API
3. **Real-time Chat:** Uses page reloads (ActionCable ready but not implemented)

## Author

Built for Week 8 assignment - Multi-Stack AI-Accelerated Web App Build
