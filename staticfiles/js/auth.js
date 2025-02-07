// Handle logout functionality
document.addEventListener('DOMContentLoaded', function() {
    // Find all logout links
    const logoutLinks = document.querySelectorAll('a[href*="/api/auth/logout/"]');
    
    logoutLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get the current page URL to redirect back to after logout
            const currentPage = window.location.pathname;
            
            // Send POST request to logout endpoint
            fetch('/api/auth/logout/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                // Redirect to the original page
                window.location.href = data.redirect_url;
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback to current page on error
                window.location.href = currentPage;
            });
        });
    });
});

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
