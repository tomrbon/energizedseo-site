// Netlify Forms AJAX submission
// Prevents page reload and shows success message

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[name="contact"]');
    const successMessage = document.getElementById('success-message');
    
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(formData).toString()
        })
        .then(() => {
            // Hide form, show success message
            form.classList.add('hidden');
            successMessage.classList.remove('hidden');
            
            // Scroll to success message
            successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
        })
        .catch((error) => {
            console.error('Error submitting form:', error);
            alert('Oops! Something went wrong. Please email us at hello@energizedseo.com');
        });
    });
});
