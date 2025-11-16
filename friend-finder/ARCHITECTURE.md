# Friend Finder Lite - Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  React Frontend                       │  │
│  │                  (Port 3000)                          │  │
│  │                                                        │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │  Create  │  │  Browse  │  │  Matches │          │  │
│  │  │ Profile  │  │ Profiles │  │          │          │  │
│  │  └──────────┘  └──────────┘  └──────────┘          │  │
│  │                                                        │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │  Profile │  │   Edit   │  │Connection│          │  │
│  │  │  Detail  │  │ Profile  │  │    s     │          │  │
│  │  └──────────┘  └──────────┘  └──────────┘          │  │
│  │                                                        │  │
│  └────────────────────┬───────────────────────────────────┘
│                       │ HTTP/REST API                        │
│                       │ (fetch calls)                        │
└───────────────────────┼──────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Express Backend                           │
│                    (Port 5000)                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   API Routes                          │  │
│  │                                                        │  │
│  │  • POST   /api/profiles         - Create profile     │  │
│  │  • GET    /api/profiles         - List all           │  │
│  │  • GET    /api/profiles/:id     - Get one            │  │
│  │  • PUT    /api/profiles/:id     - Update             │  │
│  │  • DELETE /api/profiles/:id     - Delete             │  │
│  │  • POST   /api/profiles/filter  - Filter profiles    │  │
│  │  • GET    /api/profiles/:id/matches  - Get matches   │  │
│  │                                                        │  │
│  │  • POST /api/connections              - Send request │  │
│  │  • PUT  /api/connections/:id          - Update       │  │
│  │  • GET  /api/profiles/:id/connections - List all     │  │
│  │  • GET  /api/profiles/:id/requests    - Pending      │  │
│  │  • GET  /api/profiles/:id/friends     - Accepted     │  │
│  │                                                        │  │
│  └────────────────────┬─────────────────────────────────────┘
│                       │                                      │
│                       │ Supabase Client                      │
│                       │ (@supabase/supabase-js)             │
└───────────────────────┼──────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Supabase Cloud                            │
│                    (PostgreSQL)                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   Database Tables                     │  │
│  │                                                        │  │
│  │  profiles                                             │  │
│  │  ├─ id (uuid)                                         │  │
│  │  ├─ name (text)                                       │  │
│  │  ├─ bio (text)                                        │  │
│  │  ├─ city (text)                                       │  │
│  │  ├─ neighborhood (text)                               │  │
│  │  ├─ availability (enum)                               │  │
│  │  └─ timestamps                                        │  │
│  │                                                        │  │
│  │  interests                                            │  │
│  │  ├─ id (uuid)                                         │  │
│  │  ├─ profile_id (fk → profiles)                        │  │
│  │  └─ tag (text)                                        │  │
│  │                                                        │  │
│  │  activities                                           │  │
│  │  ├─ id (uuid)                                         │  │
│  │  ├─ profile_id (fk → profiles)                        │  │
│  │  └─ activity (text)                                   │  │
│  │                                                        │  │
│  │  connections                                          │  │
│  │  ├─ id (uuid)                                         │  │
│  │  ├─ sender_id (fk → profiles)                         │  │
│  │  ├─ receiver_id (fk → profiles)                       │  │
│  │  ├─ status (enum: pending/accepted/declined)         │  │
│  │  └─ timestamps                                        │  │
│  │                                                        │  │
│  └────────────────────────────────────────────────────────┘
│                                                              │
│  Row Level Security (RLS) - Public access for MVP          │
│  Indexes on foreign keys for performance                    │
│  Cascade deletes for data integrity                         │
└──────────────────────────────────────────────────────────────┘
```

## Component Hierarchy

```
App (Router)
│
├─ Navbar (always visible)
│  ├─ Logo/Brand
│  └─ Navigation Links
│     ├─ Browse
│     ├─ Matches
│     ├─ Connections
│     ├─ My Profile
│     └─ Logout
│
├─ Route: / (Home)
│  └─ Welcome Screen
│     ├─ Hero Section
│     └─ CTA Buttons
│
├─ Route: /create
│  └─ CreateProfile
│     ├─ Form Fields
│     ├─ Tag Input (interests)
│     ├─ Tag Input (activities)
│     └─ Submit Button
│
├─ Route: /profiles
│  └─ ProfileList
│     ├─ FilterSection
│     │  └─ Filter Form
│     └─ Profile Cards (map)
│        └─ View Profile Button
│
├─ Route: /profiles/:id
│  └─ ProfileDetail
│     ├─ Profile Header
│     ├─ Bio Section
│     ├─ Interests Display
│     ├─ Activities Display
│     └─ Actions
│        ├─ Send Request (if not own)
│        ├─ Edit (if own)
│        └─ Delete (if own)
│
├─ Route: /profiles/:id/edit
│  └─ EditProfile
│     └─ (Same structure as CreateProfile)
│
├─ Route: /profiles/:id/matches
│  └─ Matches
│     └─ Profile Cards with Match Scores
│        ├─ Match Score Badge
│        ├─ Shared Interests Count
│        └─ Shared Activities Count
│
└─ Route: /profiles/:id/connections
   └─ Connections
      ├─ Pending Requests Section
      │  └─ Request Cards
      │     ├─ Accept Button
      │     ├─ Decline Button
      │     └─ View Profile
      │
      └─ Friends Section
         └─ Friend Cards
            └─ View Profile Button
