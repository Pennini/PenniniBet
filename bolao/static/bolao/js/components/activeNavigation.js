export const initActiveNavigation = () => {
    const updateActiveLink = () => {
        const navLinksElements = document.querySelectorAll('.nav-link');
        const currentPath = window.location.pathname;

        navLinksElements.forEach(link => {
            // Remove active class from all links
            link.classList.remove('active');

            // Add active class if href matches current path
            if (link.getAttribute('href') === currentPath ||
                (currentPath === '/' && link.getAttribute('href') === '/') ||
                (currentPath.includes(link.getAttribute('href')) && link.getAttribute('href') !== '/')) {
                link.classList.add('active');
            }
        });
    };

    // Update active link on page load
    document.addEventListener('DOMContentLoaded', updateActiveLink);

    // Update active link on navigation
    window.addEventListener('popstate', updateActiveLink);
}; 