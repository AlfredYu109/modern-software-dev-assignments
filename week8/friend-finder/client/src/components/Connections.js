import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function Connections({ currentProfileId }) {
  const { id } = useParams();
  const [requests, setRequests] = useState([]);
  const [friends, setFriends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchRequests();
      fetchFriends();
    }
  }, [id]);

  const fetchRequests = async () => {
    try {
      const response = await fetch(`/api/profiles/${id}/requests`);
      const data = await response.json();
      setRequests(data);
    } catch (error) {
      console.error('Error fetching requests:', error);
    }
  };

  const fetchFriends = async () => {
    try {
      const response = await fetch(`/api/profiles/${id}/friends`);
      const data = await response.json();
      setFriends(data);
    } catch (error) {
      console.error('Error fetching friends:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRequest = async (connectionId, status) => {
    try {
      const response = await fetch(`/api/connections/${connectionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status })
      });

      if (response.ok) {
        fetchRequests();
        fetchFriends();
      }
    } catch (error) {
      console.error('Error updating connection:', error);
      alert('Failed to update connection');
    }
  };

  if (loading) {
    return <div className="loading">Loading connections...</div>;
  }

  return (
    <div>
      <h2>Connections</h2>

      {requests.length > 0 && (
        <section style={{ marginBottom: '3rem' }}>
          <h3>Pending Requests ({requests.length})</h3>
          {requests.map((request) => (
            <div key={request.id} className="connection-card">
              <span className="status pending">Pending</span>
              <h4>{request.sender.name}</h4>
              {request.sender.city && (
                <p className="location">{request.sender.city}</p>
              )}
              {request.sender.bio && <p>{request.sender.bio}</p>}

              {request.sender.interests && request.sender.interests.length > 0 && (
                <div>
                  <strong>Interests:</strong>
                  <div className="tags">
                    {request.sender.interests.map((interest) => (
                      <span key={interest.id} className="tag">
                        {interest.tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="profile-actions">
                <button
                  onClick={() => handleRequest(request.id, 'accepted')}
                  className="btn btn-success"
                >
                  Accept
                </button>
                <button
                  onClick={() => handleRequest(request.id, 'declined')}
                  className="btn btn-danger"
                >
                  Decline
                </button>
                <Link
                  to={`/profiles/${request.sender.id}`}
                  className="btn btn-secondary"
                >
                  View Profile
                </Link>
              </div>
            </div>
          ))}
        </section>
      )}

      <section>
        <h3>My Friends ({friends.length})</h3>
        {friends.length === 0 ? (
          <div className="empty-state">
            <h4>No friends yet</h4>
            <p>Accept connection requests or browse profiles to find friends</p>
            <Link to="/profiles" className="btn btn-primary">
              Browse Profiles
            </Link>
          </div>
        ) : (
          <div className="profile-list">
            {friends.map((friend) => (
              <div key={friend.id} className="profile-card">
                <h3>{friend.name}</h3>
                {friend.city && <p className="location">{friend.city}</p>}
                {friend.bio && <p className="bio">{friend.bio}</p>}

                {friend.interests && friend.interests.length > 0 && (
                  <div>
                    <strong>Interests:</strong>
                    <div className="tags">
                      {friend.interests.map((interest) => (
                        <span key={interest.id} className="tag">
                          {interest.tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {friend.activities && friend.activities.length > 0 && (
                  <div>
                    <strong>Activities:</strong>
                    <div className="tags">
                      {friend.activities.map((activity) => (
                        <span key={activity.id} className="tag">
                          {activity.activity}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="profile-actions">
                  <Link
                    to={`/profiles/${friend.id}`}
                    className="btn btn-primary"
                  >
                    View Profile
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default Connections;
