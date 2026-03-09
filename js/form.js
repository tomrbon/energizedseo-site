// EnergizedSEO Form Submission
// Posts to Cloudflare Pages Function backend

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[name="contact"]');
    const successMessage = document.getElementById('success-message');
    const submitButton = form?.querySelector('button[type="submit"]');
    
    if (!form) return;
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="animate-pulse">Submitting...</span>';
        }
        
        const formData = new FormData(form);
        
        try {
            const response = await fetch('/api/lead', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                // Hide form, show success message
                form.classList.add('hidden');
                if (successMessage) {
                    successMessage.classList.remove('hidden');
                    
                    // Show sandbox mode notice if applicable
                    if (result.sandbox_mode) {
                        const sandboxNotice = document.createElement('div');
                        sandboxNotice.className = 'mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-800';
                        sandboxNotice.innerHTML = `
                            <strong>🧪 Sandbox Mode:</strong> No email sent. 
                            ${result.mockup_url ? `Preview would be at: <a href="${result.mockup_url}" class="underline font-medium">${result.mockup_url}</a>` : ''}
                        `;
                        successMessage.appendChild(sandboxNotice);
                    }
                }
                
                // Scroll to success message
                successMessage?.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                // Reset form
                form.reset();
            } else {
                throw new Error(result.error || 'Submission failed');
            }
        } catch (error) {
            console.error('Form submission error:', error);
            alert('Oops! Something went wrong. Please email us at hello@energizedseo.com');
        } finally {
            // Reset button state
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.innerHTML = 'Get Your Free Mockup →';
            }
        }
    });
});
