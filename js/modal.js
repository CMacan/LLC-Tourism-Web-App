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
