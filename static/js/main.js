document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    const suggestionsDiv = document.getElementById('suggestions');

    // Function to clear suggestions
    function clearSuggestions() {
        suggestionsDiv.innerHTML = '';
    }

    // Function to add suggestion to the DOM
    function addSuggestion(suggestion) {
        const div = document.createElement('div');
        div.textContent = suggestion;
        div.className = 'suggestion-item'; // Use this class for styling your suggestions
        div.addEventListener('click', function() {
            searchInput.value = suggestion; // Fill input with suggestion on click
            clearSuggestions(); // Clear suggestions after selection
        });
        suggestionsDiv.appendChild(div);
    }

    // Event listener for input to fetch suggestions
    searchInput.addEventListener('input', function() {
        console.log("event listened")
        const keyword = this.value.trim();
        if (keyword === '') {
            clearSuggestions();
            return;
        }

        fetch(`http://localhost:8000/suggestions?keyword=${encodeURIComponent(keyword)}`)
            .then(response => response.json())
            .then(data => {
                clearSuggestions(); // Clear existing suggestions before adding new ones
                data.forEach(addSuggestion);
            })
            .catch(error => console.error('Error fetching suggestions:', error));
    });
});