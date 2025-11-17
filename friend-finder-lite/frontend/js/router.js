import { renderHome } from './views/home.js';
import { renderBrowse } from './views/browse.js';
import { renderCreateProfile } from './views/createProfile.js';
import { renderProfileDetail } from './views/profileDetail.js';
import { renderEditProfile } from './views/editProfile.js';
import { renderMatches } from './views/matches.js';
import { renderConnections } from './views/connections.js';

export class Router {
    constructor() {
        this.routes = {
            'home': renderHome,
            'browse': renderBrowse,
            'create': renderCreateProfile,
            'profile': renderProfileDetail,
            'edit': renderEditProfile,
            'matches': renderMatches,
            'connections': renderConnections
        };

        window.addEventListener('hashchange', () => this.handleRoute());
        window.addEventListener('load', () => this.handleRoute());
    }

    handleRoute() {
        const hash = window.location.hash.slice(1) || 'home';
        const [route, param] = hash.split('/');

        const handler = this.routes[route];
        if (handler) {
            handler(param);
        } else {
            renderHome();
        }
    }

    navigate(path) {
        window.location.hash = path;
    }
}

export const router = new Router();
