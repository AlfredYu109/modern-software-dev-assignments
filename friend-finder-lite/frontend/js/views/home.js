import { state } from '../state.js';

export function renderHome() {
    const app = document.getElementById('app');

    const hasProfile = !!state.currentProfileId;

    app.innerHTML = `
        <div class="container">
            <h1>Welcome to Friend Finder Lite</h1>
            <p style="margin-top: 1rem; font-size: 1.1rem; line-height: 1.6;">
                Connect with recent college graduates in your city and make new friends based on shared interests.
            </p>

            <div style="margin-top: 2rem;">
                ${!hasProfile ? `
                    <div>
                        <h2>Get Started</h2>
                        <p style="margin: 1rem 0;">
                            Create your profile to start browsing and connecting with potential friends.
                        </p>
                        <a href="#create" class="btn btn-primary">Create Profile</a>
                    </div>
                ` : `
                    <div>
                        <h2>What would you like to do?</h2>
                        <div class="action-links">
                            <a href="#browse" class="btn btn-primary">Browse Profiles</a>
                            <a href="#matches/${state.currentProfileId}" class="btn btn-primary">View Matches</a>
                            <a href="#connections/${state.currentProfileId}" class="btn btn-primary">My Connections</a>
                            <a href="#profile/${state.currentProfileId}" class="btn btn-secondary">View My Profile</a>
                        </div>
                    </div>
                `}
            </div>

            <div class="info-section">
                <h2>How It Works</h2>
                <ol>
                    <li>Create your profile with interests and activities you enjoy</li>
                    <li>Browse other profiles or view your personalized matches</li>
                    <li>Send connection requests to people you'd like to meet</li>
                    <li>Connect with friends and start building your network</li>
                </ol>
            </div>
        </div>
    `;
}
