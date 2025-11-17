import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function EditProfile() {
  const { id } = useParams();
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
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, [id]);

  const fetchProfile = async () => {
    try {
      const response = await fetch(`/api/profiles/${id}`);
      const data = await response.json();

      setFormData({
        name: data.name,
        bio: data.bio || '',
        city: data.city || '',
        neighborhood: data.neighborhood || '',
        availability: data.availability || ''
      });

      setInterests(data.interests ? data.interests.map(i => i.tag) : []);
      setActivities(data.activities ? data.activities.map(a => a.activity) : []);
    } catch (error) {
      setError('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

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
    setSaving(true);

    if (!formData.name.trim()) {
      setError('Name is required');
      setSaving(false);
      return;
    }

    try {
      const response = await fetch(`/api/profiles/${id}`, {
        method: 'PUT',
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
        throw new Error(data.error || 'Failed to update profile');
      }

      navigate(`/profiles/${id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading profile...</div>;
  }

  return (
    <div className="form-container">
      <h2>Edit Profile</h2>
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
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate(`/profiles/${id}`)}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default EditProfile;
