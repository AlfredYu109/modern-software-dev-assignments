import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';

function ProfileDetail({ onProfileDeleted }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const currentProfileId = localStorage.getItem('currentProfileId');
  const isOwnProfile = currentProfileId === id;

  useEffect(() => {
    fetchProfile();
  }, [id]);

  const fetchProfile = async () => {
    try {
      const response = await fetch(`/api/profiles/${id}`);
      if (!response.ok) throw new Error('Profile not found');
      const data = await response.json();
      setProfile(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete your profile?')) return;

    try {
      const response = await fetch(`/api/profiles/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to delete profile');

      onProfileDeleted();
      navigate('/');
    } catch (err) {
      setError(err.message);
    }
  };

  const handleSendConnection = async () => {
    try {
      const response = await fetch('/api/connections', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sender_id: currentProfileId,
          receiver_id: id,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to send connection request');
      }

      alert('Connection request sent!');
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <div className="container">Loading...</div>;
  if (error) return <div className="container"><div className="error">{error}</div></div>;
  if (!profile) return <div className="container">Profile not found</div>;

  return (
    <div className="container profile-detail">
      <div className="profile-header">
        <h1>{profile.name}</h1>
        {profile.city && <p className="location">{profile.city}{profile.neighborhood && `, ${profile.neighborhood}`}</p>}
      </div>

      {profile.bio && (
        <div className="profile-section">
          <h3>About</h3>
          <p>{profile.bio}</p>
        </div>
      )}

      {profile.interests && profile.interests.length > 0 && (
        <div className="profile-section">
          <h3>Interests</h3>
          <div className="tags-list">
            {profile.interests.map((item) => (
              <div key={item.tag} className="tag">{item.tag}</div>
            ))}
          </div>
        </div>
      )}

      {profile.activities && profile.activities.length > 0 && (
        <div className="profile-section">
          <h3>Preferred Activities</h3>
          <div className="tags-list">
            {profile.activities.map((item) => (
              <div key={item.activity} className="tag">{item.activity}</div>
            ))}
          </div>
        </div>
      )}

      {profile.availability && profile.availability.length > 0 && (
        <div className="profile-section">
          <h3>Availability</h3>
          <div className="tags-list">
            {profile.availability.map((avail) => (
              <div key={avail} className="tag">{avail}</div>
            ))}
          </div>
        </div>
      )}

      <div className="button-group">
        {isOwnProfile ? (
          <>
            <Link to={`/edit/${id}`} className="btn btn-primary">
              Edit Profile
            </Link>
            <button onClick={handleDelete} className="btn btn-danger">
              Delete Profile
            </button>
          </>
        ) : currentProfileId && (
          <button onClick={handleSendConnection} className="btn btn-primary">
            Send Connection Request
          </button>
        )}
      </div>
    </div>
  );
}

export default ProfileDetail;
