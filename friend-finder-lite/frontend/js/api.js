const API_BASE = 'http://localhost:5000/api';

export const api = {
    async getProfiles(filters = {}) {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE}/profiles?${params}`);
        if (!response.ok) throw new Error('Failed to fetch profiles');
        return response.json();
    },

    async getProfile(id) {
        const response = await fetch(`${API_BASE}/profiles/${id}`);
        if (!response.ok) throw new Error('Profile not found');
        return response.json();
    },

    async createProfile(data) {
        const response = await fetch(`${API_BASE}/profiles`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to create profile');
        }
        return response.json();
    },

    async updateProfile(id, data) {
        const response = await fetch(`${API_BASE}/profiles/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to update profile');
        }
        return response.json();
    },

    async deleteProfile(id) {
        const response = await fetch(`${API_BASE}/profiles/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete profile');
    },

    async getMatches(profileId) {
        const response = await fetch(`${API_BASE}/profiles/${profileId}/matches`);
        if (!response.ok) throw new Error('Failed to fetch matches');
        return response.json();
    },

    async createConnection(senderId, receiverId) {
        const response = await fetch(`${API_BASE}/connections`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sender_id: senderId, receiver_id: receiverId })
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to send connection request');
        }
        return response.json();
    },

    async updateConnection(connectionId, status) {
        const response = await fetch(`${API_BASE}/connections/${connectionId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });
        if (!response.ok) throw new Error('Failed to update connection');
        return response.json();
    },

    async getSentConnections(profileId) {
        const response = await fetch(`${API_BASE}/connections/sent/${profileId}`);
        if (!response.ok) throw new Error('Failed to fetch sent connections');
        return response.json();
    },

    async getReceivedConnections(profileId) {
        const response = await fetch(`${API_BASE}/connections/received/${profileId}`);
        if (!response.ok) throw new Error('Failed to fetch received connections');
        return response.json();
    },

    async getFriends(profileId) {
        const response = await fetch(`${API_BASE}/connections/friends/${profileId}`);
        if (!response.ok) throw new Error('Failed to fetch friends');
        return response.json();
    }
};
