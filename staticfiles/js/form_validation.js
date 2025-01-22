document.addEventListener('DOMContentLoaded', function () {
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach(group => {
        const input = group.querySelector('input');
        const errorMessage = group.querySelector('.error-message');
        const formText = group.querySelector('.form-text');

        if (errorMessage) {
            // Show instructions if there's an error
            formText.style.display = 'block';
        } else {
            // Hide instructions initially
            formText.style.display = 'none';
        }

        // Show instructions on input focus
        input.addEventListener('focus', () => {
            formText.style.display = 'block';
        });

        // Hide instructions on input blur if no error
        input.addEventListener('blur', () => {
            if (!errorMessage) {
                formText.style.display = 'none';
            }
        });
    });
});