```

## Data Flow

### Creating a Profile

```
User fills form
      ↓
Form submission
      ↓
React state validation
      ↓
POST /api/profiles
      ↓
Express receives request
      ↓
Validates required fields
      ↓
Supabase: INSERT INTO profiles
      ↓
Supabase: INSERT INTO interests (multiple)
      ↓
Supabase: INSERT INTO activities (multiple)
      ↓
Fetch complete profile with joins
      ↓
Return to frontend
      ↓
Store profile ID in localStorage
      ↓
Navigate to profile page
```

### Viewing Matches

```
User clicks "Matches"
      ↓
GET /api/profiles/:id/matches
      ↓
Express fetches current profile with interests/activities
      ↓
Express fetches all other profiles with interests/activities
      ↓
For each profile:
    Calculate shared interests
    Calculate shared activities
    Add city bonus if same
    Sum = match score
      ↓
Sort by match score (descending)
      ↓
Return sorted array
      ↓
Frontend displays with scores
```

### Sending Connection Request

```
User clicks "Send Connection Request"
      ↓
POST /api/connections
      ↓
Express validates:
    • sender_id exists
    • receiver_id exists
    • Not same person
    • No existing connection
      ↓
Supabase: INSERT INTO connections
    status = 'pending'
      ↓
Return connection record
      ↓
Update UI to show "Request Pending"
```

### Accepting Connection

```
Receiver views "Connections" page
      ↓
GET /api/profiles/:id/requests
      ↓
Display pending requests
      ↓
User clicks "Accept"
      ↓
PUT /api/connections/:id
    status = 'accepted'
      ↓
Supabase: UPDATE connections
      ↓
Refresh requests and friends lists
      ↓
Request moves to "My Friends"
```

## State Management

### Frontend State

```javascript
// App.js - Global state
currentProfileId (localStorage + state)

// Each component maintains local state
CreateProfile:
  - formData (name, bio, city, etc.)
  - interests array
  - activities array
  - error state
  - loading state

ProfileList:
  - profiles array
  - filteredProfiles array
  - filters object
  - loading state

ProfileDetail:
  - profile object
  - connectionStatus
  - loading state
  - error state

Matches:
  - matches array (sorted)
  - loading state

Connections:
  - requests array
  - friends array
  - loading state
```

### Backend State

```javascript
// Stateless - each request is independent
// State stored in:
// 1. Database (persistent)
// 2. Session (via localStorage on frontend)
// 3. Request context (during processing)
```

## Security Model

### Database Level (Supabase RLS)

```sql
-- All tables have RLS enabled
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE interests ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE connections ENABLE ROW LEVEL SECURITY;

-- Public access policies (MVP - no auth)
CREATE POLICY "Anyone can read profiles"
  ON profiles FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE POLICY "Anyone can create profiles"
  ON profiles FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

-- Similar for UPDATE, DELETE, and other tables
```

### Application Level

```javascript
// Input validation
if (!name || name.trim().length === 0) {
  return res.status(400).json({ error: 'Name is required' });
}

// Business logic validation
if (sender_id === receiver_id) {
  return res.status(400).json({
    error: 'Cannot send connection request to yourself'
  });
}

// SQL injection prevention
// Supabase client uses parameterized queries automatically
await supabase
  .from('profiles')
  .select('*')
  .eq('id', userId)  // Safe - parameterized
```

## Matching Algorithm

```javascript
// Pseudo-code implementation
function calculateMatchScore(currentProfile, otherProfile) {
  let score = 0;

  // Count shared interests
  const currentInterests = currentProfile.interests.map(i => i.tag.toLowerCase());
  const otherInterests = otherProfile.interests.map(i => i.tag.toLowerCase());

  for (const interest of currentInterests) {
    if (otherInterests.includes(interest)) {
      score += 1;  // +1 for each shared interest
    }
  }

  // Count shared activities
  const currentActivities = currentProfile.activities.map(a => a.activity.toLowerCase());
  const otherActivities = otherProfile.activities.map(a => a.activity.toLowerCase());

  for (const activity of currentActivities) {
    if (otherActivities.includes(activity)) {
      score += 1;  // +1 for each shared activity
    }
  }

  // City bonus
  if (currentProfile.city && otherProfile.city &&
      currentProfile.city.toLowerCase() === otherProfile.city.toLowerCase()) {
    score += 1;  // +1 for same city
  }

  return score;
}

