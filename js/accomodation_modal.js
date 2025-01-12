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

// Document ready handler
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchAccommodation');
    const clearButton = document.getElementById('clearSearch');

    if (!searchInput) {
        console.error('Search input not found');
        return;
    }

    // Function to perform the search
    function performSearch(searchTerm) {
        const accommodationCards = document.querySelectorAll('.col-md-4[data-id]');
        let hasResults = false;

        accommodationCards.forEach(card => {
            const name = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
            const address = card.querySelector('.text-muted')?.textContent.toLowerCase() || '';
            const description = card.querySelector('.description-text')?.textContent.toLowerCase() || '';
            const searchValue = searchTerm.toLowerCase();

            if (name.includes(searchValue) || 
                address.includes(searchValue) || 
                description.includes(searchValue)) {
                card.style.display = '';
                hasResults = true;
            } else {
                card.style.display = 'none';
            }
        });

        // Handle no results message
        handleNoResults(hasResults, searchTerm);
    }

    // Function to handle no results message
    function handleNoResults(hasResults, searchTerm) {
        let noResultsMsg = document.getElementById('noResultsMessage');
        
        if (!hasResults && searchTerm !== '') {
            if (!noResultsMsg) {
                noResultsMsg = document.createElement('div');
                noResultsMsg.id = 'noResultsMessage';
                noResultsMsg.className = 'col-12 text-center mt-4';
                noResultsMsg.innerHTML = '<p class="text-muted">No accommodations found matching your search.</p>';
                document.querySelector('.row.mt-4').appendChild(noResultsMsg);
            }
        } else if (noResultsMsg) {
            noResultsMsg.remove();
        }
    }

    // Add event listener with debounce
    searchInput.addEventListener('input', debounce(function(e) {
        performSearch(e.target.value);
    }, 300));

    // Clear button functionality
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            searchInput.value = '';
            performSearch('');
        });
    }

    // Add escape key functionality
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Escape') {
            this.value = '';
            performSearch('');
        }
    });
});

// Form submission handlers
document.getElementById('addAccommodationForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const jsonData = {};
    
    // Convert form data to JSON, excluding file inputs
    for (let [key, value] of formData.entries()) {
        if (key !== 'image') {
            if (key === 'amenities[]') {
                if (!jsonData.amenities) jsonData.amenities = [];
                jsonData.amenities.push(value);
            } else {
                jsonData[key] = value;
            }
        }
    }
    
    formData.set('data', JSON.stringify(jsonData));
    
    fetch('/admin_side/accommodations/create/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Accommodation added successfully!');
            location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('updateAccommodationForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const id = this.getAttribute('data-id');
    const formData = new FormData(this);
    const jsonData = {};
    
    for (let [key, value] of formData.entries()) {
        if (key !== 'image') {
            if (key === 'amenities[]') {
                if (!jsonData.amenities) jsonData.amenities = [];
                jsonData.amenities.push(value);
            } else {
                jsonData[key] = value;
            }
        }
    }
    
    formData.set('data', JSON.stringify(jsonData));
    
    fetch(`/admin_side/accommodations/${id}/update/`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Accommodation updated successfully!');
            location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Delete confirmation
function confirmDeletion(id) {
    if (confirm('Are you sure you want to delete this accommodation?')) {
        fetch(`/admin_side/accommodations/${id}/delete/`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Accommodation deleted successfully!');
                location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

// Update modal population
function populateUpdateModal(id) {
    fetch(`/admin_side/accommodations/${id}/`)
    .then(response => response.json())
    .then(data => {
        const form = document.getElementById('updateAccommodationForm');
        form.setAttribute('data-id', id);
        
        // Populate form fields
        form.querySelector('#update-name').value = data.name;
        form.querySelector('#update-address').value = data.address;
        form.querySelector('#update-price').value = data.price_per_night;
        form.querySelector('#update-description').value = data.description;
        form.querySelector('#update-contact').value = data.contact_number || '';
        form.querySelector('#update-email').value = data.email || '';
        form.querySelector('#update-website').value = data.website || '';
        form.querySelector('#update-rating').value = data.rating || '';

        // Handle amenities
        if (data.amenities) {
            const amenitiesCheckboxes = form.querySelectorAll('input[name="amenities[]"]');
            amenitiesCheckboxes.forEach(checkbox => {
                checkbox.checked = data.amenities.includes(checkbox.value);
            });
        }
    })
    .catch(error => console.error('Error:', error));
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
