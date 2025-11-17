import { api } from '../api.js';

export async function renderBrowse() {
    const app = document.getElementById('app');

    app.innerHTML = `
        <div class="filters">
            <h3>Filter Profiles</h3>
            <form id="filter-form">
                <div class="filter-row">
                    <div class="form-group">
                        <label for="filter-city">City</label>
                        <input type="text" id="filter-city" placeholder="e.g., San Francisco">
                    </div>
                    <div class="form-group">
                        <label for="filter-neighborhood">Neighborhood</label>
                        <input type="text" id="filter-neighborhood" placeholder="e.g., Mission District">
                    </div>
                    <div class="form-group">
                        <label for="filter-interest">Interest</label>
                        <input type="text" id="filter-interest" placeholder="e.g., hiking">
                    </div>
                    <div class="form-group">
                        <label for="filter-activity">Activity</label>
                        <input type="text" id="filter-activity" placeholder="e.g., coffee">
                    </div>
                    <div class="form-group">
                        <label for="filter-availability">Availability</label>
                        <select id="filter-availability">
                            <option value="">All</option>
                            <option value="weekday">Weekdays</option>
                            <option value="weekend">Weekends</option>
                        </select>
                    </div>
                </div>
                <div class="button-group">
                    <button type="submit" class="btn btn-primary">Apply Filters</button>
                    <button type="button" id="clear-filters" class="btn btn-secondary">Clear</button>
                </div>
            </form>
        </div>

        <div class="container">
            <h1>Browse Profiles</h1>
            <div id="profiles-container" class="loading">Loading profiles...</div>
        </div>
    `;

    async function loadProfiles(filters = {}) {
        const container = document.getElementById('profiles-container');
        container.innerHTML = '<div class="loading">Loading profiles...</div>';

        try {
            const profiles = await api.getProfiles(filters);

            if (profiles.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <h3>No profiles found</h3>
                        <p>Try adjusting your filters or check back later</p>
                    </div>
                `;
                return;
            }

            container.innerHTML = `
                <div class="profile-grid">
                    ${profiles.map(profile => `
                        <div class="profile-card" data-profile-id="${profile.id}">
                            <h3>${profile.name}</h3>
                            ${profile.city ? `
                                <p class="location">${profile.city}${profile.neighborhood ? `, ${profile.neighborhood}` : ''}</p>
                            ` : ''}
                            ${profile.bio ? `<p class="bio">${profile.bio}</p>` : ''}
                            ${profile.interests && profile.interests.length > 0 ? `
                                <div class="tags-list">
                                    ${profile.interests.slice(0, 3).map(i => `
                                        <div class="tag">${i.tag}</div>
                                    `).join('')}
                                    ${profile.interests.length > 3 ? `
                                        <div class="tag">+${profile.interests.length - 3} more</div>
                                    ` : ''}
                                </div>
                            ` : ''}
                        </div>
                    `).join('')}
                </div>
            `;

            document.querySelectorAll('.profile-card').forEach(card => {
                card.addEventListener('click', () => {
                    const profileId = card.getAttribute('data-profile-id');
                    window.location.hash = `profile/${profileId}`;
                });
            });
        } catch (error) {
            container.innerHTML = `<div class="error">${error.message}</div>`;
        }
    }

    document.getElementById('filter-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const filters = {};
        const city = document.getElementById('filter-city').value;
        const neighborhood = document.getElementById('filter-neighborhood').value;
        const interest = document.getElementById('filter-interest').value;
        const activity = document.getElementById('filter-activity').value;
        const availability = document.getElementById('filter-availability').value;

        if (city) filters.city = city;
        if (neighborhood) filters.neighborhood = neighborhood;
        if (interest) filters.interest = interest;
        if (activity) filters.activity = activity;
        if (availability) filters.availability = availability;

        loadProfiles(filters);
    });

    document.getElementById('clear-filters').addEventListener('click', () => {
        document.getElementById('filter-form').reset();
        loadProfiles();
    });

    loadProfiles();
}
