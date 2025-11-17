const express = require('express');
const cors = require('cors');
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize Supabase client
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Profile Routes

// Get all profiles
app.get('/api/profiles', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('profiles')
      .select(`
        *,
        interests (id, tag),
        activities (id, activity)
      `)
      .order('created_at', { ascending: false });

    if (error) throw error;
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get single profile
app.get('/api/profiles/:id', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('profiles')
      .select(`
        *,
        interests (id, tag),
        activities (id, activity)
      `)
      .eq('id', req.params.id)
      .maybeSingle();

    if (error) throw error;
    if (!data) return res.status(404).json({ error: 'Profile not found' });
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Create profile
app.post('/api/profiles', async (req, res) => {
  try {
    const { name, bio, city, neighborhood, availability, interests, activities } = req.body;

    if (!name || name.trim().length === 0) {
      return res.status(400).json({ error: 'Name is required' });
    }

    // Create profile
    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .insert({
        name: name.trim(),
        bio: bio?.trim() || null,
        city: city?.trim() || null,
        neighborhood: neighborhood?.trim() || null,
        availability: availability || null
      })
      .select()
      .single();

    if (profileError) throw profileError;

    // Add interests
    if (interests && interests.length > 0) {
      const interestsData = interests.map(tag => ({
        profile_id: profile.id,
        tag: tag.trim()
      }));

      const { error: interestsError } = await supabase
        .from('interests')
        .insert(interestsData);

      if (interestsError) throw interestsError;
    }

    // Add activities
    if (activities && activities.length > 0) {
      const activitiesData = activities.map(activity => ({
        profile_id: profile.id,
        activity: activity.trim()
      }));

      const { error: activitiesError } = await supabase
        .from('activities')
        .insert(activitiesData);

      if (activitiesError) throw activitiesError;
    }

    // Fetch complete profile
    const { data: completeProfile, error: fetchError } = await supabase
      .from('profiles')
      .select(`
        *,
        interests (id, tag),
        activities (id, activity)
      `)
      .eq('id', profile.id)
      .single();

    if (fetchError) throw fetchError;

    res.status(201).json(completeProfile);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update profile
app.put('/api/profiles/:id', async (req, res) => {
  try {
    const { name, bio, city, neighborhood, availability, interests, activities } = req.body;

    if (!name || name.trim().length === 0) {
      return res.status(400).json({ error: 'Name is required' });
    }

    // Update profile
    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .update({
        name: name.trim(),
        bio: bio?.trim() || null,
        city: city?.trim() || null,
        neighborhood: neighborhood?.trim() || null,
        availability: availability || null
      })
      .eq('id', req.params.id)
      .select()
      .single();

    if (profileError) throw profileError;

    // Delete existing interests and activities
    await supabase.from('interests').delete().eq('profile_id', req.params.id);
    await supabase.from('activities').delete().eq('profile_id', req.params.id);

    // Add new interests
    if (interests && interests.length > 0) {
      const interestsData = interests.map(tag => ({
        profile_id: req.params.id,
        tag: tag.trim()
      }));

      await supabase.from('interests').insert(interestsData);
    }

    // Add new activities
    if (activities && activities.length > 0) {
      const activitiesData = activities.map(activity => ({
        profile_id: req.params.id,
        activity: activity.trim()
      }));

      await supabase.from('activities').insert(activitiesData);
    }

    // Fetch complete profile
    const { data: completeProfile, error: fetchError } = await supabase
      .from('profiles')
      .select(`
        *,
        interests (id, tag),
        activities (id, activity)
      `)
      .eq('id', req.params.id)
      .single();

    if (fetchError) throw fetchError;

    res.json(completeProfile);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Delete profile
app.delete('/api/profiles/:id', async (req, res) => {
  try {
    const { error } = await supabase
      .from('profiles')
      .delete()
      .eq('id', req.params.id);

    if (error) throw error;
    res.json({ message: 'Profile deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Matching Routes

// Get matches for a profile
app.get('/api/profiles/:id/matches', async (req, res) => {
  try {
    // Get the current profile
    const { data: currentProfile, error: profileError } = await supabase
      .from('profiles')
      .select(`
        *,
        interests (tag),
        activities (activity)
      `)
      .eq('id', req.params.id)
      .single();

    if (profileError) throw profileError;

    // Get all other profiles
    const { data: allProfiles, error: allProfilesError } = await supabase
      .from('profiles')
      .select(`
        *,
        interests (tag),
        activities (activity)
      `)
      .neq('id', req.params.id);

    if (allProfilesError) throw allProfilesError;

    // Calculate match scores
    const currentInterests = currentProfile.interests.map(i => i.tag.toLowerCase());
    const currentActivities = currentProfile.activities.map(a => a.activity.toLowerCase());

    const matches = allProfiles.map(profile => {
      const profileInterests = profile.interests.map(i => i.tag.toLowerCase());
      const profileActivities = profile.activities.map(a => a.activity.toLowerCase());

      // Count shared tags and activities
      const sharedInterests = currentInterests.filter(tag =>
        profileInterests.includes(tag)
      ).length;

      const sharedActivities = currentActivities.filter(activity =>
        profileActivities.includes(activity)
      ).length;

      // Bonus for same city
      const cityBonus = (currentProfile.city && profile.city &&
        currentProfile.city.toLowerCase() === profile.city.toLowerCase()) ? 1 : 0;

      const matchScore = sharedInterests + sharedActivities + cityBonus;

      return {
        ...profile,
        matchScore,
        sharedInterests,
        sharedActivities
      };
    });

    // Sort by match score (highest first)
    matches.sort((a, b) => b.matchScore - a.matchScore);

    res.json(matches);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Filter profiles
app.post('/api/profiles/filter', async (req, res) => {
  try {
    const { interest, city, neighborhood, availability } = req.body;

    let query = supabase
      .from('profiles')
      .select(`
        *,
        interests (id, tag),
        activities (id, activity)
      `);

    if (city) {
      query = query.ilike('city', `%${city}%`);
    }

    if (neighborhood) {
      query = query.ilike('neighborhood', `%${neighborhood}%`);
    }

    if (availability) {
      query = query.eq('availability', availability);
    }

    const { data, error } = await query;

    if (error) throw error;

    // Filter by interest if provided
    let filteredData = data;
    if (interest) {
      filteredData = data.filter(profile =>
        profile.interests.some(i =>
          i.tag.toLowerCase().includes(interest.toLowerCase())
        )
      );
    }

    res.json(filteredData);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Connection Routes

// Get all connections for a profile
app.get('/api/profiles/:id/connections', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('connections')
      .select(`
        *,
        sender:sender_id (id, name, bio, city),
        receiver:receiver_id (id, name, bio, city)
      `)
      .or(`sender_id.eq.${req.params.id},receiver_id.eq.${req.params.id}`)
      .order('created_at', { ascending: false });

    if (error) throw error;
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get pending connection requests (received)
app.get('/api/profiles/:id/requests', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('connections')
      .select(`
        *,
        sender:sender_id (id, name, bio, city, interests (tag), activities (activity))
      `)
      .eq('receiver_id', req.params.id)
      .eq('status', 'pending')
      .order('created_at', { ascending: false });

    if (error) throw error;
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Send connection request
app.post('/api/connections', async (req, res) => {
  try {
    const { sender_id, receiver_id } = req.body;

    if (!sender_id || !receiver_id) {
      return res.status(400).json({ error: 'Sender and receiver IDs are required' });
    }

    if (sender_id === receiver_id) {
      return res.status(400).json({ error: 'Cannot send connection request to yourself' });
    }

    // Check if connection already exists
    const { data: existing } = await supabase
      .from('connections')
      .select('*')
      .or(`and(sender_id.eq.${sender_id},receiver_id.eq.${receiver_id}),and(sender_id.eq.${receiver_id},receiver_id.eq.${sender_id})`)
      .maybeSingle();

    if (existing) {
      return res.status(400).json({ error: 'Connection request already exists' });
    }

    const { data, error } = await supabase
      .from('connections')
      .insert({
        sender_id,
        receiver_id,
        status: 'pending'
      })
      .select()
      .single();

    if (error) throw error;
    res.status(201).json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update connection status
app.put('/api/connections/:id', async (req, res) => {
  try {
    const { status } = req.body;

    if (!['accepted', 'declined'].includes(status)) {
      return res.status(400).json({ error: 'Invalid status' });
    }

    const { data, error } = await supabase
      .from('connections')
      .update({ status })
      .eq('id', req.params.id)
      .select()
      .single();

    if (error) throw error;
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get matched friends (accepted connections)
app.get('/api/profiles/:id/friends', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('connections')
      .select(`
        *,
        sender:sender_id (id, name, bio, city, interests (tag), activities (activity)),
        receiver:receiver_id (id, name, bio, city, interests (tag), activities (activity))
      `)
      .or(`sender_id.eq.${req.params.id},receiver_id.eq.${req.params.id}`)
      .eq('status', 'accepted')
      .order('updated_at', { ascending: false });

    if (error) throw error;

    // Format the response to show the friend (not the current user)
    const friends = data.map(connection => {
      const isSender = connection.sender_id === req.params.id;
      const friend = isSender ? connection.receiver : connection.sender;
      return {
        connectionId: connection.id,
        ...friend
      };
    });

    res.json(friends);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
