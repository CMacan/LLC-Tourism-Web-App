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
function addRestaurant() {
    const restaurantData = {
      name: document.getElementById('add-name').value,
      pricePerNight: document.getElementById('add-price').value,
      address: document.getElementById('add-address').value,
      contactNumber: document.getElementById('add-contact').value,
      websiteURL: document.getElementById('add-website').value,
      rating: document.getElementById('add-rating').value,
      image: document.getElementById('add-image').value
    };
  
    fetch('/admin_side/restaurants/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(restaurantData)
    })
    .then(response => {
      if (response.headers.get('content-type').includes('application/json')) {
        return response.json();
      } else {
        throw new Error('Invalid JSON response');
      }
    })
    .then(data => {
      // Handle the successful response here
      console.log('Restaurant added successfully:', data);
      // Optionally, update the UI or show a success message
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle the error here, such as showing an error message to the user
    });
  }
  
  // Event listener for the "Add Restaurant" button
  document.getElementById('addRestaurantButton').addEventListener('click', addRestaurant);
  


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

// Delete confirmation
function confirmDeletion(id) {
    if (confirm('Are you sure you want to delete this restaurant?')) {
        fetch(`/admin_side/retaurants/${id}/delete/`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Restaurant deleted successfully!');
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
    fetch(`/admin_side/restaurants/${id}/`)
    .then(response => response.json())
    .then(data => {
        const form = document.getElementById('updateRestaurantForm');
        form.setAttribute('data-id', id);
        
        // Populate form fields
        form.querySelector('#update-name').value = data.name;
        form.querySelector('#update-address').value = data.address;
        form.querySelector('#update-price').value = data.price_per_night;
        form.querySelector('#update-contact').value = data.contact_number || '';
        form.querySelector('#update-website').value = data.website || '';
        form.querySelector('#update-rating').value = data.rating || '';
    
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
