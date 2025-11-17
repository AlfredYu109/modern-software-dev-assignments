const API_BASE = 'http://localhost:5000/api';

let currentProfileId = null;

function showView(viewName) {
    document.querySelectorAll('.view').forEach(view => {
        view.style.display = 'none';
    });
    document.getElementById(`${viewName}-view`).style.display = 'block';

    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-view="${viewName}"]`).classList.add('active');

    switch(viewName) {
        case 'browse':
            loadProfiles();
            break;
        case 'matches':
            loadMatches();
            break;
        case 'connections':
            loadConnections();
            break;
        case 'profile':
            break;
    }
}

async function loadProfile() {
    if (!currentProfileId) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/profiles/${currentProfileId}`);
        if (response.ok) {
            const profile = await response.json();
            document.getElementById('name').value = profile.name || '';
            document.getElementById('bio').value = profile.bio || '';
            document.getElementById('city').value = profile.city || '';
            document.getElementById('interests').value = profile.interests || '';
            document.getElementById('activities').value = profile.activities || '';
            document.getElementById('availability').value = profile.availability || '';
            document.getElementById('delete-profile-btn').style.display = 'inline-block';
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

async function saveProfile(event) {
    event.preventDefault();

    const formData = {
        name: document.getElementById('name').value,
        bio: document.getElementById('bio').value,
        city: document.getElementById('city').value,
        interests: document.getElementById('interests').value.split(',').map(i => i.trim()).filter(i => i),
        activities: document.getElementById('activities').value.split(',').map(a => a.trim()).filter(a => a),
        availability: document.getElementById('availability').value
    };

    try {
        let response;
        if (currentProfileId) {
            response = await fetch(`${API_BASE}/profiles/${currentProfileId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
        } else {
            response = await fetch(`${API_BASE}/profiles`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
        }

        if (response.ok) {
            const result = await response.json();
            if (!currentProfileId && result.id) {
                currentProfileId = result.id;
                localStorage.setItem('currentProfileId', currentProfileId);
            }
            alert('Profile saved successfully!');
            document.getElementById('delete-profile-btn').style.display = 'inline-block';
        } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);
        }
    } catch (error) {
        console.error('Error saving profile:', error);
        alert('Error saving profile');
    }
}

async function deleteProfile() {
    if (!currentProfileId) {
        alert('No profile to delete');
        return;
    }

    if (!confirm('Are you sure you want to delete your profile? This cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/profiles/${currentProfileId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('Profile deleted successfully');
            currentProfileId = null;
            localStorage.removeItem('currentProfileId');
            document.getElementById('profile-form').reset();
            document.getElementById('delete-profile-btn').style.display = 'none';
        }
    } catch (error) {
        console.error('Error deleting profile:', error);
        alert('Error deleting profile');
    }
}

async function loadProfiles(filters = {}) {
    try {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE}/profiles?${params}`);
        const profiles = await response.json();

        const profilesList = document.getElementById('profiles-list');

        if (profiles.length === 0) {
            profilesList.innerHTML = '<p class="no-results">No profiles found</p>';
            return;
        }

        profilesList.innerHTML = profiles
            .filter(p => p.id !== currentProfileId)
            .map(profile => `
                <div class="profile-card" onclick="showProfileDetail(${profile.id})">
                    <h3>${profile.name}</h3>
                    <p class="profile-city">${profile.city || 'Location not specified'}</p>
                    <p class="profile-bio">${profile.bio || 'No bio provided'}</p>
                    <div class="profile-tags">
                        ${profile.interests ? profile.interests.split(',').map(i =>
                            `<span class="tag tag-interest">${i.trim()}</span>`
                        ).join('') : ''}
                        ${profile.activities ? profile.activities.split(',').map(a =>
                            `<span class="tag tag-activity">${a.trim()}</span>`
                        ).join('') : ''}
                    </div>
                    <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); sendConnectionRequest(${profile.id})">
                        Connect
                    </button>
                </div>
            `).join('');
    } catch (error) {
        console.error('Error loading profiles:', error);
    }
}

async function loadMatches() {
    if (!currentProfileId) {
        document.getElementById('matches-list').innerHTML = '<p class="hint">Please create your profile first to see matches</p>';
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/matches/${currentProfileId}`);
        const matches = await response.json();

        const matchesList = document.getElementById('matches-list');

        if (matches.error) {
            matchesList.innerHTML = `<p class="hint">${matches.error}</p>`;
            return;
        }

        if (matches.length === 0) {
            matchesList.innerHTML = '<p class="no-results">No matches found. Try updating your interests!</p>';
            return;
        }

        matchesList.innerHTML = matches.map(match => `
            <div class="profile-card match-card" onclick="showProfileDetail(${match.id})">
                <div class="match-score">Match Score: ${match.match_score}</div>
                <h3>${match.name}</h3>
                <p class="profile-city">${match.city || 'Location not specified'}</p>
                <p class="profile-bio">${match.bio || 'No bio provided'}</p>
                <div class="shared-section">
                    ${match.shared_interests && match.shared_interests.length > 0 ? `
                        <p><strong>Shared Interests:</strong></p>
                        <div class="profile-tags">
                            ${match.shared_interests.map(i => `<span class="tag tag-interest">${i}</span>`).join('')}
                        </div>
                    ` : ''}
                    ${match.shared_activities && match.shared_activities.length > 0 ? `
                        <p><strong>Shared Activities:</strong></p>
                        <div class="profile-tags">
                            ${match.shared_activities.map(a => `<span class="tag tag-activity">${a}</span>`).join('')}
                        </div>
                    ` : ''}
                </div>
                <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); sendConnectionRequest(${match.id})">
                    Connect
                </button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading matches:', error);
    }
}

async function loadConnections() {
    if (!currentProfileId) {
        document.getElementById('incoming-requests').innerHTML = '<p class="hint">Please create your profile first</p>';
        document.getElementById('friends-list').innerHTML = '';
        return;
    }

    try {
        const incomingResponse = await fetch(`${API_BASE}/connections/${currentProfileId}/incoming`);
        const incoming = await incomingResponse.json();

        const incomingContainer = document.getElementById('incoming-requests');
        if (incoming.length === 0) {
            incomingContainer.innerHTML = '<p class="no-results">No incoming requests</p>';
        } else {
            incomingContainer.innerHTML = incoming.map(conn => `
                <div class="connection-card">
                    <h4>${conn.name}</h4>
                    <p>${conn.bio || 'No bio'}</p>
                    <div class="profile-tags">
                        ${conn.interests ? conn.interests.split(',').map(i =>
                            `<span class="tag tag-interest">${i.trim()}</span>`
                        ).join('') : ''}
                    </div>
                    <div class="connection-actions">
                        <button class="btn btn-primary btn-sm" onclick="acceptConnection(${conn.id})">Accept</button>
                        <button class="btn btn-danger btn-sm" onclick="declineConnection(${conn.id})">Decline</button>
                    </div>
                </div>
            `).join('');
        }

        const friendsResponse = await fetch(`${API_BASE}/connections/${currentProfileId}/friends`);
        const friends = await friendsResponse.json();

        const friendsContainer = document.getElementById('friends-list');
        if (friends.length === 0) {
            friendsContainer.innerHTML = '<p class="no-results">No friends yet</p>';
        } else {
            friendsContainer.innerHTML = friends.map(friend => `
                <div class="profile-card" onclick="showProfileDetail(${friend.id})">
                    <h3>${friend.name}</h3>
                    <p class="profile-city">${friend.city || 'Location not specified'}</p>
                    <p class="profile-bio">${friend.bio || 'No bio'}</p>
                    <div class="profile-tags">
                        ${friend.interests ? friend.interests.split(',').map(i =>
                            `<span class="tag tag-interest">${i.trim()}</span>`
                        ).join('') : ''}
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading connections:', error);
    }
}

async function sendConnectionRequest(receiverId) {
    if (!currentProfileId) {
        alert('Please create your profile first');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/connections`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sender_id: currentProfileId,
                receiver_id: receiverId
            })
        });

        if (response.ok) {
            alert('Connection request sent!');
        } else {
            const error = await response.json();
            alert(error.error || 'Error sending connection request');
        }
    } catch (error) {
        console.error('Error sending connection request:', error);
        alert('Error sending connection request');
    }
}

