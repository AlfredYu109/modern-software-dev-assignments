import React from 'react';
import { Link } from 'react-router-dom';

function Home({ currentProfile }) {
  return (
    <div className="container">
      <h1>Welcome to Friend Finder Lite</h1>
      <p style={{ marginTop: '1rem', fontSize: '1.1rem', lineHeight: '1.6' }}>
        Connect with recent college graduates in your city and make new friends based on shared interests.
      </p>

      <div style={{ marginTop: '2rem' }}>
        {!currentProfile ? (
          <div>
            <h2>Get Started</h2>
            <p style={{ margin: '1rem 0' }}>
              Create your profile to start browsing and connecting with potential friends.
            </p>
            <Link to="/create" className="btn btn-primary">
              Create Profile
            </Link>
          </div>
        ) : (
          <div>
            <h2>What would you like to do?</h2>
            <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem', flexWrap: 'wrap' }}>
              <Link to="/browse" className="btn btn-primary">
                Browse Profiles
              </Link>
              <Link to={`/matches/${currentProfile.id}`} className="btn btn-primary">
                View Matches
              </Link>
              <Link to={`/connections/${currentProfile.id}`} className="btn btn-primary">
                My Connections
              </Link>
              <Link to={`/profile/${currentProfile.id}`} className="btn btn-secondary">
                View My Profile
              </Link>
            </div>
          </div>
        )}
      </div>

      <div style={{ marginTop: '3rem', padding: '2rem', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
        <h2>How It Works</h2>
        <ol style={{ marginTop: '1rem', lineHeight: '2' }}>
          <li>Create your profile with interests and activities you enjoy</li>
          <li>Browse other profiles or view your personalized matches</li>
          <li>Send connection requests to people you'd like to meet</li>
          <li>Connect with friends and start building your network</li>
        </ol>
      </div>
    </div>
  );
}

export default Home;
