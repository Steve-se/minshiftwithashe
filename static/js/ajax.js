document.addEventListener("DOMContentLoaded", function() {
    function fetchFilteredContent(params) {
        fetch(`?${params}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update the content of your containers
            document.getElementById("articles-container").innerHTML = data.articles_html;
            document.getElementById("vlogs-container").innerHTML = data.vlogs_html;
        })
        .catch(error => console.error('Error:', error));
    }

    // Example event listener for a category link
    document.querySelectorAll(".category-link").forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            const category = this.dataset.category;
            fetchFilteredContent(`category=${category}`);
        });
    });
});
