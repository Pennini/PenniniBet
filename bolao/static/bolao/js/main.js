import { initMobileMenu } from './components/mobileMenu.js';
import { initProfileDropdown } from './components/profileDropdown.js';
import { initActiveNavigation } from './components/activeNavigation.js';

// Initialize all components
document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initProfileDropdown();
    initActiveNavigation();
}); 