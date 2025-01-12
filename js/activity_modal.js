document.addEventListener('DOMContentLoaded', function() {
    const activityForm = document.querySelector('#addActivityForm');
    
    if (!activityForm) {
        console.error('Activity form not found');
        return;
    }

    activityForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        // Debug: Log form data
        console.log('Form Data:');
        for (let pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }

        fetch('/admin_side/admin_activity/add-activity/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                // Remove Content-Type header - browser will set it automatically with boundary
            }
        })
        .then(async response => {
            const text = await response.text();
            console.log('Raw server response:', text);
            
            try {
                const data = JSON.parse(text);
                if (!response.ok) {
                    throw new Error(data.message || 'Server error');
                }
                return data;
            } catch (e) {
                throw new Error('Invalid response: ' + text);
            }
        })
        .then(data => {
            if (data.success) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('addActivityModal'));
                modal.hide();
                activityForm.reset();
                window.location.reload();
            } else {
                alert('Error saving activity: ' + (data.message || ''));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error saving the activity. Please try again.');
        });
    });
});


function confirmDeletion(activityId) {
    if (confirm('Are you sure you want to delete this activity?')) {
        deleteActivity(activityId);
    }
}

function deleteActivity(activityId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/admin_side/admin_activity/delete/${activityId}/`, {
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
            const card = document.querySelector(`[data-id="${activityId}"]`).closest('.col-md-4');
            card.remove();
            
            // Show success message
            alert('Activity deleted successfully!');
            
            // Refresh the page to update the layout
            window.location.reload();
        } else {
            alert('Error deleting activity');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error deleting the activity. Please try again.');
    });
}

// Function to populate the update modal with activity data
function populateUpdateModal(activityId) {
    fetch(`/admin_side/admin_activity/get/${activityId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('updateActivityId').value = activityId;
            document.getElementById('updateName').value = data.name;
            document.getElementById('updateDescription').value = data.description;
            document.getElementById('updateCategory').value = data.category;
            document.getElementById('updateRating').value = data.rating;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading activity data');
        });
}

// Function to handle the update submission
function updateActivity() {
    const form = document.getElementById('updateActivityForm');
    const formData = new FormData(form);
    const activityId = document.getElementById('updateActivityId').value;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Check if we have a valid ID
    if (!activityId) {
        alert('Error: No activity ID found');
        return;
    }

    fetch(`/admin_side/admin_activity/update/${activityId}/`, {
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
            alert('Activity updated successfully!');
            
            // Refresh the page to show updated data
            window.location.reload();
        } else {
            alert('Error updating activity: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating activity');
    });
}

// Add event listener to update buttons when the document loads
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
    const searchInput = document.getElementById('searchActivity');

    const clearButton = document.getElementById('clearSearch');
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            const searchInput = document.getElementById('searchActivity');
            searchInput.value = '';
            performSearch('');
        });
    }

    
    if (!searchInput) {
        console.error('Search input not found');
        return;
    }

    // Debounce function to limit how often the search is performed
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

    // Function to perform the search
    function performSearch(searchTerm) {
        const activityCards = document.querySelectorAll('.col-md-4[data-id]');
        
        activityCards.forEach(card => {
            const title = card.querySelector('.card-title').textContent.toLowerCase();
            const category = card.querySelector('.badge').textContent.toLowerCase();
            const searchValue = searchTerm.toLowerCase();

            // Check if the search term is in the title or category
            if (title.includes(searchValue) || category.includes(searchValue)) {
                card.style.display = ''; // Show the card
            } else {
                card.style.display = 'none'; // Hide the card
            }
        });

        // Show "no results" message if needed
        const visibleCards = document.querySelectorAll('.col-md-4[data-id]:not([style*="display: none"])');
        const noResultsMsg = document.getElementById('noResultsMessage');
        
        if (visibleCards.length === 0 && searchTerm !== '') {
            if (!noResultsMsg) {
                const message = document.createElement('div');
                message.id = 'noResultsMessage';
                message.className = 'col-12 text-center mt-4';
                message.innerHTML = '<p class="text-muted">No activities found matching your search.</p>';
                document.querySelector('.row.mt-4').appendChild(message);
            }
        } else if (noResultsMsg) {
            noResultsMsg.remove();
        }
    }

    // Add event listener with debounce
    searchInput.addEventListener('input', debounce(function(e) {
        performSearch(e.target.value);
    }, 300));

    // Add clear search functionality
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Escape') {
            this.value = '';
            performSearch('');
        }
    });
});
