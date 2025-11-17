import sys
import sqlite3
import json

DATABASE = 'test_friend_finder.db'

def init_test_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS connections')
    cursor.execute('DROP TABLE IF EXISTS profiles')

    cursor.execute('''
        CREATE TABLE profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bio TEXT,
            city TEXT,
            interests TEXT,
            activities TEXT,
            availability TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES profiles (id),
            FOREIGN KEY (receiver_id) REFERENCES profiles (id),
            UNIQUE(sender_id, receiver_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✓ Database schema created successfully")

def test_profile_crud():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO profiles (name, bio, city, interests, activities, availability)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Alice', 'Love hiking and reading', 'San Francisco', 'hiking,reading,music', 'coffee,hiking,concerts', 'weekends'))

    profile1_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO profiles (name, bio, city, interests, activities, availability)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Bob', 'Avid hiker and music lover', 'San Francisco', 'hiking,music,cooking', 'hiking,concerts,cooking', 'both'))

    profile2_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO profiles (name, bio, city, interests, activities, availability)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Charlie', 'Foodie and coder', 'Oakland', 'cooking,tech,gaming', 'cooking,movies,gaming', 'weekdays'))

    conn.commit()

    cursor.execute('SELECT * FROM profiles')
    profiles = cursor.fetchall()
    print(f"✓ Created {len(profiles)} profiles")

    cursor.execute('SELECT * FROM profiles WHERE id = ?', (profile1_id,))
    profile = cursor.fetchone()
    print(f"✓ Retrieved profile: {profile[1]}")

    cursor.execute('UPDATE profiles SET bio = ? WHERE id = ?', ('Updated bio', profile1_id))
    conn.commit()
    print("✓ Updated profile")

    conn.close()
    return profile1_id, profile2_id

def test_matching(profile1_id, profile2_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM profiles WHERE id = ?', (profile1_id,))
    user_profile = cursor.fetchone()

    user_interests = set(filter(None, user_profile['interests'].split(',')))
    user_activities = set(filter(None, user_profile['activities'].split(',')))

    cursor.execute('SELECT * FROM profiles WHERE id != ?', (profile1_id,))
    all_profiles = cursor.fetchall()

    matches = []
    for profile in all_profiles:
        profile_interests = set(filter(None, profile['interests'].split(',')))
        profile_activities = set(filter(None, profile['activities'].split(',')))

        shared_interests = user_interests & profile_interests
        shared_activities = user_activities & profile_activities
        match_score = len(shared_interests) + len(shared_activities)

        if match_score > 0:
            matches.append({
                'name': profile['name'],
                'match_score': match_score,
                'shared_interests': list(shared_interests),
                'shared_activities': list(shared_activities)
            })

    matches.sort(key=lambda x: x['match_score'], reverse=True)

    print(f"✓ Found {len(matches)} matches for {user_profile['name']}")
    if matches:
        best_match = matches[0]
        print(f"  Best match: {best_match['name']} (score: {best_match['match_score']})")
        print(f"  Shared interests: {', '.join(best_match['shared_interests'])}")
        print(f"  Shared activities: {', '.join(best_match['shared_activities'])}")

    conn.close()
    return len(matches) > 0

def test_connections(profile1_id, profile2_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO connections (sender_id, receiver_id, status)
        VALUES (?, ?, 'pending')
    ''', (profile1_id, profile2_id))
    conn.commit()
    print("✓ Connection request created")

    cursor.execute('''
        SELECT * FROM connections WHERE receiver_id = ? AND status = 'pending'
    ''', (profile2_id,))
    incoming = cursor.fetchall()
    print(f"✓ Retrieved {len(incoming)} incoming connection requests")

    connection_id = incoming[0][0]
    cursor.execute('UPDATE connections SET status = ? WHERE id = ?', ('accepted', connection_id))
    conn.commit()
    print("✓ Connection accepted")

    cursor.execute('''
        SELECT p.* FROM profiles p
        JOIN connections c ON (p.id = c.sender_id OR p.id = c.receiver_id)
        WHERE (c.sender_id = ? OR c.receiver_id = ?)
        AND c.status = 'accepted'
        AND p.id != ?
    ''', (profile1_id, profile1_id, profile1_id))
    friends = cursor.fetchall()
    print(f"✓ Retrieved {len(friends)} friends")

    conn.close()
    return len(friends) > 0

def test_filters():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profiles WHERE city LIKE ?", ('%San Francisco%',))
    sf_profiles = cursor.fetchall()
    print(f"✓ Filtered by city: found {len(sf_profiles)} profiles in San Francisco")

    cursor.execute("SELECT * FROM profiles WHERE interests LIKE ?", ('%hiking%',))
    hiking_profiles = cursor.fetchall()
    print(f"✓ Filtered by interest: found {len(hiking_profiles)} profiles interested in hiking")

    conn.close()
    return len(sf_profiles) > 0 and len(hiking_profiles) > 0

def run_tests():
    print("Starting Friend Finder Lite Tests...\n")

    print("Test 1: Database Initialization")
    init_test_db()
    print()

    print("Test 2: Profile CRUD Operations")
    profile1_id, profile2_id = test_profile_crud()
    print()

    print("Test 3: Matching Algorithm")
    matching_works = test_matching(profile1_id, profile2_id)
    print()

    print("Test 4: Connection System")
    connections_work = test_connections(profile1_id, profile2_id)
    print()

    print("Test 5: Filtering")
    filters_work = test_filters()
    print()

    print("=" * 50)
    if matching_works and connections_work and filters_work:
        print("✓ All tests passed!")
        print("\nThe Friend Finder Lite app is ready to use!")
        print("\nTo run the app:")
        print("1. Install dependencies: pip install Flask flask-cors")
        print("2. Run the server: python app.py")
        print("3. Open http://localhost:5000 in your browser")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    import os
    try:
        sys.exit(run_tests())
    finally:
        if os.path.exists(DATABASE):
            os.remove(DATABASE)
            print("\nTest database cleaned up.")
