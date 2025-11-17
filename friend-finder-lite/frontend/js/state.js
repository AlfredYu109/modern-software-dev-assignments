class AppState {
    constructor() {
        this.currentProfileId = localStorage.getItem('currentProfileId');
        this.updateNav();
    }

    setCurrentProfile(profileId) {
        this.currentProfileId = profileId;
        localStorage.setItem('currentProfileId', profileId);
        this.updateNav();
    }

    clearCurrentProfile() {
        this.currentProfileId = null;
        localStorage.removeItem('currentProfileId');
        this.updateNav();
    }

    updateNav() {
        const hasProfile = !!this.currentProfileId;

        document.getElementById('nav-matches').style.display = hasProfile ? 'block' : 'none';
        document.getElementById('nav-connections').style.display = hasProfile ? 'block' : 'none';
        document.getElementById('nav-profile').style.display = hasProfile ? 'block' : 'none';
        document.getElementById('nav-create').style.display = hasProfile ? 'none' : 'block';

        if (hasProfile) {
            document.getElementById('nav-matches').href = `#matches/${this.currentProfileId}`;
            document.getElementById('nav-connections').href = `#connections/${this.currentProfileId}`;
            document.getElementById('nav-profile').href = `#profile/${this.currentProfileId}`;
        }
    }
}

export const state = new AppState();
