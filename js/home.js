document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('search_input');
    const categorySelect = document.getElementById('category');
    const searchResults = document.getElementById('searchResults');
    const searchButton = searchForm.querySelector('.search-btn');
    let searchTimeout;

    // Handle form submission
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        performSearch();
    });

    // Handle input changes (with debounce)
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(performSearch, 500);
    });

    // Handle category changes
    categorySelect.addEventListener('change', performSearch);

    function performSearch() {
        const query = searchInput.value.trim();
        const category = categorySelect.value;

        if (query.length < 2) {
            searchResults.classList.add('d-none');
            return;
        }

        // Show loading state
        searchButton.classList.add('loading');
        searchButton.disabled = true;

        // Perform the search
        fetch(`/api/search/?q=${encodeURIComponent(query)}&category=${category}`)
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error('Search error:', error);
                showError();
            })
            .finally(() => {
                // Hide loading state
                searchButton.classList.remove('loading');
                searchButton.disabled = false;
            });
    }

    function displayResults(results) {
        searchResults.classList.remove('d-none');
        
        if (results.length === 0) {
            searchResults.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search fa-2x mb-3 text-muted"></i>
                    <p>No results found</p>
                </div>
            `;
            return;
        }

        searchResults.innerHTML = results.map(result => `
            <div class="result-item" onclick="navigateToResult('${result.url}')">
                <img src="${result.image || '/static/images/placeholder.jpg'}" 
                     alt="${result.title}" 
                     class="result-image">
                <div class="result-content">
                    <div class="result-title">${result.title}</div>
                    <div class="result-category">
                        <i class="fas fa-tag me-1"></i>${result.category}
                    </div>
                    <div class="result-description">${result.description}</div>
                </div>
            </div>
        `).join('');
    }

    function showError() {
        searchResults.classList.remove('d-none');
        searchResults.innerHTML = `
            <div class="no-results">
                <i class="fas fa-exclamation-circle fa-2x mb-3 text-danger"></i>
                <p>An error occurred while searching. Please try again.</p>
            </div>
        `;
    }

    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchForm.contains(e.target)) {
            searchResults.classList.add('d-none');
        }
    });
});

function navigateToResult(url) {
    window.location.href = url;
}