import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Home from './components/Home';
import CreateProfile from './components/CreateProfile';
import ProfileDetail from './components/ProfileDetail';
import EditProfile from './components/EditProfile';
import Browse from './components/Browse';
import Matches from './components/Matches';
import Connections from './components/Connections';

function App() {
  const [currentProfile, setCurrentProfile] = useState(null);

  useEffect(() => {
    const savedProfileId = localStorage.getItem('currentProfileId');
    if (savedProfileId) {
      setCurrentProfile({ id: savedProfileId });
    }
  }, []);

  const handleProfileCreated = (profile) => {
    setCurrentProfile(profile);
    localStorage.setItem('currentProfileId', profile.id);
  };

  const handleProfileDeleted = () => {
    setCurrentProfile(null);
    localStorage.removeItem('currentProfileId');
  };

  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-container">
            <Link to="/" className="nav-brand">Friend Finder Lite</Link>
            <div className="nav-links">
              <Link to="/">Home</Link>
              <Link to="/browse">Browse</Link>
              {currentProfile && (
                <>
                  <Link to={`/matches/${currentProfile.id}`}>Matches</Link>
                  <Link to={`/connections/${currentProfile.id}`}>Connections</Link>
                  <Link to={`/profile/${currentProfile.id}`}>My Profile</Link>
                </>
              )}
              {!currentProfile && <Link to="/create">Create Profile</Link>}
            </div>
          </div>
        </nav>

        <div className="main-content">
          <Routes>
            <Route path="/" element={<Home currentProfile={currentProfile} />} />
            <Route path="/create" element={<CreateProfile onProfileCreated={handleProfileCreated} />} />
            <Route path="/profile/:id" element={<ProfileDetail onProfileDeleted={handleProfileDeleted} />} />
            <Route path="/edit/:id" element={<EditProfile />} />
            <Route path="/browse" element={<Browse />} />
            <Route path="/matches/:id" element={<Matches />} />
            <Route path="/connections/:id" element={<Connections />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
