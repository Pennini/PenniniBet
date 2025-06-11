import { initMobileMenu } from './components/mobileMenu.js';
import { initProfileDropdown } from './components/profileDropdown.js';
import { initActiveNavigation } from './components/activeNavigation.js';

// Initialize all components
document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initProfileDropdown();
    initActiveNavigation();
});

// Toggle password visibility
document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('id_password');
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function () {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
            passwordInput.focus();
            passwordInput.setSelectionRange(passwordInput.value.length, passwordInput.value.length);
        });
    }
});