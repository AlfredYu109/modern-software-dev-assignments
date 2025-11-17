import { api } from '../api.js';
import { router } from '../router.js';

export async function renderEditProfile(profileId) {
    const app = document.getElementById('app');

    app.innerHTML = '<div class="container"><div class="loading">Loading profile...</div></div>';

    try {
        const profile = await api.getProfile(profileId);

        const interests = profile.interests ? profile.interests.map(i => i.tag) : [];
        const activities = profile.activities ? profile.activities.map(a => a.activity) : [];

        app.innerHTML = `
            <div class="container">
                <h1>Edit Profile</h1>

                <div id="error-message"></div>

                <form id="edit-profile-form">
                    <div class="form-group">
                        <label for="name">Name *</label>
                        <input type="text" id="name" name="name" value="${profile.name}" required>
                    </div>

                    <div class="form-group">
                        <label for="bio">Bio</label>
                        <textarea id="bio" name="bio" placeholder="Tell us about yourself...">${profile.bio || ''}</textarea>
                    </div>

                    <div class="form-group">
                        <label for="city">City</label>
                        <input type="text" id="city" name="city" value="${profile.city || ''}" placeholder="e.g., San Francisco">
                    </div>

                    <div class="form-group">
                        <label for="neighborhood">Neighborhood</label>
                        <input type="text" id="neighborhood" name="neighborhood" value="${profile.neighborhood || ''}" placeholder="e.g., Mission District">
                    </div>

                    <div class="form-group">
                        <label>Interests</label>
                        <div class="tag-input-container">
                            <input type="text" id="interest-input" placeholder="e.g., hiking, cooking, photography">
                            <button type="button" id="add-interest" class="btn btn-secondary">Add</button>
                        </div>
                        <div id="interests-list" class="tags-list"></div>
                    </div>

                    <div class="form-group">
                        <label>Preferred Activities</label>
                        <div class="tag-input-container">
                            <input type="text" id="activity-input" placeholder="e.g., coffee, movies, sports">
                            <button type="button" id="add-activity" class="btn btn-secondary">Add</button>
                        </div>
                        <div id="activities-list" class="tags-list"></div>
                    </div>

                    <div class="form-group">
                        <label>Availability</label>
                        <div class="checkbox-group">
                            <label>
                                <input type="checkbox" name="availability" value="weekday" ${profile.availability?.includes('weekday') ? 'checked' : ''}>
                                Weekdays
                            </label>
                            <label>
                                <input type="checkbox" name="availability" value="weekend" ${profile.availability?.includes('weekend') ? 'checked' : ''}>
                                Weekends
                            </label>
                        </div>
                    </div>

                    <div class="button-group">
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                        <button type="button" id="cancel-edit" class="btn btn-secondary">Cancel</button>
                    </div>
                </form>
            </div>
        `;

        function renderTags() {
            document.getElementById('interests-list').innerHTML = interests.map(tag => `
                <div class="tag">
                    ${tag}
                    <button type="button" data-interest="${tag}">×</button>
                </div>
            `).join('');

            document.getElementById('activities-list').innerHTML = activities.map(tag => `
                <div class="tag">
                    ${tag}
                    <button type="button" data-activity="${tag}">×</button>
                </div>
            `).join('');

            document.querySelectorAll('[data-interest]').forEach(btn => {
                btn.addEventListener('click', () => {
                    const tag = btn.getAttribute('data-interest');
                    const index = interests.indexOf(tag);
                    if (index > -1) {
                        interests.splice(index, 1);
                        renderTags();
                    }
                });
            });

            document.querySelectorAll('[data-activity]').forEach(btn => {
                btn.addEventListener('click', () => {
                    const tag = btn.getAttribute('data-activity');
                    const index = activities.indexOf(tag);
                    if (index > -1) {
                        activities.splice(index, 1);
                        renderTags();
                    }
                });
            });
        }

        renderTags();

        document.getElementById('add-interest').addEventListener('click', () => {
            const input = document.getElementById('interest-input');
            const value = input.value.trim();
            if (value && !interests.includes(value)) {
                interests.push(value);
                input.value = '';
                renderTags();
            }
        });

        document.getElementById('interest-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('add-interest').click();
            }
        });

        document.getElementById('add-activity').addEventListener('click', () => {
            const input = document.getElementById('activity-input');
            const value = input.value.trim();
            if (value && !activities.includes(value)) {
                activities.push(value);
                input.value = '';
                renderTags();
            }
        });

        document.getElementById('activity-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('add-activity').click();
            }
        });

        document.getElementById('cancel-edit').addEventListener('click', () => {
            router.navigate(`profile/${profileId}`);
        });

        document.getElementById('edit-profile-form').addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(e.target);
            const availability = formData.getAll('availability');

            const data = {
                name: formData.get('name'),
                bio: formData.get('bio'),
                city: formData.get('city'),
                neighborhood: formData.get('neighborhood'),
                interests,
                activities,
                availability
            };

            try {
                await api.updateProfile(profileId, data);
                router.navigate(`profile/${profileId}`);
            } catch (error) {
                document.getElementById('error-message').innerHTML = `
                    <div class="error">${error.message}</div>
                `;
            }
        });
    } catch (error) {
        app.innerHTML = `<div class="container"><div class="error">${error.message}</div></div>`;
    }
}
