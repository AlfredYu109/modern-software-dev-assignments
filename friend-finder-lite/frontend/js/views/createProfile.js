import { api } from '../api.js';
import { state } from '../state.js';
import { router } from '../router.js';

export function renderCreateProfile() {
    const app = document.getElementById('app');

    const interests = [];
    const activities = [];

    app.innerHTML = `
        <div class="container">
            <h1>Create Your Profile</h1>

            <div id="error-message"></div>

            <form id="create-profile-form">
                <div class="form-group">
                    <label for="name">Name *</label>
                    <input type="text" id="name" name="name" required>
                </div>

                <div class="form-group">
                    <label for="bio">Bio</label>
                    <textarea id="bio" name="bio" placeholder="Tell us about yourself..."></textarea>
                </div>

                <div class="form-group">
                    <label for="city">City</label>
                    <input type="text" id="city" name="city" placeholder="e.g., San Francisco">
                </div>

                <div class="form-group">
                    <label for="neighborhood">Neighborhood</label>
                    <input type="text" id="neighborhood" name="neighborhood" placeholder="e.g., Mission District">
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
                            <input type="checkbox" name="availability" value="weekday">
                            Weekdays
                        </label>
                        <label>
                            <input type="checkbox" name="availability" value="weekend">
                            Weekends
                        </label>
                    </div>
                </div>

                <button type="submit" class="btn btn-primary">Create Profile</button>
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

    document.getElementById('create-profile-form').addEventListener('submit', async (e) => {
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
            const profile = await api.createProfile(data);
            state.setCurrentProfile(profile.id);
            router.navigate(`profile/${profile.id}`);
        } catch (error) {
            document.getElementById('error-message').innerHTML = `
                <div class="error">${error.message}</div>
            `;
        }
    });
}
