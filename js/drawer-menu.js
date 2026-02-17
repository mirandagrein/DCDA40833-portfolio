/**
 * Responsive Drawer Menu
 * Vanilla JavaScript - No frameworks required
 * Author: Miranda Grein
 * Course: DCDA 40833
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navOverlay = document.querySelector('.nav-overlay');
    const body = document.body;

    // Check if elements exist (in case script is loaded on a page without the menu)
    if (!menuToggle || !navMenu || !navOverlay) {
        return;
    }

    /**
     * Toggle menu open/closed
     */
    function toggleMenu() {
        menuToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        navOverlay.classList.toggle('active');
        body.classList.toggle('menu-open');
    }

    /**
     * Close menu
     */
    function closeMenu() {
        menuToggle.classList.remove('active');
        navMenu.classList.remove('active');
        navOverlay.classList.remove('active');
        body.classList.remove('menu-open');
    }

    // Event listener for hamburger button
    menuToggle.addEventListener('click', toggleMenu);

    // Event listener for overlay (clicking outside closes menu)
    navOverlay.addEventListener('click', closeMenu);

    // Close menu when clicking a nav link
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    // Close menu on escape key press
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            closeMenu();
        }
    });

    // Handle window resize - close menu if resizing to desktop view
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
                closeMenu();
            }
        }, 250);
    });
});
