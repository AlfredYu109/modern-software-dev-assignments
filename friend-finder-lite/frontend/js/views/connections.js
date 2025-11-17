import { api } from '../api.js';

export async function renderConnections(profileId) {
    const app = document.getElementById('app');

    app.innerHTML = `
        <div class="container">
            <h1>My Connections</h1>

            <div class="tabs">
                <button class="tab active" data-tab="received">Requests Received (<span id="received-count">0</span>)</button>
                <button class="tab" data-tab="sent">Requests Sent (<span id="sent-count">0</span>)</button>
                <button class="tab" data-tab="friends">Friends (<span id="friends-count">0</span>)</button>
            </div>

            <div id="tab-content"></div>
        </div>
    `;

    let sentConnections = [];
    let receivedConnections = [];
    let friends = [];

    async function loadConnections() {
        try {
            [sentConnections, receivedConnections, friends] = await Promise.all([
                api.getSentConnections(profileId),
                api.getReceivedConnections(profileId),
                api.getFriends(profileId)
            ]);

            const pendingReceived = receivedConnections.filter(c => c.status === 'pending');
            document.getElementById('received-count').textContent = pendingReceived.length;
            document.getElementById('sent-count').textContent = sentConnections.length;
            document.getElementById('friends-count').textContent = friends.length;
        } catch (error) {
            console.error('Failed to load connections:', error);
        }
    }

    function renderReceivedTab() {
        const pending = receivedConnections.filter(c => c.status === 'pending');
        const content = document.getElementById('tab-content');

        if (pending.length === 0) {
            content.innerHTML = `
                <div class="empty-state">
                    <h3>No pending requests</h3>
                    <p>When someone sends you a connection request, it will appear here</p>
                </div>
            `;
            return;
        }

        content.innerHTML = `
            <div class="connection-list">
                ${pending.map(conn => `
                    <div class="connection-card">
                        <div class="connection-info" style="cursor: pointer;" data-profile-id="${conn.sender.id}">
                            <h4>${conn.sender.name}</h4>
                            ${conn.sender.city ? `<p class="location">${conn.sender.city}</p>` : ''}
                        </div>
                        <div class="button-group">
                            <button class="btn btn-success" data-accept="${conn.id}">Accept</button>
                            <button class="btn btn-danger" data-decline="${conn.id}">Decline</button>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        content.querySelectorAll('[data-profile-id]').forEach(el => {
            el.addEventListener('click', () => {
                window.location.hash = `profile/${el.getAttribute('data-profile-id')}`;
            });
        });

        content.querySelectorAll('[data-accept]').forEach(btn => {
            btn.addEventListener('click', async () => {
                try {
                    await api.updateConnection(btn.getAttribute('data-accept'), 'accepted');
                    await loadConnections();
                    renderReceivedTab();
                } catch (error) {
                    alert(error.message);
                }
            });
        });

        content.querySelectorAll('[data-decline]').forEach(btn => {
            btn.addEventListener('click', async () => {
                try {
                    await api.updateConnection(btn.getAttribute('data-decline'), 'declined');
                    await loadConnections();
                    renderReceivedTab();
                } catch (error) {
                    alert(error.message);
                }
            });
        });
    }

    function renderSentTab() {
        const content = document.getElementById('tab-content');

        if (sentConnections.length === 0) {
            content.innerHTML = `
                <div class="empty-state">
                    <h3>No sent requests</h3>
                    <p>Browse profiles and send connection requests to start making friends</p>
                </div>
            `;
            return;
        }

        content.innerHTML = `
            <div class="connection-list">
                ${sentConnections.map(conn => `
                    <div class="connection-card">
                        <div class="connection-info" style="cursor: pointer;" data-profile-id="${conn.receiver.id}">
                            <h4>${conn.receiver.name}</h4>
                            ${conn.receiver.city ? `<p class="location">${conn.receiver.city}</p>` : ''}
                        </div>
                        <span class="connection-status ${conn.status}">${conn.status.charAt(0).toUpperCase() + conn.status.slice(1)}</span>
                    </div>
                `).join('')}
            </div>
        `;

        content.querySelectorAll('[data-profile-id]').forEach(el => {
            el.addEventListener('click', () => {
                window.location.hash = `profile/${el.getAttribute('data-profile-id')}`;
            });
        });
    }

    function renderFriendsTab() {
        const content = document.getElementById('tab-content');

        if (friends.length === 0) {
            content.innerHTML = `
                <div class="empty-state">
                    <h3>No friends yet</h3>
                    <p>Accept connection requests to build your friend network</p>
                </div>
            `;
            return;
        }

        content.innerHTML = `
            <div class="profile-grid">
                ${friends.map(friend => `
                    <div class="profile-card" data-profile-id="${friend.id}">
                        <h3>${friend.name}</h3>
                        ${friend.city ? `
                            <p class="location">${friend.city}${friend.neighborhood ? `, ${friend.neighborhood}` : ''}</p>
                        ` : ''}
                        ${friend.bio ? `<p class="bio">${friend.bio}</p>` : ''}
                    </div>
                `).join('')}
            </div>
        `;

        content.querySelectorAll('.profile-card').forEach(card => {
            card.addEventListener('click', () => {
                window.location.hash = `profile/${card.getAttribute('data-profile-id')}`;
            });
        });
    }

    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const tabName = tab.getAttribute('data-tab');
            if (tabName === 'received') renderReceivedTab();
            else if (tabName === 'sent') renderSentTab();
            else if (tabName === 'friends') renderFriendsTab();
        });
    });

    await loadConnections();
    renderReceivedTab();
}