// Sort profiles by score
matches.sort((a, b) => b.matchScore - a.matchScore);
```

## Performance Optimizations

### Database
- Indexes on foreign keys (automatic with FK constraints)
- Indexes on frequently queried columns
- Proper use of JOINs vs multiple queries
- Cascade deletes reduce cleanup queries

### Backend
- Single query for profile with nested relations
- Efficient matching algorithm (O(n*m) where n=profiles, m=avg tags)
- Proper error handling prevents retries
- Connection pooling via Supabase client

### Frontend
- React Router lazy loading (code splitting)
- Conditional rendering reduces DOM nodes
- Proper use of keys in lists
- Loading states prevent duplicate requests
- LocalStorage for session persistence

## Scalability Considerations

### Current Limitations
- No caching (each request hits database)
- No pagination on profile list
- No rate limiting
- No connection pooling management

### Future Improvements
```
1. Add Redis caching layer
   - Cache profile data (TTL: 5 minutes)
   - Cache match scores (TTL: 1 hour)
   - Invalidate on updates

2. Implement pagination
   - Cursor-based for matches
   - Offset-based for browse

3. Add rate limiting
   - Per IP: 100 requests/hour
   - Per profile: 50 requests/hour

4. Database optimization
   - Materialized views for matches
   - Read replicas for queries
   - Write to primary only

5. Backend scaling
   - Horizontal scaling with load balancer
   - Stateless design enables this
   - Session in database, not memory

6. Frontend optimization
   - CDN for static assets
   - Service worker for offline
   - Virtual scrolling for long lists
```

## Monitoring & Observability

### Key Metrics to Track

```
Backend:
- Request rate (requests/second)
- Response time (p50, p95, p99)
- Error rate (%)
- Database query time
- Active connections

Frontend:
- Page load time
- Time to interactive
- API call success rate
- JavaScript errors

Database:
- Query performance
- Connection pool usage
- Storage size
- Index usage
```

### Logging Strategy

```javascript
// Backend
console.log(`[${new Date().toISOString()}] ${method} ${path} - ${statusCode}`);

// Error logging
console.error(`[ERROR] ${error.message}`, {
  path: req.path,
  body: req.body,
  stack: error.stack
});

// Future: Use structured logging
// Winston, Pino, or cloud logging service
```

## Deployment Architecture

### Development
```
Local Machine
├─ Frontend: localhost:3000 (React Dev Server)
└─ Backend: localhost:5000 (Node Express)
    └─ Database: Supabase Cloud (shared)
```

### Production (Option 1: Render)
```
Internet
  ↓
Render CDN
  ↓
Frontend Static Site (Render)
  ↓ API calls
Backend Web Service (Render)
  ↓
Supabase Cloud (PostgreSQL)
```

### Production (Option 2: Traditional VPS)
```
Internet
  ↓
Nginx (reverse proxy)
├─ / → Frontend (static files)
└─ /api → Backend (PM2 process)
    ↓
Supabase Cloud (PostgreSQL)
```

## Error Handling Flow

```
Error occurs
  ↓
Backend catches error
  ↓
Log error details
  ↓
Send user-friendly response
  {
    error: "Profile not found",
    statusCode: 404
  }
  ↓
Frontend receives error
  ↓
Display to user
  - Toast notification
  - Error message
  - Fallback UI
  ↓
User can retry or navigate away
```

## Testing Strategy

### Unit Tests (Future)
```javascript
// Backend
test('calculateMatchScore returns correct score', () => {
  const profile1 = { interests: ['hiking'], activities: ['coffee'] };
  const profile2 = { interests: ['hiking'], activities: ['dinner'] };
  expect(calculateMatchScore(profile1, profile2)).toBe(1);
});

// Frontend
test('CreateProfile validates required fields', () => {
  render(<CreateProfile />);
  fireEvent.click(screen.getByText('Create Profile'));
  expect(screen.getByText('Name is required')).toBeInTheDocument();
});
```

### Integration Tests (Future)
```javascript
test('User can create profile and view it', async () => {
  // Create profile
  const profile = await api.post('/api/profiles', testData);

  // Fetch profile
  const fetched = await api.get(`/api/profiles/${profile.id}`);

  expect(fetched.name).toBe(testData.name);
});
```

### E2E Tests (Future)
```javascript
test('Complete user flow', async () => {
  // 1. Create profile
  await page.goto('/create');
  await page.fill('[name="name"]', 'Test User');
  await page.click('button[type="submit"]');

  // 2. Browse profiles
  await page.click('a:has-text("Browse")');
  await expect(page).toHaveURL(/\/profiles$/);

  // 3. View match
  await page.click('a:has-text("Matches")');
  await page.click('button:has-text("View Profile")');

  // 4. Send request
  await page.click('button:has-text("Send Connection Request")');
  await expect(page.locator('text=Request Pending')).toBeVisible();
});
```

This architecture provides a solid foundation that's easy to understand, maintain, and scale as the application grows.
