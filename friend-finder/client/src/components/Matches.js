import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function Matches({ currentProfileId }) {
  const { id } = useParams();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchMatches();
    }
  }, [id]);

  const fetchMatches = async () => {
    try {
      const response = await fetch(`/api/profiles/${id}/matches`);
      const data = await response.json();
      setMatches(data);
    } catch (error) {
      console.error('Error fetching matches:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Finding your matches...</div>;
  }

  return (
    <div>
      <h2>Your Best Matches</h2>
      {matches.length === 0 ? (
        <div className="empty-state">
          <h3>No matches yet</h3>
          <p>Check back later as more people join!</p>
        </div>
      ) : (
        <div className="profile-list">
          {matches.map((profile) => (
            <div key={profile.id} className="profile-card">
              <h3>
                {profile.name}
                <span className="match-score">
                  Match Score: {profile.matchScore}
                </span>
              </h3>
              {(profile.city || profile.neighborhood) && (
                <div className="location">
                  {profile.city}
                  {profile.city && profile.neighborhood && ', '}
                  {profile.neighborhood}
                </div>
              )}
              {profile.bio && <p className="bio">{profile.bio}</p>}

              {profile.sharedInterests > 0 && (
                <p style={{ color: '#27ae60', fontWeight: 'bold' }}>
                  {profile.sharedInterests} shared interest
                  {profile.sharedInterests !== 1 ? 's' : ''}
                </p>
              )}

              {profile.sharedActivities > 0 && (
                <p style={{ color: '#27ae60', fontWeight: 'bold' }}>
                  {profile.sharedActivities} shared activit
                  {profile.sharedActivities !== 1 ? 'ies' : 'y'}
                </p>
              )}

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

export default Matches;
