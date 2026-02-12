
if (registerResponse.ok) {
    showAlert('Registration successful! Redirecting to login...', 'success');
    setTimeout(() => {
        window.location.href = 'login.html';
    }, 2000);
}
window.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token) {
        window.location.href = 'index.html';
    }
});
if (response.ok) {
    // Store authentication data
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));

    showAlert('Login successful! Redirecting...', 'success');

    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1000);
}
function handleLogout(event) {
    event.preventDefault();

    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('cart');
        showToast('Logged out successfully');

        setTimeout(() => {
            window.location.href = 'register.html';
        }, 1000);
    }
}

function checkAuthAndLoadUser() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');

    if (!token || !user) {
        window.location.href = 'register.html';
        return;
    }

    try {
        const userData = JSON.parse(user);
        document.getElementById('userName').textContent =
            userData.full_name || userData.email.split('@')[0];
    } catch (error) {
        console.error('Error parsing user data:', error);
        window.location.href = 'register.html';
    }
}