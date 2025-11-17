const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
);

const sampleProfiles = [
  {
    name: 'Alex Chen',
    bio: 'Just moved to SF for a tech job. Love hiking and exploring new cafes!',
    city: 'San Francisco',
    neighborhood: 'Mission District',
    availability: 'weekend',
    interests: ['hiking', 'coffee', 'photography', 'tech'],
    activities: ['coffee chats', 'hiking', 'exploring the city']
  },
  {
    name: 'Sarah Johnson',
    bio: 'Recent grad working in marketing. Always up for trying new restaurants.',
    city: 'San Francisco',
    neighborhood: 'Marina',
    availability: 'both',
    interests: ['food', 'yoga', 'reading', 'travel'],
    activities: ['dinner parties', 'yoga classes', 'book clubs']
  },
  {
    name: 'Mike Rodriguez',
    bio: 'Software engineer who loves gaming and outdoor activities.',
    city: 'San Francisco',
    neighborhood: 'SOMA',
    availability: 'weekday',
    interests: ['gaming', 'hiking', 'tech', 'music'],
    activities: ['game nights', 'hiking', 'concerts']
  },
  {
    name: 'Emily Davis',
    bio: 'Artist and designer looking to meet creative people in the city.',
    city: 'San Francisco',
    neighborhood: 'Mission District',
    availability: 'weekend',
    interests: ['art', 'photography', 'coffee', 'design'],
    activities: ['art galleries', 'coffee chats', 'photography walks']
  },
  {
    name: 'James Park',
    bio: 'Finance analyst with a passion for fitness and healthy living.',
    city: 'San Francisco',
    neighborhood: 'Financial District',
    availability: 'both',
    interests: ['fitness', 'cooking', 'hiking', 'investing'],
    activities: ['gym sessions', 'cooking classes', 'hiking']
  }
];

async function seedDatabase() {
  console.log('Starting database seed...');

  try {
    for (const profileData of sampleProfiles) {
      // Create profile
      const { data: profile, error: profileError } = await supabase
        .from('profiles')
        .insert({
          name: profileData.name,
          bio: profileData.bio,
          city: profileData.city,
          neighborhood: profileData.neighborhood,
          availability: profileData.availability
        })
        .select()
        .single();

      if (profileError) {
        console.error('Error creating profile:', profileError);
        continue;
      }

      console.log(`Created profile: ${profile.name}`);

      // Add interests
      const interestsData = profileData.interests.map(tag => ({
        profile_id: profile.id,
        tag
      }));

      const { error: interestsError } = await supabase
        .from('interests')
        .insert(interestsData);

      if (interestsError) {
        console.error('Error adding interests:', interestsError);
      }

      // Add activities
      const activitiesData = profileData.activities.map(activity => ({
        profile_id: profile.id,
        activity
      }));

      const { error: activitiesError } = await supabase
        .from('activities')
        .insert(activitiesData);

      if (activitiesError) {
        console.error('Error adding activities:', activitiesError);
      }
    }

    console.log('Database seed completed successfully!');
  } catch (error) {
    console.error('Error seeding database:', error);
  }
}

seedDatabase();
