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
    const searchInput = document.getElementById('searchRestaurant');
    const clearButton = document.getElementById('clearSearch');

    if (!searchInput) {
        console.error('Search input not found');
        return;
    }

    // Function to perform the search
    function performSearch(searchTerm) {
        const restaurantCards = document.querySelectorAll('.col-md-4[data-id]');
        let hasResults = false;

        restaurantCards.forEach(card => {
            const name = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
            const address = card.querySelector('.text-muted')?.textContent.toLowerCase() || '';
            const searchValue = searchTerm.toLowerCase();

            if (name.includes(searchValue) || 
                address.includes(searchValue)) {
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
                noResultsMsg.innerHTML = '<p class="text-muted">No restaurant found matching your search.</p>';
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


// Function to add a new restaurant
function addRestaurant(e) {
    e.preventDefault();

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const restaurantData = new FormData(document.getElementById('addRestaurantForm'));

    fetch('/admin_side/restaurants/create/', {  // Make sure this matches your URL pattern
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            // Remove Content-Type header - let the browser set it with boundary for FormData
        },
        body: restaurantData,
        // Don't set Content-Type header when sending FormData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message || 'Something went wrong');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Restaurant added successfully:', data);
        // Close the modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addRestaurantModal'));
        modal.hide();
        
        // Show success message
        alert('Restaurant added successfully!');
        
        // Optionally reload the page or update the UI
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding restaurant: ' + error.message);
    });
}

// Event listener for the form
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('addRestaurantForm');
    if (form) {
        form.addEventListener('submit', addRestaurant);
    }
});


document.getElementById('updateRestaurantForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const id = this.getAttribute('data-id');
    const formData = new FormData(this);
    const jsonData = {};
    
    for (let [key, value] of formData.entries()) {
        if (key !== 'image') {
            jsonData[key] = value;
        }
    }
    
    formData.set('data', JSON.stringify(jsonData));
    
    fetch(`/admin_side/restaurants/${id}/update/`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Restaurant updated successfully!');
            location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

function deleteRestaurant(restaurantId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const restaurantCard = document.querySelector(`[data-id="${restaurantId}"]`);

    fetch(`/admin_side/restaurants/delete/${restaurantId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',  // Add this line
        },
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message || 'Something went wrong');
            });
        }
        return response.json();
    })
    .then(data => {
        // Remove the restaurant card with animation
        if (restaurantCard) {
            restaurantCard.style.opacity = '0';
            restaurantCard.style.transform = 'scale(0.9)';
            setTimeout(() => {
                restaurantCard.remove();
            }, 300);
        }
        
        // Show success message
        alert(data.message || 'Restaurant deleted successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting restaurant: ' + error.message);
    });
}

function confirmDeletion(restaurantId) {
    if (confirm('Are you sure you want to delete this restaurant?')) {
        deleteRestaurant(restaurantId);
    }
}

// Function to populate the update modal
// food_modal.js
function populateUpdateModal(restaurantId) {
    console.log("Fetching restaurant data for ID:", restaurantId);

    fetch(`/admin_side/restaurants/${restaurantId}/`)
        .then(response => response.json())
        .then(data => {
            console.log("Received data:", data);

            if (data.status === 'success' && data.restaurant) {
                const restaurant = data.restaurant;

                // Set the restaurant ID in the hidden field
                document.getElementById('update-restaurant-id').value = restaurant.id;
                
                // Populate other fields
                document.getElementById('update-name').value = restaurant.name || '';
                document.getElementById('update-address').value = restaurant.address || '';
                document.getElementById('update-facebook').value = restaurant.facebook || '';
                document.getElementById('update-instagram').value = restaurant.instagram || '';
                document.getElementById('update-website').value = restaurant.website || '';
                document.getElementById('update-rating').value = restaurant.rating || '0';

                // Handle image preview
                const currentImageDiv = document.getElementById('current-image');
                if (restaurant.image_url) {
                    currentImageDiv.innerHTML = `
                        <img src="${restaurant.image_url}" 
                             alt="Current image" 
                             class="img-thumbnail"
                             style="max-width: 200px; max-height: 200px;">
                        <p class="mt-2 text-muted">Current image will be kept if no new image is selected.</p>
                    `;
                } else {
                    currentImageDiv.innerHTML = '<p class="text-muted">No current image</p>';
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading restaurant data');
        });
}

// Handle form submission
document.getElementById('updateRestaurantForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const restaurantId = formData.get('restaurant_id'); // Get ID from hidden field
    
    console.log("Updating restaurant ID:", restaurantId); // Debug log

    if (!restaurantId) {
        console.error("No restaurant ID found");
        alert("Error: Restaurant ID is missing");
        return;
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/admin_side/restaurants/update/${restaurantId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Close the modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('updateModal'));
            modal.hide();
            
            // Show success message
            alert('Restaurant updated successfully!');
            
            // Reload the page
            window.location.reload();
        } else {
            throw new Error(data.message || 'Update failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating restaurant: ' + error.message);
    });
});

// Event listener for update button clicks
document.addEventListener('click', function(e) {
    const updateButton = e.target.closest('[data-bs-target="#updateModal"]');
    if (updateButton) {
        const restaurantId = updateButton.getAttribute('data-id');
        if (restaurantId) {
            console.log("Update button clicked for restaurant ID:", restaurantId);
            populateUpdateModal(restaurantId);
        } else {
            console.error("No restaurant ID found on update button");
        }
    }
});



