// Debug: confirm script is loaded in browser console
console.log('script.js loaded');

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const navbar = document.querySelector('.navbar');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navbar.classList.toggle('active');
        });
    }

    // Auto-fill membership type from card buttons
    const membershipButtons = document.querySelectorAll('.membership-register-btn');
    membershipButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const membershipType = this.getAttribute('data-type');
            const selectElement = document.getElementById('membership-type');
            if (selectElement) {
                selectElement.value = membershipType;
            }
            // Scroll to registration form
            const registerSection = document.getElementById('register');
            if (registerSection) {
                registerSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Set minimum date for appointment booking to today
    const dateInput = document.getElementById('appt-date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }

    // Form validation messages
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#ef4444';
                } else {
                    field.style.borderColor = '#e5e7eb';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            // allow normal behaviour for links that only reference the top (#)
            const href = this.getAttribute('href');
            if (href === '#') return;
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Active navigation link highlighting
    const currentLocation = window.location.pathname.replace(/\/$/, ''); // normalize
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        try {
            const linkHref = link.getAttribute('href');
            if (!linkHref) return;
            // For Django generated links, href may be absolute or relative; normalize
            const normalizedHref = linkHref.replace(window.location.origin, '').replace(/\/$/, '');
            if (normalizedHref === currentLocation || (normalizedHref === '' && currentLocation === '/')) {
                link.classList.add('active');
            }
        } catch (err) {
            // ignore malformed href
        }
    });

    // Logo image fallback: show text if image fails to load
    const logoImg = document.getElementById('siteLogo');
    const logoText = document.getElementById('logoText');
    if (logoImg) {
        logoImg.addEventListener('error', function() {
            logoImg.style.display = 'none';
            if (logoText) logoText.style.display = 'inline-block';
        });
        logoImg.addEventListener('load', function() {
            if (logoText) logoText.style.display = 'none';
        });
        // handle cached broken images
        if (logoImg.complete && logoImg.naturalWidth === 0) {
            logoImg.dispatchEvent(new Event('error'));
        }
    }
});