document.getElementById('addArticleForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    
    console.log('Submitting article with data:');
    for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }

    fetch('/admin_articles/create/', {  
        method: 'POST',
        body: formData,
    })
    .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Network response was not ok');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.message) {
            alert(data.message);
            const modal = bootstrap.Modal.getInstance(document.getElementById('addArticleModal'));
            modal.hide();
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message || 'An unexpected error occurred. Please try again.');
    });
});


document.addEventListener('DOMContentLoaded', function() {

    $('#tags').select2({
        placeholder: 'Select tags',
        allowClear: true
    });
});


document.getElementById('updateArticleForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const id = document.getElementById('updateArticleId').value;
    const formData = new FormData(this);

    // Debug log
    console.log('Updating article ID:', id);
    console.log('Form data contents:');
    for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }

    fetch(`/admin_articles/${id}/update/`, {  // Make sure this URL matches your urls.py
        method: 'POST',
        body: formData,
    })
    .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Server error occurred');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Success response:', data);
        if (data.message) {
            alert(data.message);
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error details:', error);
        alert('Error updating article: ' + error.message);
    });
});


function populateUpdateModal(articleId) {

    const article = document.querySelector(`[data-id="${articleId}"]`);
    document.getElementById('updateArticleId').value = articleId;
    document.getElementById('updateTitle').value = article.querySelector('.card-title').innerText;
    document.getElementById('updateContent').value = 'Existing content'; // Adjust with actual data
    document.getElementById('updateAuthor').value = 'Existing author'; // Adjust with actual data
}


function deleteArticle(id) {
    if (confirm("Are you sure you want to delete this article?")) {
        fetch(`/admin_articles/${id}/delete/`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();
        })
        .catch(error => console.error('Error:', error));
    }
}
