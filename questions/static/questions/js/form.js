// Form validation and enhancement
document.addEventListener('DOMContentLoaded', function() {
    // Form submission handling
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                // Store original button text
                const originalText = submitButton.innerHTML;
                
                // Only disable the button if the form is valid
                if (form.checkValidity()) {
                    submitButton.disabled = true;
                    submitButton.innerHTML = 'Gönderiliyor...';
                    
                    // Re-enable the button if the form submission takes too long
                    setTimeout(() => {
                        submitButton.disabled = false;
                        submitButton.innerHTML = originalText;
                    }, 5000); // 5 second timeout
                }
            }
        });
    }

    // Character counter for text areas
    const textAreas = document.querySelectorAll('textarea');
    textAreas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('div');
            counter.className = 'char-counter text-muted small';
            textarea.parentNode.appendChild(counter);

            function updateCounter() {
                const remaining = maxLength - textarea.value.length;
                counter.textContent = `${remaining} karakter kaldı`;
            }

            textarea.addEventListener('input', updateCounter);
            updateCounter(); // Initial count
        }
    });

    // Handle progress bar
    const progressBar = document.querySelector('.progress-bar-custom');
    if (progressBar) {
        const progress = progressBar.getAttribute('data-progress');
        progressBar.style.setProperty('--progress', progress + '%');
    }
}); 