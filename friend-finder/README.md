# Friend Finder Lite

A lightweight web application helping recent college graduates (ages 21-26) make new friends in their post-grad city. Built with the MERN stack (MongoDB replaced with Supabase PostgreSQL).

## Features

- **Profile Management**: Create, read, update, and delete your friend profile
- **Interest-Based Matching**: Find compatible friends based on shared interests and activities
- **Browse & Filter**: Search profiles by interests, location, and availability
- **Connection Requests**: Send and receive friend requests
- **Match Scoring**: Algorithm-based matching showing compatibility scores
- **Persistent Storage**: All data stored securely in Supabase

## Tech Stack

### Backend
- Node.js + Express
- Supabase (PostgreSQL database)
- RESTful API design

### Frontend
- React 18
- React Router for navigation
- Modern CSS with responsive design

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Supabase account (free tier works)

## Installation

### 1. Clone the repository

```bash
cd friend-finder
```

### 2. Set up Supabase

The database schema has already been created in your Supabase project with the following tables:
- `profiles` - User profile information
- `interests` - User interests (tags)
- `activities` - Preferred activities
- `connections` - Friend connection requests and status

### 3. Backend Setup

```bash
cd server
npm install
```

Create a `.env` file in the `server` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your Supabase credentials:

```
PORT=5000
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

You can find these values in your Supabase dashboard under Settings > API.

### 4. Frontend Setup

```bash
cd ../client
npm install
```

## Running the Application

### Development Mode

You need to run both the backend and frontend servers:

**Terminal 1 - Backend:**
```bash
cd server
npm start
# or for auto-reload:
npm run dev
```

The backend will run on `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
cd client
npm start
```

The frontend will run on `http://localhost:3000` and automatically proxy API requests to the backend.

### Access the Application

Open your browser and navigate to `http://localhost:3000`

## Usage Guide

### Creating a Profile

1. Click "Create Your Profile" on the home page
2. Fill in your details:
   - Name (required)
   - Bio
   - City and neighborhood
   - Availability (weekday/weekend/both)
   - Interests (tags like "hiking", "photography")
   - Preferred activities (like "coffee chats", "hiking")
3. Click "Create Profile"

### Browsing Profiles

1. Navigate to "Browse Profiles" from the navbar
2. Use filters to find specific people:
   - Filter by interest
   - Filter by city/neighborhood
   - Filter by availability
3. Click "View Profile" to see full details

### Finding Matches

1. Click "Matches" in the navbar
2. View profiles sorted by match score
3. Match scores are calculated based on:
   - Shared interests
   - Shared activities
   - Same city (bonus point)

### Connecting with Others

1. View a profile you're interested in
2. Click "Send Connection Request"
3. The other person will see your request in their Connections page
4. They can accept or decline
5. Accepted connections appear in "My Friends"

### Managing Your Profile

1. Click "My Profile" in the navbar
2. Click "Edit Profile" to update your information
3. Click "Delete Profile" to remove your account

## API Endpoints

### Profiles
- `GET /api/profiles` - Get all profiles
- `GET /api/profiles/:id` - Get single profile
- `POST /api/profiles` - Create new profile
- `PUT /api/profiles/:id` - Update profile
- `DELETE /api/profiles/:id` - Delete profile
- `POST /api/profiles/filter` - Filter profiles
- `GET /api/profiles/:id/matches` - Get match recommendations

### Connections
- `GET /api/profiles/:id/connections` - Get all connections
- `GET /api/profiles/:id/requests` - Get pending requests
- `GET /api/profiles/:id/friends` - Get accepted friends
- `POST /api/connections` - Send connection request
- `PUT /api/connections/:id` - Update connection status

## Database Schema

### profiles
- `id` (uuid, primary key)
- `name` (text, required)
- `bio` (text)
- `city` (text)
- `neighborhood` (text)
- `availability` (text: weekday/weekend/both)
- `created_at`, `updated_at` (timestamps)

### interests
- `id` (uuid, primary key)
- `profile_id` (foreign key to profiles)
- `tag` (text, required)

### activities
- `id` (uuid, primary key)
- `profile_id` (foreign key to profiles)
- `activity` (text, required)

### connections
- `id` (uuid, primary key)
- `sender_id` (foreign key to profiles)
- `receiver_id` (foreign key to profiles)
- `status` (text: pending/accepted/declined)
- `created_at`, `updated_at` (timestamps)

## Matching Algorithm

The matching algorithm is rule-based and calculates scores as follows:

```javascript
match_score = shared_interests_count + shared_activities_count + city_bonus

// Where:
// - shared_interests_count: Number of overlapping interest tags
// - shared_activities_count: Number of overlapping activities
// - city_bonus: +1 if both users are in the same city
```

Profiles are sorted by match score in descending order.

## Project Structure

```
friend-finder/
├── server/
│   ├── server.js           # Express server & API routes
│   ├── package.json        # Backend dependencies
│   └── .env               # Environment variables
├── client/
│   ├── public/
│   │   └── index.html     # HTML template
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── CreateProfile.js
│   │   │   ├── ProfileList.js
│   │   │   ├── ProfileDetail.js
│   │   │   ├── EditProfile.js
│   │   │   ├── Matches.js
│   │   │   └── Connections.js
│   │   ├── App.js         # Main app component
│   │   ├── App.css        # Styling
│   │   └── index.js       # React entry point
│   └── package.json       # Frontend dependencies
└── README.md
```

## Features Implemented

- ✅ Profile CRUD operations
- ✅ Interest and activity tagging
- ✅ Rule-based matching algorithm
- ✅ Profile browsing with filters
- ✅ Connection request system
- ✅ Friend list management
- ✅ Responsive design
- ✅ Persistent storage with Supabase

## Design Decisions

### Why Supabase over MongoDB?
- Built-in PostgreSQL provides strong relational data integrity
- Row Level Security (RLS) for data protection
- Automatic API generation
- Real-time subscriptions (future enhancement)
- Generous free tier

### Why Simple Matching Algorithm?
- Fast performance (< 200ms locally)
- Transparent scoring that users can understand
- No external dependencies or API calls
- Easy to extend with more factors

### Why No Authentication?
- MVP focuses on core functionality
- Simplified onboarding (one less barrier)
- Profile ID stored in localStorage for session management
- Production version should add proper auth

## Future Enhancements

- User authentication (email/password or OAuth)
- Real-time messaging between matched friends
- Profile pictures and photo upload
- Event creation and RSVP system
- Location-based search with maps
- Mobile app (React Native)
- Email notifications for connection requests
- Advanced matching with weighted preferences

## Troubleshooting

### Port Already in Use
If port 5000 or 3000 is already in use:
```bash
# Backend - change PORT in .env
PORT=5001

# Frontend - React will automatically suggest another port
```

### CORS Issues
Make sure the backend is running before starting the frontend. The frontend proxy is configured to forward requests to `http://localhost:5000`.

### Database Connection Errors
Verify your Supabase credentials in `server/.env`:
- Check the URL format is correct
- Ensure the anon key has proper permissions
- Verify your Supabase project is active

### Cannot Find Module Errors
Run `npm install` in both the server and client directories.

## License

MIT

## Contributing

This is a demo application for educational purposes. Feel free to fork and extend it for your own use.

## Support

For issues or questions, please open an issue in the repository.
