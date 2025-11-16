import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Browse() {
  const navigate = useNavigate();
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    city: '',
    neighborhood: '',
    interest: '',
    activity: '',
    availability: ''
  });

  useEffect(() => {
    fetchProfiles();
  }, []);

  const fetchProfiles = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });

      const response = await fetch(`/api/profiles?${params}`);
      if (!response.ok) throw new Error('Failed to fetch profiles');
      const data = await response.json();
      setProfiles(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFilterSubmit = (e) => {
    e.preventDefault();
    fetchProfiles();
  };

  const clearFilters = () => {
    setFilters({
      city: '',
      neighborhood: '',
      interest: '',
      activity: '',
      availability: ''
    });
    setTimeout(() => fetchProfiles(), 100);
  };

  return (
    <div>
      <div className="filters">
        <h3>Filter Profiles</h3>
        <form onSubmit={handleFilterSubmit}>
          <div className="filter-row">
            <div className="form-group">
              <label htmlFor="city">City</label>
              <input
                type="text"
                id="city"
                name="city"
                value={filters.city}
                onChange={handleFilterChange}
                placeholder="e.g., San Francisco"
              />
            </div>

            <div className="form-group">
              <label htmlFor="neighborhood">Neighborhood</label>
              <input
                type="text"
                id="neighborhood"
                name="neighborhood"
                value={filters.neighborhood}
                onChange={handleFilterChange}
                placeholder="e.g., Mission District"
              />
            </div>

            <div className="form-group">
              <label htmlFor="interest">Interest</label>
              <input
                type="text"
                id="interest"
                name="interest"
                value={filters.interest}
                onChange={handleFilterChange}
                placeholder="e.g., hiking"
              />
            </div>

            <div className="form-group">
              <label htmlFor="activity">Activity</label>
              <input
                type="text"
                id="activity"
                name="activity"
                value={filters.activity}
                onChange={handleFilterChange}
                placeholder="e.g., coffee"
              />
            </div>

            <div className="form-group">
              <label htmlFor="availability">Availability</label>
              <select
                id="availability"
                name="availability"
                value={filters.availability}
                onChange={handleFilterChange}
              >
                <option value="">All</option>
                <option value="weekday">Weekdays</option>
                <option value="weekend">Weekends</option>
              </select>
            </div>
          </div>

          <div className="button-group">
            <button type="submit" className="btn btn-primary">Apply Filters</button>
            <button type="button" onClick={clearFilters} className="btn btn-secondary">Clear</button>
          </div>
        </form>
      </div>

      <div className="container">
        <h1>Browse Profiles</h1>

        {error && <div className="error">{error}</div>}

        {loading ? (
          <p>Loading profiles...</p>
        ) : profiles.length === 0 ? (
          <div className="empty-state">
            <h3>No profiles found</h3>
            <p>Try adjusting your filters or check back later</p>
          </div>
        ) : (
          <div className="profile-grid">
            {profiles.map((profile) => (
              <div
                key={profile.id}
                className="profile-card"
                onClick={() => navigate(`/profile/${profile.id}`)}
              >
                <h3>{profile.name}</h3>
                {profile.city && (
                  <p className="location">
                    {profile.city}{profile.neighborhood && `, ${profile.neighborhood}`}
                  </p>
                )}
                {profile.bio && <p className="bio">{profile.bio}</p>}
                {profile.interests && profile.interests.length > 0 && (
                  <div className="tags-list">
                    {profile.interests.slice(0, 3).map((item) => (
                      <div key={item.tag} className="tag">{item.tag}</div>
                    ))}
                    {profile.interests.length > 3 && (
                      <div className="tag">+{profile.interests.length - 3} more</div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Browse;
