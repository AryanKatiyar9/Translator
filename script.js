function search() {
    const searchBar = document.getElementById("search-bar");
    const category = document.getElementById("categories").value;
    const results = document.getElementById("result-list");

    // Clear existing results
    results.innerHTML = "";

    // Example search results
    const sampleResults = [
        { name: "Fresh Mart", category: "grocery" },
        { name: "Tech World", category: "electronics" },
        { name: "Fashion Hub", category: "clothing" }
    ];

    const query = searchBar.value.toLowerCase();
    const filteredResults = sampleResults.filter(
        result => 
            (result.name.toLowerCase().includes(query) || query === "") &&
            (result.category === category || category === "all")
    );

    if (filteredResults.length > 0) {
        filteredResults.forEach(result => {
            const listItem = document.createElement("li");
            listItem.textContent = result.name;
            results.appendChild(listItem);
        });
    } else {
        results.innerHTML = "<li>No results found</li>";
    }
}