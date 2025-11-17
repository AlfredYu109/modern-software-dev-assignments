import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function CreateProfile({ onProfileCreated }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    bio: '',
    city: '',
    neighborhood: '',
    availability: ''
  });
  const [interests, setInterests] = useState([]);
  const [currentInterest, setCurrentInterest] = useState('');
  const [activities, setActivities] = useState([]);
  const [currentActivity, setCurrentActivity] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const addInterest = () => {
    if (currentInterest.trim()) {
      setInterests([...interests, currentInterest.trim()]);
      setCurrentInterest('');
    }
  };

  const removeInterest = (index) => {
    setInterests(interests.filter((_, i) => i !== index));
  };

  const addActivity = () => {
    if (currentActivity.trim()) {
      setActivities([...activities, currentActivity.trim()]);
      setCurrentActivity('');
    }
  };

  const removeActivity = (index) => {
    setActivities(activities.filter((_, i) => i !== index));
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
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...formData,
          interests,
          activities
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to create profile');
      }

      onProfileCreated(data.id);
      navigate(`/profiles/${data.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Create Your Profile</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name *</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Bio</label>
          <textarea
            name="bio"
            value={formData.bio}
            onChange={handleChange}
            placeholder="Tell us a bit about yourself..."
          />
        </div>

        <div className="form-group">
          <label>City</label>
          <input
            type="text"
            name="city"
            value={formData.city}
            onChange={handleChange}
            placeholder="e.g., San Francisco"
          />
        </div>

        <div className="form-group">
          <label>Neighborhood</label>
          <input
            type="text"
            name="neighborhood"
            value={formData.neighborhood}
            onChange={handleChange}
            placeholder="e.g., Mission District"
          />
        </div>

        <div className="form-group">
          <label>Availability</label>
          <select
            name="availability"
            value={formData.availability}
            onChange={handleChange}
          >
            <option value="">Select...</option>
            <option value="weekday">Weekdays</option>
            <option value="weekend">Weekends</option>
            <option value="both">Both</option>
          </select>
        </div>

        <div className="form-group">
          <label>Interests</label>
          <div className="tag-input-container">
            <input
              type="text"
              value={currentInterest}
              onChange={(e) => setCurrentInterest(e.target.value)}
              placeholder="e.g., hiking, photography"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  addInterest();
                }
              }}
            />
            <button
              type="button"
              onClick={addInterest}
              className="btn btn-secondary"
            >
              Add
            </button>
          </div>
          <div className="tag-list">
            {interests.map((interest, index) => (
              <div key={index} className="tag">
                {interest}
                <button type="button" onClick={() => removeInterest(index)}>
                  ×
                </button>
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
              placeholder="e.g., coffee chats, hiking"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  addActivity();
                }
              }}
            />
            <button
              type="button"
              onClick={addActivity}
              className="btn btn-secondary"
            >
              Add
            </button>
          </div>
          <div className="tag-list">
            {activities.map((activity, index) => (
              <div key={index} className="tag">
                {activity}
                <button type="button" onClick={() => removeActivity(index)}>
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Creating...' : 'Create Profile'}
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate('/')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default CreateProfile;
