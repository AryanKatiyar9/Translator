fetch("/products")
  .then(response => response.json())
  .then(data => {
    const categories = document.getElementById("categories");
    categories.innerHTML = ""; // Clear existing content
    data.forEach(product => {
      const categoryDiv = document.createElement("div");
      categoryDiv.classList.add("category");
      categoryDiv.innerHTML = `
        <h3>${product.name}</h3>
        <p>${product.description}</p>
        <button onclick="addToCart()">Add to Cart</button>
      `;
      categories.appendChild(categoryDiv);
    });
  });
