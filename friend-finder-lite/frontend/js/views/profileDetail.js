import { api } from '../api.js';
import { state } from '../state.js';
import { router } from '../router.js';

export async function renderProfileDetail(profileId) {
    const app = document.getElementById('app');

    app.innerHTML = '<div class="container"><div class="loading">Loading profile...</div></div>';

    try {
        const profile = await api.getProfile(profileId);
        const isOwnProfile = state.currentProfileId === profileId;

        app.innerHTML = `
            <div class="container">
                <div class="profile-header">
                    <h1>${profile.name}</h1>
                    ${profile.city ? `
                        <p class="location">${profile.city}${profile.neighborhood ? `, ${profile.neighborhood}` : ''}</p>
                    ` : ''}
                </div>

                ${profile.bio ? `
                    <div class="profile-section">
                        <h3>About</h3>
                        <p>${profile.bio}</p>
                    </div>
                ` : ''}

                ${profile.interests && profile.interests.length > 0 ? `
                    <div class="profile-section">
                        <h3>Interests</h3>
                        <div class="tags-list">
                            ${profile.interests.map(i => `<div class="tag">${i.tag}</div>`).join('')}
                        </div>
                    </div>
                ` : ''}

                ${profile.activities && profile.activities.length > 0 ? `
                    <div class="profile-section">
                        <h3>Preferred Activities</h3>
                        <div class="tags-list">
                            ${profile.activities.map(a => `<div class="tag">${a.activity}</div>`).join('')}
                        </div>
                    </div>
                ` : ''}

                ${profile.availability && profile.availability.length > 0 ? `
                    <div class="profile-section">
                        <h3>Availability</h3>
                        <div class="tags-list">
                            ${profile.availability.map(avail => `<div class="tag">${avail}</div>`).join('')}
                        </div>
                    </div>
                ` : ''}

                <div class="button-group">
                    ${isOwnProfile ? `
                        <a href="#edit/${profileId}" class="btn btn-primary">Edit Profile</a>
                        <button id="delete-profile" class="btn btn-danger">Delete Profile</button>
                    ` : state.currentProfileId ? `
                        <button id="send-connection" class="btn btn-primary">Send Connection Request</button>
                    ` : ''}
                </div>
            </div>
        `;

        if (isOwnProfile) {
            document.getElementById('delete-profile').addEventListener('click', async () => {
                if (confirm('Are you sure you want to delete your profile?')) {
                    try {
                        await api.deleteProfile(profileId);
                        state.clearCurrentProfile();
                        router.navigate('home');
                    } catch (error) {
                        alert(error.message);
                    }
                }
            });
        } else if (state.currentProfileId) {
            document.getElementById('send-connection').addEventListener('click', async () => {
                try {
                    await api.createConnection(state.currentProfileId, profileId);
                    alert('Connection request sent!');
                } catch (error) {
                    alert(error.message);
                }
            });
        }
    } catch (error) {
        app.innerHTML = `<div class="container"><div class="error">${error.message}</div></div>`;
    }
}
