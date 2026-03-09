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
                    
                    // Show test mode notice if applicable
                    if (result.test_mode) {
                        const testNotice = document.createElement('div');
                        testNotice.className = 'mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800';
                        testNotice.innerHTML = `
                            <strong>🧪 Test Mode Active:</strong> A test email has been sent to <strong>tomrbon@gmail.com</strong> with subject "TEST: PLUMBING".
                            ${result.mockup_url ? `Preview URL: <a href="${result.mockup_url}" class="underline font-medium" target="_blank">${result.mockup_url}</a>` : ''}
                        `;
                        successMessage.appendChild(testNotice);
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
