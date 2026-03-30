let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

// Renderizar carrito
function renderCarrito() {
    const body = document.getElementById("cart-body");
    body.innerHTML = "";

    let total = 0;

    carrito.forEach((prod, index) => {
        const subtotal = prod.precio * prod.cantidad;
        total += subtotal;

        body.innerHTML += `
            <tr>
                <td>${prod.nombre}</td>
                <td>$${prod.precio}</td>
                <td>
                    <input type="number" min="1" value="${prod.cantidad}" 
                        onchange="cambiarCantidad(${index}, this.value)">
                </td>
                <td>$${subtotal}</td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="eliminarProducto(${index})">
                        X
                    </button>
                </td>
            </tr>
        `;
    });

    document.getElementById("total").innerText = "Total: $" + total;
}

// Cambiar cantidad
function cambiarCantidad(index, cantidad) {
    carrito[index].cantidad = parseInt(cantidad);
    guardarCarrito();
    renderCarrito();
}

// Eliminar producto
function eliminarProducto(index) {
    carrito.splice(index, 1);
    guardarCarrito();
    renderCarrito();
}

// Guardar en localStorage
function guardarCarrito() {
    localStorage.setItem("carrito", JSON.stringify(carrito));
}

// Inicializar
renderCarrito();