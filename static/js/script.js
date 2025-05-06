// Dog Breeding Management Application - Client-side functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Filter functionality for dogs list
    setupFilters();
    
    // Setup dynamic mating selection based on mother
    setupMatingDependency();
    
    // Delete confirmation modals
    setupDeleteConfirmations();
    
    // Form validation
    setupFormValidation();
    
    // Date picker initialization
    setupDatepickers();
    
    // Create charts if statistics page
    if (document.getElementById('yearly-stats-chart')) {
        setupCharts();
    }
});

// Setup filters for dog list and other list pages
function setupFilters() {
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            // Remove empty parameters from the form
            const formElements = filterForm.elements;
            for (let i = 0; i < formElements.length; i++) {
                if (!formElements[i].value && formElements[i].name) {
                    formElements[i].disabled = true;
                }
            }
        });
    }
}

// Setup dependencies between mother selection and available matings
function setupMatingDependency() {
    const motherSelect = document.getElementById('mother_id');
    const matingSelect = document.getElementById('mating_id');
    
    if (motherSelect && matingSelect) {
        motherSelect.addEventListener('change', function() {
            const motherId = this.value;
            
            // Clear current options
            matingSelect.innerHTML = '<option value="">Seleziona un accoppiamento (opzionale)</option>';
            
            if (motherId) {
                // Fetch matings for the selected mother via AJAX
                fetch(`/api/matings?female_id=${motherId}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(mating => {
                            const option = document.createElement('option');
                            option.value = mating.id;
                            option.textContent = `${mating.date} con ${mating.male_name} (${mating.type})`;
                            matingSelect.appendChild(option);
                        });
                    })
                    .catch(error => {
                        console.error('Error fetching matings:', error);
                    });
            }
        });
    }
}

// Setup delete confirmation modals
function setupDeleteConfirmations() {
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const confirmModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
            const confirmButton = document.getElementById('confirmDeleteButton');
            const formAction = this.getAttribute('data-action');
            
            confirmButton.addEventListener('click', function() {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = formAction;
                document.body.appendChild(form);
                form.submit();
            }, { once: true });
            
            confirmModal.show();
        });
    });
}

// Setup form validation
function setupFormValidation() {
    // Example validation for adding a new dog
    const dogForm = document.querySelector('form.needs-validation');
    
    if (dogForm) {
        dogForm.addEventListener('submit', function(event) {
            if (!dogForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            dogForm.classList.add('was-validated');
        });
    }
    
    // Validate birth form specifically
    const birthForm = document.getElementById('birth-form');
    if (birthForm) {
        birthForm.addEventListener('submit', function(event) {
            const puppiesCount = parseInt(document.getElementById('puppies_count').value, 10);
            const maleCount = parseInt(document.getElementById('male_count').value, 10);
            const femaleCount = parseInt(document.getElementById('female_count').value, 10);
            
            if (maleCount + femaleCount !== puppiesCount) {
                event.preventDefault();
                alert('La somma dei cuccioli maschi e femmine deve essere uguale al numero totale di cuccioli.');
            }
        });
    }
}

// Setup datepickers
function setupDatepickers() {
    // Apply datepicker to all date inputs if needed
    // Note: Using HTML5 date inputs by default
}

// Setup charts for statistics page
function setupCharts() {
    // Get the yearly stats from the data attribute
    const statsElement = document.getElementById('yearly-stats-data');
    if (!statsElement) return;
    
    try {
        const statsData = statsElement.getAttribute('data-stats');
        if (!statsData) {
            console.error('No data-stats attribute found');
            return;
        }
        
        const stats = JSON.parse(statsData);
        
        if (!Array.isArray(stats) || stats.length === 0) {
            console.log('No yearly stats data available or invalid format');
            return;
        }
        
        // Create the chart using Chart.js
        const ctx = document.getElementById('yearly-stats-chart');
        if (!ctx) {
            console.error('Could not find chart canvas element');
            return;
        }
        
        const chart = new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: stats.map(stat => stat.year),
                datasets: [
                    {
                        label: 'Nascite',
                        data: stats.map(stat => stat.births),
                        backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Cuccioli',
                        data: stats.map(stat => stat.puppies),
                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Accoppiamenti',
                        data: stats.map(stat => stat.matings),
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error setting up chart:', error);
    }
}
