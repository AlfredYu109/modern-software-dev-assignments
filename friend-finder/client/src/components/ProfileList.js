import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function ProfileList() {
  const [profiles, setProfiles] = useState([]);
  const [filteredProfiles, setFilteredProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    interest: '',
    city: '',
    neighborhood: '',
    availability: ''
  });

  useEffect(() => {
    fetchProfiles();
  }, []);

  const fetchProfiles = async () => {
    try {
      const response = await fetch('/api/profiles');
      const data = await response.json();
      setProfiles(data);
      setFilteredProfiles(data);
    } catch (error) {
      console.error('Error fetching profiles:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const applyFilters = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('/api/profiles/filter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(filters)
      });
      const data = await response.json();
      setFilteredProfiles(data);
    } catch (error) {
      console.error('Error filtering profiles:', error);
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setFilters({
      interest: '',
      city: '',
      neighborhood: '',
      availability: ''
    });
    setFilteredProfiles(profiles);
  };

  if (loading && profiles.length === 0) {
    return <div className="loading">Loading profiles...</div>;
  }

  return (
    <div className="profile-list">
      <h2>Browse Profiles</h2>

      <div className="filter-section">
        <h3>Filter Profiles</h3>
        <form onSubmit={applyFilters} className="filter-form">
          <div className="form-group">
            <label>Interest</label>
            <input
              type="text"
              name="interest"
              value={filters.interest}
              onChange={handleFilterChange}
              placeholder="e.g., hiking"
            />
          </div>

          <div className="form-group">
            <label>City</label>
            <input
              type="text"
              name="city"
              value={filters.city}
              onChange={handleFilterChange}
              placeholder="e.g., San Francisco"
            />
          </div>

          <div className="form-group">
            <label>Neighborhood</label>
            <input
              type="text"
              name="neighborhood"
              value={filters.neighborhood}
              onChange={handleFilterChange}
              placeholder="e.g., Mission"
            />
          </div>

          <div className="form-group">
            <label>Availability</label>
            <select
              name="availability"
              value={filters.availability}
              onChange={handleFilterChange}
            >
              <option value="">All</option>
              <option value="weekday">Weekdays</option>
              <option value="weekend">Weekends</option>
              <option value="both">Both</option>
            </select>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn btn-primary">
              Apply Filters
            </button>
            <button
              type="button"
              onClick={clearFilters}
              className="btn btn-secondary"
            >
              Clear
            </button>
          </div>
        </form>
      </div>

      {filteredProfiles.length === 0 ? (
        <div className="empty-state">
          <h3>No profiles found</h3>
          <p>Try adjusting your filters or check back later</p>
        </div>
      ) : (
        <div className="profile-list">
          {filteredProfiles.map((profile) => (
            <div key={profile.id} className="profile-card">
              <h3>{profile.name}</h3>
              {(profile.city || profile.neighborhood) && (
                <div className="location">
                  {profile.city}
                  {profile.city && profile.neighborhood && ', '}
                  {profile.neighborhood}
                </div>
              )}
              {profile.bio && <p className="bio">{profile.bio}</p>}

              {profile.interests && profile.interests.length > 0 && (
                <div>
                  <strong>Interests:</strong>
                  <div className="tags">
                    {profile.interests.map((interest) => (
                      <span key={interest.id} className="tag">
                        {interest.tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {profile.activities && profile.activities.length > 0 && (
                <div>
                  <strong>Activities:</strong>
                  <div className="tags">
                    {profile.activities.map((activity) => (
                      <span key={activity.id} className="tag">
                        {activity.activity}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {profile.availability && (
                <p>
                  <strong>Available:</strong> {profile.availability}
                </p>
              )}

              <div className="profile-actions">
                <Link
                  to={`/profiles/${profile.id}`}
                  className="btn btn-primary"
                >
                  View Profile
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ProfileList;
