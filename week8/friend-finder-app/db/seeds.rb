# Clear existing data
puts "Clearing existing data..."
EventParticipant.destroy_all
Message.destroy_all
Match.destroy_all
Event.destroy_all
Profile.destroy_all
User.destroy_all

puts "Creating users and profiles..."

# Create test users with profiles
users_data = [
  {
    name: "Alex Chen",
    email: "alex@example.com",
    age: 24,
    city: "San Francisco",
    interests: ["hiking", "coffee", "board games", "photography"],
    vibes: ["chill outdoorsy", "creative"],
    social_energy: "ambivert",
    preferred_formats: ["1-on-1 coffee", "small group hikes"],
    hometown: "Seattle",
    routine: "Free on weekends, likes morning coffee and evening walks"
  },
  {
    name: "Jordan Lee",
    email: "jordan@example.com",
    age: 23,
    city: "San Francisco",
    interests: ["music", "concerts", "cooking", "yoga"],
    vibes: ["social butterfly", "health-conscious"],
    social_energy: "extrovert",
    preferred_formats: ["group hangouts", "workout sessions"],
    hometown: "Portland",
    routine: "Evening yoga classes, weekend brunch enthusiast"
  },
  {
    name: "Sam Rivera",
    email: "sam@example.com",
    age: 25,
    city: "San Francisco",
    interests: ["gaming", "tech", "coffee", "books"],
    vibes: ["nerdy", "laid-back"],
    social_energy: "introvert",
    preferred_formats: ["1-on-1 coffee", "game nights"],
    hometown: "Austin",
    routine: "Prefer weeknight hangouts, love quiet cafes"
  },
  {
    name: "Taylor Kim",
    email: "taylor@example.com",
    age: 22,
    city: "San Francisco",
    interests: ["hiking", "photography", "art", "travel"],
    vibes: ["adventurous", "creative"],
    social_energy: "ambivert",
    preferred_formats: ["outdoor adventures", "museum trips"],
    hometown: "Denver",
    routine: "Weekends for adventures, weeknights for chill activities"
  },
  {
    name: "Morgan Smith",
    email: "morgan@example.com",
    age: 26,
    city: "San Francisco",
    interests: ["cooking", "board games", "hiking", "movies"],
    vibes: ["foodie", "game enthusiast"],
    social_energy: "ambivert",
    preferred_formats: ["dinner parties", "game nights"],
    hometown: "Boston",
    routine: "Love hosting weekend gatherings"
  }
]

users = users_data.map do |user_data|
  user = User.create!(
    name: user_data[:name],
    email: user_data[:email],
    password: "password123",
    password_confirmation: "password123",
    age: user_data[:age],
    city: user_data[:city],
    onboarded: true
  )

  Profile.create!(
    user: user,
    hometown: user_data[:hometown],
    interests: user_data[:interests],
    vibes: user_data[:vibes],
    social_energy: user_data[:social_energy],
    preferred_formats: user_data[:preferred_formats],
    routine: user_data[:routine]
  )

  user
end

puts "Created #{users.count} users with profiles"

# Create matches
puts "Creating matches..."
matches = []

# Alex <-> Jordan (accepted)
match1 = Match.create!(
  user: users[0],
  matched_user: users[1],
  status: 'accepted',
  compatibility_score: 75,
  last_contact: 2.days.ago
)
matches << match1

# Alex <-> Sam (pending)
match2 = Match.create!(
  user: users[0],
  matched_user: users[2],
  status: 'pending',
  compatibility_score: 85
)
matches << match2

# Jordan <-> Taylor (accepted)
match3 = Match.create!(
  user: users[1],
  matched_user: users[3],
  status: 'accepted',
  compatibility_score: 80,
  last_contact: 1.day.ago
)
matches << match3

# Sam <-> Morgan (accepted)
match4 = Match.create!(
  user: users[2],
  matched_user: users[4],
  status: 'accepted',
  compatibility_score: 90,
  last_contact: 3.hours.ago
)
matches << match4

puts "Created #{matches.count} matches"

# Create messages
puts "Creating messages..."
Message.create!(
  match: match1,
  sender: users[0],
  content: "Hey Jordan! Would love to grab coffee sometime!",
  read: true
)

Message.create!(
  match: match1,
  sender: users[1],
  content: "Hi Alex! That sounds great! How about this weekend?",
  read: true
)

Message.create!(
  match: match3,
  sender: users[1],
  content: "Hey Taylor! Saw you like photography. Want to go on a photo walk?",
  read: true
)

Message.create!(
  match: match4,
  sender: users[2],
  content: "Hi Morgan! Want to do a game night sometime?",
  read: true
)

Message.create!(
  match: match4,
  sender: users[4],
  content: "Yes! I love board games! How about Friday?",
  read: false
)

puts "Created messages"

# Create events
puts "Creating events..."

event1 = Event.create!(
  title: "Weekend Hike at Lands End",
  description: "Join us for a scenic hike followed by coffee!",
  location: "Lands End Trail, San Francisco",
  event_date: 2.days.from_now,
  max_participants: 6,
  category: "Outdoor",
  created_by: users[0]
)
EventParticipant.create!(event: event1, user: users[0], status: 'confirmed')
EventParticipant.create!(event: event1, user: users[1], status: 'confirmed')
EventParticipant.create!(event: event1, user: users[3], status: 'interested')

event2 = Event.create!(
  title: "Board Game Night",
  description: "Bring your favorite board games! We'll have snacks and drinks.",
  location: "Morgan's Place, Mission District",
  event_date: 5.days.from_now,
  max_participants: 8,
  category: "Social",
  created_by: users[4]
)
EventParticipant.create!(event: event2, user: users[4], status: 'confirmed')
EventParticipant.create!(event: event2, user: users[2], status: 'confirmed')
EventParticipant.create!(event: event2, user: users[0], status: 'interested')

event3 = Event.create!(
  title: "Brunch & Art Museum",
  description: "Brunch at Tartine, then explore SFMOMA",
  location: "Tartine Bakery, then SFMOMA",
  event_date: 7.days.from_now,
  max_participants: 5,
  category: "Culture",
  created_by: users[3]
)
EventParticipant.create!(event: event3, user: users[3], status: 'confirmed')
EventParticipant.create!(event: event3, user: users[1], status: 'interested')

puts "Created events"
puts ""
puts "✅ Seed data created successfully!"
puts ""
puts "Test accounts:"
puts "  Email: alex@example.com | Password: password123"
puts "  Email: jordan@example.com | Password: password123"
puts "  Email: sam@example.com | Password: password123"
puts "  Email: taylor@example.com | Password: password123"
puts "  Email: morgan@example.com | Password: password123"
