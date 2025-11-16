import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function Matches() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMatches();
  }, [id]);

  const fetchMatches = async () => {
    try {
      const response = await fetch(`/api/profiles/${id}/matches`);
      if (!response.ok) throw new Error('Failed to fetch matches');
      const data = await response.json();
      setMatches(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Your Matches</h1>
      <p style={{ marginBottom: '1.5rem', color: '#666' }}>
        Profiles sorted by shared interests and activities
      </p>

      {error && <div className="error">{error}</div>}

      {loading ? (
        <p>Finding your matches...</p>
      ) : matches.length === 0 ? (
        <div className="empty-state">
          <h3>No matches found yet</h3>
          <p>Add more interests to your profile or check back later as more people join!</p>
        </div>
      ) : (
        <div className="profile-grid">
          {matches.map((profile) => (
            <div
              key={profile.id}
              className="profile-card"
              onClick={() => navigate(`/profile/${profile.id}`)}
            >
              <h3>
                {profile.name}
                <span className="match-score">{profile.match_score} matches</span>
              </h3>
              {profile.city && (
                <p className="location">
                  {profile.city}{profile.neighborhood && `, ${profile.neighborhood}`}
                </p>
              )}
              {profile.bio && <p className="bio">{profile.bio}</p>}

              {profile.shared_interests && profile.shared_interests.length > 0 && (
                <div style={{ marginTop: '1rem' }}>
                  <strong style={{ fontSize: '0.9rem', color: '#666' }}>Shared Interests:</strong>
                  <div className="tags-list">
                    {profile.shared_interests.map((interest) => (
                      <div key={interest} className="tag">{interest}</div>
                    ))}
                  </div>
                </div>
              )}

              {profile.shared_activities && profile.shared_activities.length > 0 && (
                <div style={{ marginTop: '1rem' }}>
                  <strong style={{ fontSize: '0.9rem', color: '#666' }}>Shared Activities:</strong>
                  <div className="tags-list">
                    {profile.shared_activities.map((activity) => (
                      <div key={activity} className="tag">{activity}</div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Matches;
