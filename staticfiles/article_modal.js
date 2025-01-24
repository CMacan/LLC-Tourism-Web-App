document.getElementById('addArticleForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('/admin_side/articles/create/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    })
    .catch(error => console.error('Error:', error));
});


document.getElementById('updateArticleForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const id = document.getElementById('updateArticleId').value;
    const formData = new FormData(this); // Use FormData directly

    fetch(`/admin_side/articles/${id}/update/`, {
        method: 'POST',
        body: formData, // Send the FormData directly
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            location.reload(); // Reload the page if successful
        } else {
            alert('Failed to update the article. Please check the input data.');
        }
    })
    .catch(error => console.error('Error:', error));
});

function populateUpdateModal(articleId) {
    // Fetch article data (if needed) or pass existing data
    const article = document.querySelector(`[data-id="${articleId}"]`);
    document.getElementById('updateArticleId').value = articleId;
    document.getElementById('updateTitle').value = article.querySelector('.card-title').innerText;
    document.getElementById('updateContent').value = 'Existing content'; // Adjust with actual data
    document.getElementById('updateAuthor').value = 'Existing author'; // Adjust with actual data
}


function deleteArticle(id) {
    if (confirm("Are you sure you want to delete this article?")) {
        fetch(`/admin_side/articles/${id}/delete/`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();
        })
        .catch(error => console.error('Error:', error));
    }
}
