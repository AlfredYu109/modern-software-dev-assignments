# Quick Start Guide

Get Friend Finder Lite up and running in 5 minutes!

## Prerequisites

- Node.js v16+ installed
- A Supabase account (free at [supabase.com](https://supabase.com))

## Steps

### 1. Get Supabase Credentials

The database schema has already been created. You just need to get your credentials:

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Go to Settings → API
4. Copy these values:
   - Project URL
   - anon/public key

### 2. Configure Backend

```bash
cd server
npm install
cp .env.example .env
```

Edit `server/.env` and paste your Supabase credentials:
```
PORT=5000
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

### 3. Configure Frontend

```bash
cd ../client
npm install
```

### 4. Run the App

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
cd server
npm start
```

**Terminal 2 - Frontend:**
```bash
cd client
npm start
```

### 5. Open the App

Your browser should automatically open to `http://localhost:3000`

If not, manually navigate to that URL.

## First Steps

1. Click "Create Your Profile"
2. Fill in your information
3. Add some interests (e.g., "hiking", "photography", "gaming")
4. Add preferred activities (e.g., "coffee chats", "outdoor activities")
5. Click "Create Profile"
6. Browse other profiles or check your matches!

## Testing with Multiple Users

To test the matching and connection features:

1. Create a profile in one browser
2. Open an incognito/private window
3. Create a different profile with some overlapping interests
4. Send connection requests between profiles
5. Accept requests to become friends

## Troubleshooting

### "Cannot connect to server"
- Make sure the backend is running on port 5000
- Check your Supabase credentials in `.env`

### "Port already in use"
- Change the PORT in `server/.env` to 5001 or another available port
- The frontend will automatically use whatever port React suggests

### "Module not found"
- Run `npm install` in both server and client directories

## Optional: Run Both Simultaneously

From the root directory:
```bash
npm install
npm run install-all
npm run dev
```

This will start both servers at once using concurrently.

## Next Steps

- Create multiple test profiles to see matching in action
- Test the connection request flow
- Try the filter functionality
- Explore the matches page to see algorithm scoring

Enjoy connecting with friends! 🎉
