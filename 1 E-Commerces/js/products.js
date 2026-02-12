// js/products.js

console.log("products.js loaded");

const API_URL = "http://127.0.0.1:5000/api/products";

document.addEventListener("DOMContentLoaded", () => {
  loadProducts();
});

function loadProducts() {
  fetch(API_URL)
    .then(response => response.json())
    .then(data => {
      console.log("API Response:", data);

      if (!data.success) {
        alert("Failed to load products");
        return;
      }

      const products = data.products;
      const container = document.getElementById("products");

      if (!container) {
        console.error("❌ products div not found in HTML");
        return;
      }

      container.innerHTML = "";

      if (products.length === 0) {
        container.innerHTML = "<p>No products found</p>";
        return;
      }

      products.forEach(p => {
        container.innerHTML += `
          <div class="product-card">
            <img src="${p.image || 'https://via.placeholder.com/150'}">
            <h3>${p.name}</h3>
            <p>₹${p.price}</p>
            <button onclick="viewProduct(${p.id})">View</button>
          </div>
        `;
      });
    })
    .catch(error => {
      console.error("❌ Fetch error:", error);
    });
}

function viewProduct(id) {
  window.location.href = `product_details.html?id=${id}`;
}
