import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css';
import CreateProfile from './components/CreateProfile';
import ProfileList from './components/ProfileList';
import ProfileDetail from './components/ProfileDetail';
import EditProfile from './components/EditProfile';
import Matches from './components/Matches';
import Connections from './components/Connections';

function App() {
  const [currentProfileId, setCurrentProfileId] = useState(
    localStorage.getItem('currentProfileId') || null
  );

  const handleProfileCreated = (profileId) => {
    setCurrentProfileId(profileId);
    localStorage.setItem('currentProfileId', profileId);
  };

  const handleLogout = () => {
    setCurrentProfileId(null);
    localStorage.removeItem('currentProfileId');
  };

  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-container">
            <Link to="/" className="nav-brand">
              Friend Finder Lite
            </Link>
            <div className="nav-links">
              {currentProfileId ? (
                <>
                  <Link to="/profiles">Browse</Link>
                  <Link to={`/profiles/${currentProfileId}/matches`}>Matches</Link>
                  <Link to={`/profiles/${currentProfileId}/connections`}>Connections</Link>
                  <Link to={`/profiles/${currentProfileId}`}>My Profile</Link>
                  <button onClick={handleLogout} className="logout-btn">
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link to="/profiles">Browse Profiles</Link>
                  <Link to="/create">Create Profile</Link>
                </>
              )}
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route
              path="/"
              element={
                currentProfileId ? (
                  <Navigate to={`/profiles/${currentProfileId}`} />
                ) : (
                  <div className="welcome">
                    <h1>Welcome to Friend Finder Lite</h1>
                    <p>Connect with recent grads in your city</p>
                    <div className="welcome-actions">
                      <Link to="/create" className="btn btn-primary">
                        Create Your Profile
                      </Link>
                      <Link to="/profiles" className="btn btn-secondary">
                        Browse Profiles
                      </Link>
                    </div>
                  </div>
                )
              }
            />
            <Route
              path="/create"
              element={<CreateProfile onProfileCreated={handleProfileCreated} />}
            />
            <Route path="/profiles" element={<ProfileList />} />
            <Route path="/profiles/:id" element={<ProfileDetail currentProfileId={currentProfileId} />} />
            <Route
              path="/profiles/:id/edit"
              element={<EditProfile />}
            />
            <Route
              path="/profiles/:id/matches"
              element={<Matches currentProfileId={currentProfileId} />}
            />
            <Route
              path="/profiles/:id/connections"
              element={<Connections currentProfileId={currentProfileId} />}
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
