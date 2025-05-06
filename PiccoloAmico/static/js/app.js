document.addEventListener('DOMContentLoaded', function() {
    // Enable all tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Handle form submissions with fetch API
    const apiForms = document.querySelectorAll('form[data-api="true"]');
    
    apiForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const url = form.action;
            const method = form.dataset.method || 'POST';
            const formData = new FormData(form);
            
            const data = {};
            formData.forEach((value, key) => {
                // Handle checkboxes
                if (form.elements[key].type === 'checkbox') {
                    data[key] = form.elements[key].checked;
                } else {
                    data[key] = value;
                }
            });
            
            fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (form.dataset.redirect) {
                    window.location.href = form.dataset.redirect;
                } else {
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please check the console for details.');
            });
        });
    });
    
    // Initialize date pickers with today's date
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    
    dateInputs.forEach(input => {
        if (!input.value && !input.dataset.noDefault) {
            input.value = today;
        }
    });
    
    // Handle delete confirmations
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const confirmMessage = button.dataset.confirmMessage || 'Are you sure you want to delete this item? This action cannot be undone.';
            
            if (confirm(confirmMessage)) {
                const url = button.href || button.dataset.url;
                const redirectUrl = button.dataset.redirect;
                
                fetch(url, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (redirectUrl) {
                        window.location.href = redirectUrl;
                    } else {
                        window.location.reload();
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting. Please check the console for details.');
                });
            }
        });
    });
});
