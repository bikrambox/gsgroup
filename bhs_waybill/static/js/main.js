// Main JavaScript for BHS Waybill SPA

document.addEventListener('DOMContentLoaded', function() {
    // Navigation handling
    const navLinks = document.querySelectorAll('.nav-link');
    const contentSections = document.querySelectorAll('.content-section');
    
    // Add click event listeners to all navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get the page to show from data attribute
            const pageToShow = this.getAttribute('data-page');
            
            // Update active state in navigation
            navLinks.forEach(navLink => navLink.classList.remove('active'));
            this.classList.add('active');
            
            // Hide all content sections
            contentSections.forEach(section => section.classList.add('d-none'));
            
            // Show the selected content section
            document.getElementById(`${pageToShow}-content`).classList.remove('d-none');
        });
    });
    
    // Form submission handling for contact form
    const contactForm = document.querySelector('#contact-content form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            
            // In a real application, you would send this data to the server
            // For this demo, we'll just show an alert
            alert(`Thank you, ${name}! Your message has been received. We'll contact you at ${email} soon.`);
            
            // Reset the form
            this.reset();
        });
    }
    
    // Add click event listeners to "Learn More" buttons
    const learnMoreButtons = document.querySelectorAll('.card .btn-primary');
    learnMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const featureTitle = this.closest('.card').querySelector('.card-title').textContent;
            alert(`You clicked to learn more about ${featureTitle}. Additional information would be shown here.`);
        });
    });
});
