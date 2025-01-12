document.addEventListener('DOMContentLoaded', function() {
    const destinationForm = document.querySelector('#addDestinationModal form');
    
    if (!destinationForm) {
        console.error('Destination form not found');
        return;
    }

    destinationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/admin_side/admin_destination/add-destination/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Close the modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('addDestinationModal'));
                modal.hide();
                
                // Show success message
                alert('Destination added successfully!');
                
                // Reset the form
                destinationForm.reset();
                
                // Refresh the page
                window.location.reload();
            } else {
                alert('Error saving destination');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error saving the destination. Please try again.');
        });
    });
});

function confirmDeletion(destinationId) {
    if (confirm('Are you sure you want to delete this destination?')) {
        deleteDestination(destinationId);
    }
}

function deleteDestination(destinationId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/admin_side/admin_destination/delete/${destinationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Find and remove the card
            const card = document.querySelector(`[data-id="${destinationId}"]`).closest('.col-md-4');
            card.remove();
            
            // Show success message
            alert('Destination deleted successfully!');
            
            // Refresh the page to update the layout
            window.location.reload();
        } else {
            alert('Error deleting destination');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error deleting the destination. Please try again.');
    });
}

// Function to populate the update modal with destination data
function populateUpdateModal(destinationId) {
    fetch(`/admin_side/admin_destination/get/${destinationId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('updateDestinationId').value = destinationId; // Set the ID
            document.getElementById('updateName').value = data.name;
            document.getElementById('updateLocation').value = data.location;
            document.getElementById('updateDescription').value = data.description;
            document.getElementById('updateCategory').value = data.category;
            document.getElementById('updateRating').value = data.rating;
            document.getElementById('updatePopular').checked = data.popular;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading destination data');
        });
}

// Function to handle the update submission
// Function to populate the update modal with destination data
function populateUpdateModal(destinationId) {
    fetch(`/admin_side/admin_destination/get/${destinationId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('updateDestinationId').value = destinationId;
            document.getElementById('updateName').value = data.name;
            document.getElementById('updateLocation').value = data.location;
            document.getElementById('updateDescription').value = data.description;
            document.getElementById('updateCategory').value = data.category;
            document.getElementById('updateRating').value = data.rating;
            document.getElementById('updatePopular').checked = data.popular;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading destination data');
        });
}

// Function to handle the update submission
function updateDestination() {
    const form = document.getElementById('updateDestinationForm');
    const formData = new FormData(form);
    const destinationId = document.getElementById('updateDestinationId').value;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Check if we have a valid ID
    if (!destinationId) {
        alert('Error: No destination ID found');
        return;
    }

    fetch(`/admin_side/admin_destination/update/${destinationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Close the modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('updateModal'));
            modal.hide();
            
            // Show success message
            alert('Destination updated successfully!');
            
            // Refresh the page to show updated data
            window.location.reload();
        } else {
            alert('Error updating destination: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating destination');
    });
}

// Add event listener to update buttons when the document loads
document.addEventListener('DOMContentLoaded', function() {
    const updateButtons = document.querySelectorAll('[data-bs-target="#updateModal"]');
    updateButtons.forEach(button => {
        button.addEventListener('click', function() {
            const destinationId = this.getAttribute('data-id');
            if (destinationId) {
                populateUpdateModal(destinationId);
            } else {
                console.error('No destination ID found on button');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const updateButtons = document.querySelectorAll('[data-bs-target="#updateModal"]');
    updateButtons.forEach(button => {
        button.addEventListener('click', function() {
            const activityId = this.getAttribute('data-id');
            if (activityId) {
                populateUpdateModal(activityId);
            } else {
                console.error('No activity ID found on button');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Get the search input and clear button elements
    const searchInput = document.getElementById('searchDestination');
    const clearButton = document.getElementById('clearSearch');

    // Function to filter destinations
    function filterDestinations() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        const destinationCards = document.querySelectorAll('.col-md-4.mb-3[data-id]');
        let hasResults = false;

        destinationCards.forEach(card => {
            const name = card.querySelector('.card-title').textContent.toLowerCase().trim();
            const category = card.querySelector('.badge').textContent.toLowerCase().trim();
            const location = card.querySelector('.card-text.text-muted').textContent.toLowerCase().trim();

            if (name.includes(searchTerm) || 
                category.includes(searchTerm) || 
                location.includes(searchTerm)) {
                card.style.display = 'block';
                hasResults = true;
            } else {
                card.style.display = 'none';
            }
        });

        // Handle no results message
        handleNoResults(hasResults, searchTerm);
    }

    // Function to handle "No results" message
    function handleNoResults(hasResults, searchTerm) {
        let noResultsMessage = document.getElementById('no-results-message');
        
        if (!hasResults && searchTerm !== '') {
            if (!noResultsMessage) {
                noResultsMessage = document.createElement('div');
                noResultsMessage.id = 'no-results-message';
                noResultsMessage.className = 'col-12 text-center mt-3';
                noResultsMessage.innerHTML = `
                    <div class="alert alert-info">
                        No destinations found matching "${searchTerm}"
                    </div>`;
                document.querySelector('.row.mt-4').appendChild(noResultsMessage);
            }
        } else if (noResultsMessage) {
            noResultsMessage.remove();
        }
    }

    // Function to clear search
    function clearSearch() {
        searchInput.value = '';
        filterDestinations();
        searchInput.focus();
    }

    // Debounce function to improve performance
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

    // Event listeners
    if (searchInput) {
        // Real-time search with debounce
        searchInput.addEventListener('input', debounce(() => {
            filterDestinations();
        }, 300));

        // Handle Enter key
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                filterDestinations();
            }
        });

        // Handle Escape key
        searchInput.addEventListener('keyup', (e) => {
            if (e.key === 'Escape') {
                clearSearch();
            }
        });
    }

    // Clear button functionality
    if (clearButton) {
        clearButton.addEventListener('click', clearSearch);
    }
});





