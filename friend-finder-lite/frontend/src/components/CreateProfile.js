import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function CreateProfile({ onProfileCreated }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    bio: '',
    city: '',
    neighborhood: '',
    availability: []
  });
  const [interests, setInterests] = useState([]);
  const [activities, setActivities] = useState([]);
  const [currentInterest, setCurrentInterest] = useState('');
  const [currentActivity, setCurrentActivity] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (type === 'checkbox') {
      setFormData(prev => ({
        ...prev,
        availability: checked
          ? [...prev.availability, value]
          : prev.availability.filter(v => v !== value)
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const addInterest = () => {
    if (currentInterest.trim() && !interests.includes(currentInterest.trim())) {
      setInterests([...interests, currentInterest.trim()]);
      setCurrentInterest('');
    }
  };

  const removeInterest = (interest) => {
    setInterests(interests.filter(i => i !== interest));
  };

  const addActivity = () => {
    if (currentActivity.trim() && !activities.includes(currentActivity.trim())) {
      setActivities([...activities, currentActivity.trim()]);
      setCurrentActivity('');
    }
  };

  const removeActivity = (activity) => {
    setActivities(activities.filter(a => a !== activity));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!formData.name.trim()) {
      setError('Name is required');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('/api/profiles', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          interests,
          activities
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to create profile');
      }

      const profile = await response.json();
      onProfileCreated(profile);
      navigate(`/profile/${profile.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Create Your Profile</h1>

      {error && <div className="error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name *</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="bio">Bio</label>
          <textarea
            id="bio"
            name="bio"
            value={formData.bio}
            onChange={handleChange}
            placeholder="Tell us about yourself..."
          />
        </div>

        <div className="form-group">
          <label htmlFor="city">City</label>
          <input
            type="text"
            id="city"
            name="city"
            value={formData.city}
            onChange={handleChange}
            placeholder="e.g., San Francisco"
          />
        </div>

        <div className="form-group">
          <label htmlFor="neighborhood">Neighborhood</label>
          <input
            type="text"
            id="neighborhood"
            name="neighborhood"
            value={formData.neighborhood}
            onChange={handleChange}
            placeholder="e.g., Mission District"
          />
        </div>

        <div className="form-group">
          <label>Interests</label>
          <div className="tag-input-container">
            <input
              type="text"
              value={currentInterest}
              onChange={(e) => setCurrentInterest(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addInterest())}
              placeholder="e.g., hiking, cooking, photography"
            />
            <button type="button" onClick={addInterest} className="btn btn-secondary">
              Add
            </button>
          </div>
          <div className="tags-list">
            {interests.map((interest) => (
              <div key={interest} className="tag">
                {interest}
                <button type="button" onClick={() => removeInterest(interest)}>×</button>
              </div>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Preferred Activities</label>
          <div className="tag-input-container">
            <input
              type="text"
              value={currentActivity}
              onChange={(e) => setCurrentActivity(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addActivity())}
              placeholder="e.g., coffee, movies, sports"
            />
            <button type="button" onClick={addActivity} className="btn btn-secondary">
              Add
            </button>
          </div>
          <div className="tags-list">
            {activities.map((activity) => (
              <div key={activity} className="tag">
                {activity}
                <button type="button" onClick={() => removeActivity(activity)}>×</button>
              </div>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Availability</label>
          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                name="availability"
                value="weekday"
                checked={formData.availability.includes('weekday')}
                onChange={handleChange}
              />
              Weekdays
            </label>
            <label>
              <input
                type="checkbox"
                name="availability"
                value="weekend"
                checked={formData.availability.includes('weekend')}
                onChange={handleChange}
              />
              Weekends
            </label>
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Creating...' : 'Create Profile'}
        </button>
      </form>
    </div>
  );
}

export default CreateProfile;
