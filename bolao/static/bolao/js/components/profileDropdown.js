export const initProfileDropdown = () => {
    const avatar = document.getElementById('avatar');
    const dropdown = document.getElementById('dropdownMenu');

    if (!avatar || !dropdown) return;

    // Toggle dropdown on avatar click
    avatar.addEventListener('click', () => {
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    });

    // Close dropdown when clicking outside
    window.addEventListener('click', function (e) {
        if (!avatar.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
}; 