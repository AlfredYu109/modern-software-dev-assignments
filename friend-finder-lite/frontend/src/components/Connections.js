import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function Connections() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [sentConnections, setSentConnections] = useState([]);
  const [receivedConnections, setReceivedConnections] = useState([]);
  const [friends, setFriends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('received');

  useEffect(() => {
    fetchConnections();
  }, [id]);

  const fetchConnections = async () => {
    try {
      const [sentRes, receivedRes, friendsRes] = await Promise.all([
        fetch(`/api/connections/sent/${id}`),
        fetch(`/api/connections/received/${id}`),
        fetch(`/api/connections/friends/${id}`)
      ]);

      if (!sentRes.ok || !receivedRes.ok || !friendsRes.ok) {
        throw new Error('Failed to fetch connections');
      }

      const [sentData, receivedData, friendsData] = await Promise.all([
        sentRes.json(),
        receivedRes.json(),
        friendsRes.json()
      ]);

      setSentConnections(sentData);
      setReceivedConnections(receivedData);
      setFriends(friendsData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleConnectionResponse = async (connectionId, status) => {
    try {
      const response = await fetch(`/api/connections/${connectionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status }),
      });

      if (!response.ok) throw new Error('Failed to update connection');

      fetchConnections();
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <div className="container">Loading connections...</div>;
  if (error) return <div className="container"><div className="error">{error}</div></div>;

  return (
    <div className="container">
      <h1>My Connections</h1>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', borderBottom: '2px solid #eee' }}>
        <button
          onClick={() => setActiveTab('received')}
          style={{
            padding: '1rem',
            border: 'none',
            background: 'none',
            cursor: 'pointer',
            fontWeight: activeTab === 'received' ? 'bold' : 'normal',
            borderBottom: activeTab === 'received' ? '2px solid #3498db' : 'none',
            marginBottom: '-2px'
          }}
        >
          Requests Received ({receivedConnections.filter(c => c.status === 'pending').length})
        </button>
        <button
          onClick={() => setActiveTab('sent')}
          style={{
            padding: '1rem',
            border: 'none',
            background: 'none',
            cursor: 'pointer',
            fontWeight: activeTab === 'sent' ? 'bold' : 'normal',
            borderBottom: activeTab === 'sent' ? '2px solid #3498db' : 'none',
            marginBottom: '-2px'
          }}
        >
          Requests Sent ({sentConnections.length})
        </button>
        <button
          onClick={() => setActiveTab('friends')}
          style={{
            padding: '1rem',
            border: 'none',
            background: 'none',
            cursor: 'pointer',
            fontWeight: activeTab === 'friends' ? 'bold' : 'normal',
            borderBottom: activeTab === 'friends' ? '2px solid #3498db' : 'none',
            marginBottom: '-2px'
          }}
        >
          Friends ({friends.length})
        </button>
      </div>

      {activeTab === 'received' && (
        <div>
          <h2>Connection Requests</h2>
          {receivedConnections.filter(c => c.status === 'pending').length === 0 ? (
            <div className="empty-state">
              <h3>No pending requests</h3>
              <p>When someone sends you a connection request, it will appear here</p>
            </div>
          ) : (
            <div className="connection-list">
              {receivedConnections
                .filter(c => c.status === 'pending')
                .map((connection) => (
                  <div key={connection.id} className="connection-card">
                    <div
                      className="connection-info"
                      style={{ cursor: 'pointer' }}
                      onClick={() => navigate(`/profile/${connection.sender.id}`)}
                    >
                      <h4>{connection.sender.name}</h4>
                      {connection.sender.city && (
                        <p className="location">{connection.sender.city}</p>
                      )}
                    </div>
                    <div className="button-group">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleConnectionResponse(connection.id, 'accepted');
                        }}
                        className="btn btn-success"
                      >
                        Accept
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleConnectionResponse(connection.id, 'declined');
                        }}
                        className="btn btn-danger"
                      >
                        Decline
                      </button>
                    </div>
                  </div>
                ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'sent' && (
        <div>
          <h2>Sent Requests</h2>
          {sentConnections.length === 0 ? (
            <div className="empty-state">
              <h3>No sent requests</h3>
              <p>Browse profiles and send connection requests to start making friends</p>
            </div>
          ) : (
            <div className="connection-list">
              {sentConnections.map((connection) => (
                <div key={connection.id} className="connection-card">
                  <div
                    className="connection-info"
                    style={{ cursor: 'pointer' }}
                    onClick={() => navigate(`/profile/${connection.receiver.id}`)}
                  >
                    <h4>{connection.receiver.name}</h4>
                    {connection.receiver.city && (
                      <p className="location">{connection.receiver.city}</p>
                    )}
                  </div>
                  <span className={`connection-status ${connection.status}`}>
                    {connection.status.charAt(0).toUpperCase() + connection.status.slice(1)}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'friends' && (
        <div>
          <h2>Your Friends</h2>
          {friends.length === 0 ? (
            <div className="empty-state">
              <h3>No friends yet</h3>
              <p>Accept connection requests to build your friend network</p>
            </div>
          ) : (
            <div className="profile-grid">
              {friends.map((friend) => (
                <div
                  key={friend.id}
                  className="profile-card"
                  onClick={() => navigate(`/profile/${friend.id}`)}
                >
                  <h3>{friend.name}</h3>
                  {friend.city && (
                    <p className="location">
                      {friend.city}{friend.neighborhood && `, ${friend.neighborhood}`}
                    </p>
                  )}
                  {friend.bio && <p className="bio">{friend.bio}</p>}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Connections;
