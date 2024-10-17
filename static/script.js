// Perform search function
function performSearch() {
    const searchInput = document.getElementById('searchInput').value.trim();
    if (searchInput === '') {
        alert('Please enter a search query!');
        return false;
    }

    document.getElementById('searchResults').innerHTML = 'Loading results...';

    // Execute search across all engines through Flask API
    fetch(`/search?query=${encodeURIComponent(searchInput)}`)
        .then(response => response.json())
        .then(results => {
            displayResults(results);
        })
        .catch(error => {
            console.error('Error during search:', error);
            document.getElementById('searchResults').innerHTML = 'Error fetching results.';
        });

    return false; // Prevent form submission
}

// Display search results on the page
function displayResults(allResults) {
    const searchResultsDiv = document.getElementById('searchResults');
    searchResultsDiv.innerHTML = ''; // Clear previous results

    if (allResults.length === 0) {
        searchResultsDiv.innerHTML = '<p>No results found.</p>';
        return;
    }

    allResults.forEach(result => {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';

        resultItem.innerHTML = `
            <h2><a href="${result.url}" target="_blank">${result.title}</a></h2>
            <p>${result.description}</p>
        `;

        searchResultsDiv.appendChild(resultItem);
    });
}
