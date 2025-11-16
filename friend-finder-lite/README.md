# Friend Finder Lite

A lightweight web application that helps recent college graduates make new friends in their post-grad city. Users can create profiles, browse matches based on shared interests, and send connection requests.

## Features

- Create and manage personal profiles
- Browse profiles with filtering by city, neighborhood, interests, and activities
- View personalized matches based on shared interests and activities
- Send and receive connection requests
- Build your friend network
- Simple, rule-based matching algorithm

## Tech Stack

- **Backend**: Flask + Python
- **Frontend**: React
- **Database**: Supabase (PostgreSQL)

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Setup Instructions

### 1. Clone the repository

```bash
cd friend-finder-lite
```

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# The database is already configured with Supabase
# Start the Flask server
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

### Creating a Profile

1. Visit the homepage
2. Click "Create Profile"
3. Fill in your information:
   - Name (required)
   - Bio
   - City and neighborhood
   - Interests (tags like "hiking", "cooking", "photography")
   - Preferred activities (like "coffee", "movies", "sports")
   - Availability (weekdays/weekends)
4. Click "Create Profile"

### Browsing Profiles

1. Click "Browse" in the navigation
2. Use filters to narrow down profiles by:
   - City
   - Neighborhood
   - Specific interest
   - Specific activity
   - Availability
3. Click on any profile card to view full details

### Finding Matches

1. Click "Matches" in the navigation
2. View profiles sorted by match score
3. Match score is calculated by:
   - Number of shared interests
   - Number of shared activities
4. Click on profiles to view details and send connection requests

### Managing Connections

1. Click "Connections" in the navigation
2. Three tabs available:
   - **Requests Received**: View and respond to incoming connection requests
   - **Requests Sent**: See status of your sent requests
   - **Friends**: View accepted connections

### Editing Your Profile

1. Click "My Profile" in the navigation
2. Click "Edit Profile"
3. Update any information
4. Click "Save Changes"

## API Endpoints

### Profiles

- `GET /api/profiles` - Get all profiles (with optional filters)
- `GET /api/profiles/:id` - Get specific profile
- `POST /api/profiles` - Create new profile
- `PUT /api/profiles/:id` - Update profile
- `DELETE /api/profiles/:id` - Delete profile
- `GET /api/profiles/:id/matches` - Get matches for profile

### Connections

- `POST /api/connections` - Send connection request
- `PUT /api/connections/:id` - Update connection status
- `GET /api/connections/sent/:profile_id` - Get sent connections
- `GET /api/connections/received/:profile_id` - Get received connections
- `GET /api/connections/friends/:profile_id` - Get accepted connections

## Database Schema

### Tables

- **profiles**: User profile information
- **interests**: Interest tags for profiles
- **activities**: Preferred activities for profiles
- **connections**: Connection requests and friendships

All tables include Row Level Security (RLS) policies for secure access.

## Matching Algorithm

The matching algorithm is simple and rule-based:

```
match_score = shared_interests_count + shared_activities_count
```

Profiles are sorted by match score in descending order.

## Development Notes

- The app uses localStorage to remember the current user's profile ID
- No authentication is implemented (as per PRD requirements)
- All data is stored in Supabase
- CORS is enabled for local development

## Future Enhancements

Potential features for future versions:

- Real-time chat messaging
- Event suggestions
- Group functionality
- Profile pictures
- Location-based matching with maps
- Email notifications

## License

MIT
