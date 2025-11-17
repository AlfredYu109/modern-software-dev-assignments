import { api } from '../api.js';

export async function renderMatches(profileId) {
    const app = document.getElementById('app');

    app.innerHTML = `
        <div class="container">
            <h1>Your Matches</h1>
            <p style="margin-bottom: 1.5rem; color: #666;">
                Profiles sorted by shared interests and activities
            </p>
            <div id="matches-container" class="loading">Finding your matches...</div>
        </div>
    `;

    try {
        const matches = await api.getMatches(profileId);
        const container = document.getElementById('matches-container');

        if (matches.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>No matches found yet</h3>
                    <p>Add more interests to your profile or check back later as more people join!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="profile-grid">
                ${matches.map(profile => `
                    <div class="profile-card" data-profile-id="${profile.id}">
                        <h3>
                            ${profile.name}
                            <span class="match-score">${profile.match_score} matches</span>
                        </h3>
                        ${profile.city ? `
                            <p class="location">${profile.city}${profile.neighborhood ? `, ${profile.neighborhood}` : ''}</p>
                        ` : ''}
                        ${profile.bio ? `<p class="bio">${profile.bio}</p>` : ''}

                        ${profile.shared_interests && profile.shared_interests.length > 0 ? `
                            <div style="margin-top: 1rem;">
                                <strong style="font-size: 0.9rem; color: #666;">Shared Interests:</strong>
                                <div class="tags-list">
                                    ${profile.shared_interests.map(interest => `
                                        <div class="tag">${interest}</div>
                                    `).join('')}
                                </div>
                            </div>
                        ` : ''}

                        ${profile.shared_activities && profile.shared_activities.length > 0 ? `
                            <div style="margin-top: 1rem;">
                                <strong style="font-size: 0.9rem; color: #666;">Shared Activities:</strong>
                                <div class="tags-list">
                                    ${profile.shared_activities.map(activity => `
                                        <div class="tag">${activity}</div>
                                    `).join('')}
                                </div>
                            </div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>
        `;

        document.querySelectorAll('.profile-card').forEach(card => {
            card.addEventListener('click', () => {
                const id = card.getAttribute('data-profile-id');
                window.location.hash = `profile/${id}`;
            });
        });
    } catch (error) {
        document.getElementById('matches-container').innerHTML = `
            <div class="error">${error.message}</div>
        `;
    }
}