async function acceptConnection(connectionId) {
    try {
        const response = await fetch(`${API_BASE}/connections/${connectionId}/accept`, {
            method: 'PUT'
        });

        if (response.ok) {
            alert('Connection accepted!');
            loadConnections();
        }
    } catch (error) {
        console.error('Error accepting connection:', error);
    }
}

async function declineConnection(connectionId) {
    try {
        const response = await fetch(`${API_BASE}/connections/${connectionId}/decline`, {
            method: 'PUT'
        });

        if (response.ok) {
            alert('Connection declined');
            loadConnections();
        }
    } catch (error) {
        console.error('Error declining connection:', error);
    }
}

async function showProfileDetail(profileId) {
    try {
        const response = await fetch(`${API_BASE}/profiles/${profileId}`);
        const profile = await response.json();

        const detailContainer = document.getElementById('profile-detail');
        detailContainer.innerHTML = `
            <h2>${profile.name}</h2>
            <p><strong>City:</strong> ${profile.city || 'Not specified'}</p>
            <p><strong>Bio:</strong> ${profile.bio || 'No bio provided'}</p>
            <p><strong>Availability:</strong> ${profile.availability || 'Not specified'}</p>

            ${profile.interests ? `
                <div class="detail-section">
                    <strong>Interests:</strong>
                    <div class="profile-tags">
                        ${profile.interests.split(',').map(i =>
                            `<span class="tag tag-interest">${i.trim()}</span>`
                        ).join('')}
                    </div>
                </div>
            ` : ''}

            ${profile.activities ? `
                <div class="detail-section">
                    <strong>Activities:</strong>
                    <div class="profile-tags">
                        ${profile.activities.split(',').map(a =>
                            `<span class="tag tag-activity">${a.trim()}</span>`
                        ).join('')}
                    </div>
                </div>
            ` : ''}

            ${currentProfileId && profileId !== currentProfileId ? `
                <button class="btn btn-primary" onclick="sendConnectionRequest(${profileId}); closeModal();">
                    Send Connection Request
                </button>
            ` : ''}
        `;

        document.getElementById('profile-detail-modal').style.display = 'block';
    } catch (error) {
        console.error('Error loading profile detail:', error);
    }
}

function closeModal() {
    document.getElementById('profile-detail-modal').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    currentProfileId = localStorage.getItem('currentProfileId');
    if (currentProfileId) {
        currentProfileId = parseInt(currentProfileId);
        loadProfile();
    }

    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            showView(e.target.dataset.view);
        });
    });

    document.getElementById('profile-form').addEventListener('submit', saveProfile);
    document.getElementById('delete-profile-btn').addEventListener('click', deleteProfile);

    document.getElementById('apply-filters').addEventListener('click', () => {
        const filters = {};
        const city = document.getElementById('filter-city').value;
        const interest = document.getElementById('filter-interest').value;

        if (city) filters.city = city;
        if (interest) filters.interest = interest;

        loadProfiles(filters);
    });

    document.getElementById('clear-filters').addEventListener('click', () => {
        document.getElementById('filter-city').value = '';
        document.getElementById('filter-interest').value = '';
        loadProfiles();
    });

    document.querySelector('.close').addEventListener('click', closeModal);

    window.addEventListener('click', (event) => {
        if (event.target === document.getElementById('profile-detail-modal')) {
            closeModal();
        }
    });

    showView('browse');
});
