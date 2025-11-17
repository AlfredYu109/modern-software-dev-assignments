import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';

function ProfileDetail({ currentProfileId }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [connectionStatus, setConnectionStatus] = useState(null);
  const [sendingRequest, setSendingRequest] = useState(false);

  const isOwnProfile = currentProfileId === id;

  useEffect(() => {
    fetchProfile();
    if (!isOwnProfile && currentProfileId) {
      checkConnectionStatus();
    }
  }, [id]);

  const fetchProfile = async () => {
    try {
      const response = await fetch(`/api/profiles/${id}`);
      if (!response.ok) {
        throw new Error('Profile not found');
      }
      const data = await response.json();
      setProfile(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const checkConnectionStatus = async () => {
    try {
      const response = await fetch(`/api/profiles/${currentProfileId}/connections`);
      const connections = await response.json();

      const existingConnection = connections.find(
        conn =>
          (conn.sender_id === id && conn.receiver_id === currentProfileId) ||
          (conn.sender_id === currentProfileId && conn.receiver_id === id)
      );

      if (existingConnection) {
        setConnectionStatus(existingConnection.status);
      }
    } catch (error) {
      console.error('Error checking connection status:', error);
    }
  };

  const sendConnectionRequest = async () => {
    if (!currentProfileId) {
      alert('Please create a profile first to send connection requests');
      return;
    }

    setSendingRequest(true);
    try {
      const response = await fetch('/api/connections', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          sender_id: currentProfileId,
          receiver_id: id
        })
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error);
      }

      setConnectionStatus('pending');
      alert('Connection request sent!');
    } catch (error) {
      alert(error.message);
    } finally {
      setSendingRequest(false);
    }
  };

  const deleteProfile = async () => {
    if (!window.confirm('Are you sure you want to delete your profile? This cannot be undone.')) {
      return;
    }

    try {
      const response = await fetch(`/api/profiles/${id}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        throw new Error('Failed to delete profile');
      }

      localStorage.removeItem('currentProfileId');
      alert('Profile deleted successfully');
      navigate('/');
    } catch (error) {
      alert(error.message);
    }
  };

  if (loading) {
    return <div className="loading">Loading profile...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <h3>Error</h3>
        <p>{error}</p>
        <Link to="/profiles" className="btn btn-primary">
          Back to Profiles
        </Link>
      </div>
    );
  }

  if (!profile) {
    return <div className="error">Profile not found</div>;
  }

  return (
    <div className="profile-detail">
      <div className="profile-header">
        <h2>{profile.name}</h2>
        {(profile.city || profile.neighborhood) && (
          <p className="location">
            {profile.city}
            {profile.city && profile.neighborhood && ', '}
            {profile.neighborhood}
          </p>
        )}
      </div>

      <div className="profile-section">
        <h3>About</h3>
        <p>{profile.bio || 'No bio provided'}</p>
      </div>

      {profile.interests && profile.interests.length > 0 && (
        <div className="profile-section">
          <h3>Interests</h3>
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
        <div className="profile-section">
          <h3>Preferred Activities</h3>
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
        <div className="profile-section">
          <h3>Availability</h3>
          <p>{profile.availability}</p>
        </div>
      )}

      <div className="profile-actions">
        {isOwnProfile ? (
          <>
            <Link
              to={`/profiles/${id}/edit`}
              className="btn btn-primary"
            >
              Edit Profile
            </Link>
            <button
              onClick={deleteProfile}
              className="btn btn-danger"
            >
              Delete Profile
            </button>
          </>
        ) : (
          <>
            {!connectionStatus && (
              <button
                onClick={sendConnectionRequest}
                className="btn btn-primary"
                disabled={sendingRequest}
              >
                {sendingRequest ? 'Sending...' : 'Send Connection Request'}
              </button>
            )}
            {connectionStatus === 'pending' && (
              <span className="status pending">Request Pending</span>
            )}
            {connectionStatus === 'accepted' && (
              <span className="status accepted">Connected</span>
            )}
            {connectionStatus === 'declined' && (
              <span className="status declined">Request Declined</span>
            )}
          </>
        )}
        <Link to="/profiles" className="btn btn-secondary">
          Back to Profiles
        </Link>
      </div>
    </div>
  );
}

export default ProfileDetail;
