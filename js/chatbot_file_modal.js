document.addEventListener('DOMContentLoaded', function() {
    const chatbot_fileForm = document.querySelector('#addChatbotFileForm');
    
    if (!chatbot_fileForm) {
        console.error('Chatbot file form not found');
        return;
    }

    chatbot_fileForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        // Debug: Log form data
        console.log('Form Data:');
        for (let pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }

        fetch('/admin_chatbot_file/add-chatbot_file/', {
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
                const modal = bootstrap.Modal.getInstance(document.getElementById('addChatbotFileModal'));
                modal.hide();
                chatbot_fileForm.reset();
                window.location.reload();
            } else {
                alert('Error saving chatbot file: ' + (data.message || ''));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error saving the chatbot file. Please try again.');
        });
    });
});


function confirmDeletion(chatbot_fileId) {
    if (confirm('Are you sure you want to delete this chatbot file?')) {
        deletechatbot_file(chatbot_fileId);
    }
}

function deletechatbot_file(chatbot_fileId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/admin_chatbot_file/delete/${chatbot_fileId}/`, {
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
            const card = document.querySelector(`[data-id="${chatbot_fileId}"]`).closest('.col-md-4');
            card.remove();
            
            // Show success message
            alert('Chatbot File deleted successfully!');
            
            // Refresh the page to update the layout
            window.location.reload();
        } else {
            alert('Error deleting chatbot file');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error deleting the chatbot file. Please try again.');
    });
}


document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchFile');

    const clearButton = document.getElementById('clearSearch');
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            const searchInput = document.getElementById('searchFile');
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
        const chatbot_fileCards = document.querySelectorAll('.col-md-4[data-id]');
        
        chatbot_fileCards.forEach(card => {
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
