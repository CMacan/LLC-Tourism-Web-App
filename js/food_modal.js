document.addEventListener('DOMContentLoaded', function() {
    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Search functionality
    const searchInput = document.getElementById('searchRestaurant');
    const clearButton = document.getElementById('clearSearch');

    function performSearch(searchTerm) {
        const restaurantCards = document.querySelectorAll('.col-md-4[data-id]');
        let hasResults = false;

        restaurantCards.forEach(card => {
            const name = card.querySelector('.card-title').textContent.toLowerCase();
            const address = card.querySelector('.text-muted').textContent.toLowerCase();
            const cuisine = card.querySelector('.card-text:nth-child(3)')?.textContent.toLowerCase() || '';
            const searchValue = searchTerm.toLowerCase();

            if (name.includes(searchValue) || 
                address.includes(searchValue) || 
                cuisine.includes(searchValue)) {
                card.style.display = '';
                hasResults = true;
            } else {
                card.style.display = 'none';
            }
        });

        handleNoResults(hasResults, searchTerm);
    }

    function handleNoResults(hasResults, searchTerm) {
        let noResultsMsg = document.getElementById('noResultsMessage');
        
        if (!hasResults && searchTerm !== '') {
            if (!noResultsMsg) {
                noResultsMsg = document.createElement('div');
                noResultsMsg.id = 'noResultsMessage';
                noResultsMsg.className = 'col-12 text-center mt-4';
                noResultsMsg.innerHTML = '<p class="text-muted">No restaurants found matching your search.</p>';
                document.querySelector('.row.mt-4').appendChild(noResultsMsg);
            }
        } else if (noResultsMsg) {
            noResultsMsg.remove();
        }
    }

    // Add event listeners for search
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function(e) {
            performSearch(e.target.value);
        }, 300));
    }

    if (clearButton) {
        clearButton.addEventListener('click', function() {
            searchInput.value = '';
            performSearch('');
        });
    }

    // Form submission handlers
    const addForm = document.getElementById('addRestaurantForm');
    if (addForm) {
        addForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            try {
                const formData = new FormData(this);
                const jsonData = {};
                
                for (let [key, value] of formData.entries()) {
                    if (key !== 'photo') {
                        jsonData[key] = value;
                    }
                }
                
                formData.set('data', JSON.stringify(jsonData));
                
                const response = await fetch('/admin/restaurants/create/', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                if (data.status === 'success') {
                    window.location.reload();
                } else {
                    alert('Error: ' + (data.message || 'Unknown error occurred'));
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error submitting form: ' + error.message);
            }
        });
    }

    // Update form handler
    const updateForm = document.getElementById('updateRestaurantForm');
    if (updateForm) {
        updateForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            try {
                const id = this.getAttribute('data-id');
                const formData = new FormData(this);
                const jsonData = {};
                
                for (let [key, value] of formData.entries()) {
                    if (key !== 'photo') {
                        jsonData[key] = value;
                    }
                }
                
                formData.set('data', JSON.stringify(jsonData));
                
                const response = await fetch(`/admin/restaurants/${id}/update/`, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                if (data.status === 'success') {
                    window.location.reload();
                } else {
                    alert('Error: ' + (data.message || 'Unknown error occurred'));
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error updating restaurant: ' + error.message);
            }
        });
    }
});

// Delete confirmation
async function confirmDeletion(id) {
    if (confirm('Are you sure you want to delete this restaurant?')) {
        try {
            const response = await fetch(`/admin/restaurants/${id}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data.status === 'success') {
                window.location.reload();
            } else {
                alert('Error: ' + (data.message || 'Unknown error occurred'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error deleting restaurant: ' + error.message);
        }
    }
}

// Get CSRF token
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

// Update modal population
async function populateUpdateModal(id) {
    try {
        const response = await fetch(`/admin/restaurants/${id}/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const form = document.getElementById('updateRestaurantForm');
        if (!form) {
            throw new Error('Update form not found');
        }

        form.setAttribute('data-id', id);
        
        // Populate form fields
        const fields = {
            'name': '#update-name',
            'address': '#update-address',
            'cuisine_type': '#update-cuisine-type',
            'price_range': '#update-price-range',
            'rating': '#update-rating',
            'opening_hours': '#update-opening-hours',
            'website': '#update-website',
            'contact_number': '#update-contact',
            'menu_url': '#update-menu-url'
        };

        for (const [key, selector] of Object.entries(fields)) {
            const element = form.querySelector(selector);
            if (element) {
                element.value = data[key] || '';
            }
        }

        // Handle boolean fields
        const isOpenCheckbox = form.querySelector('#update-is-open');
        if (isOpenCheckbox) {
            isOpenCheckbox.checked = data.is_open;
        }

    } catch (error) {
        console.error('Error:', error);
        alert('Error loading restaurant data: ' + error.message);
    }
}

// Add click handlers to update buttons
document.querySelectorAll('[data-bs-target="#updateModal"]').forEach(button => {
    button.addEventListener('click', function() {
        const id = this.getAttribute('data-id');
        if (id) {
            populateUpdateModal(id);
        }
    });
});
