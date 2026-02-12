let cart = JSON.parse(localStorage.getItem("cart")) || [];

function addToCart(id) {
    cart.push(id);
    localStorage.setItem("cart", JSON.stringify(cart));
    alert("Added to cart");
}

const cartDiv = document.getElementById("cartItems");
if (cartDiv) {
    cartDiv.innerHTML = cart.map(i => `<p>Product ID: ${i}</p>`).join("");
}
