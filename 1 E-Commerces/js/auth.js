// auth.js - Add this file to your frontend folder
// Include this script in ALL HTML pages except register.html and login.html

class AuthGuard {
    constructor() {
        this.publicPages = ['login.html', 'register.html'];
        this.init();
    }

    init() {
        // Check authentication on page load
        window.addEventListener('DOMContentLoaded', () => {
            this.checkAuth();
        });
    }

    // Check if user is authenticated
    isAuthenticated() {
        const token = localStorage.getItem('token');
        const user = localStorage.getItem('user');
        return token && user;
    }

    // Get current page name
    getCurrentPage() {
        return window.location.pathname.split('/').pop() || 'index.html';
    }

    // Check if current page is public
    isPublicPage() {
        const currentPage = this.getCurrentPage();
        return this.publicPages.includes(currentPage);
    }

    // Main authentication check
    checkAuth() {
        const currentPage = this.getCurrentPage();
        const isAuthenticated = this.isAuthenticated();

        // If not authenticated and trying to access protected page
        if (!isAuthenticated && !this.isPublicPage()) {
            this.redirectToRegister();
            return;
        }

        // If authenticated and trying to access login/register
        if (isAuthenticated && this.isPublicPage()) {
            this.redirectToHome();
            return;
        }
    }

    // Redirect to register page
    redirectToRegister() {
        window.location.href = 'register.html';
    }

    // Redirect to home page
    redirectToHome() {
        window.location.href = 'index.html';
    }

    // Logout function
    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('cart');
        this.redirectToRegister();
    }

    // Get user data
    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }

    // Get token
    getToken() {
        return localStorage.getItem('token');
    }

    // Set authentication data
    setAuth(token, user) {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
    }
}

// Create global instance
const authGuard = new AuthGuard();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AuthGuard;
}