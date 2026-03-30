// =========================
// ESTADO GLOBAL
// =========================
let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
let session = JSON.parse(localStorage.getItem("session"));

// Productos por defecto
const productos = [
  {
    id: 1,
    nombre: "Mancuernas 10kg",
    precio: 19990,
    imagen: "https://via.placeholder.com/300"
  },
  {
    id: 2,
    nombre: "Pelota de fútbol",
    precio: 14990,
    imagen: "https://via.placeholder.com/300"
  },
  {
    id: 3,
    nombre: "Banda elástica",
    precio: 8990,
    imagen: "https://via.placeholder.com/300"
  }
];

// =========================
// UTILIDADES
// =========================
function guardarCarrito() {
    localStorage.setItem("carrito", JSON.stringify(carrito));
}

function cerrarSesion() {
    localStorage.removeItem("session");
    window.location.href = "login.html";
}

// =========================
// CATÁLOGO
// =========================
function renderProductos() {
    const container = document.getElementById("product-list");
    if (!container) return;

    container.innerHTML = "";

    productos.forEach(prod => {
        container.innerHTML += `
            <div class="col-12 col-md-6 col-lg-4 mb-4">
                <div class="card h-100">
                    <img src="${prod.imagen}" class="card-img-top">
                    <div class="card-body">
                        <h5 class="card-title">${prod.nombre}</h5>
                        <p class="card-text fw-bold text-danger">$${prod.precio}</p>
                        <button class="btn btn-primary" onclick="agregarAlCarrito(${prod.id})">
                            Agregar al carrito
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
}

// =========================
// CARRITO
// =========================
function agregarAlCarrito(id) {
    const producto = productos.find(p => p.id === id);
    const existe = carrito.find(p => p.id === id);

    if (existe) {
        existe.cantidad++;
    } else {
        carrito.push({ ...producto, cantidad: 1 });
    }

    guardarCarrito();
    alert("Producto agregado al carrito");
}

function eliminarProducto(index) {
    carrito.splice(index, 1);
    guardarCarrito();
    renderCarrito();
}

function cambiarCantidad(index, cantidad) {
    cantidad = parseInt(cantidad);

    if (cantidad <= 0 || isNaN(cantidad)) {
        eliminarProducto(index);
        return;
    }

    carrito[index].cantidad = cantidad;
    guardarCarrito();
    renderCarrito();
}

function renderCarrito() {
    const body = document.getElementById("cart-body");
    const totalEl = document.getElementById("total");

    if (!body) return;

    body.innerHTML = "";
    let total = 0;

    carrito.forEach((prod, index) => {
        let subtotal = prod.precio * prod.cantidad;
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
                    <button class="btn btn-danger btn-sm"
                        onclick="eliminarProducto(${index})">
                        X
                    </button>
                </td>
            </tr>
        `;
    });

    totalEl.innerText = "Total: $" + total;
}

// =========================
// CHECKOUT
// =========================
function renderCheckout() {
    const lista = document.getElementById("checkout-list");
    const totalEl = document.getElementById("checkout-total");

    if (!lista) return;

    lista.innerHTML = "";
    let total = 0;

    carrito.forEach(prod => {
        let subtotal = prod.precio * prod.cantidad;
        total += subtotal;

        lista.innerHTML += `
            <li class="list-group-item d-flex justify-content-between">
                ${prod.nombre} x${prod.cantidad}
                <span>$${subtotal}</span>
            </li>
        `;
    });

    totalEl.innerText = "Total: $" + total;
}

function finalizarCompra() {
    alert("Compra realizada con éxito");

    carrito = [];
    guardarCarrito();

    window.location.href = "index.html";
}

function irACheckout() {
    window.location.href = "checkout.html";
}

// =========================
// CONTROL DE ACCESO (BÁSICO)
// =========================
function verificarSesion() {
    // Si estás en páginas protegidas y no hay sesión
    const paginasProtegidas = ["cart.html", "checkout.html", "profile.html", "admin.html"];

    const ruta = window.location.pathname.split("/").pop();

    if (paginasProtegidas.includes(ruta) && !session) {
        window.location.href = "login.html";
    }

    // Si es admin y no tiene rol correcto
    if (ruta === "admin.html" && session && session.rol !== "admin") {
        alert("Acceso restringido");
        window.location.href = "index.html";
    }
}

function renderNavbar() {
    const nav = document.getElementById("nav-links");
    if (!nav) return;

    nav.innerHTML = "";

    // Siempre visible
    nav.innerHTML += `
        <li class="nav-item">
            <a class="nav-link" href="index.html">Productos</a>
        </li>
    `;

    if (!session) {
        // Usuario NO logueado
        nav.innerHTML += `
            <li class="nav-item">
                <a class="nav-link" href="login.html">Login</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="register.html">Registro</a>
            </li>
        `;
    } else {
        // Usuario logueado
        nav.innerHTML += `
            <li class="nav-item">
                <a class="nav-link" href="cart.html">Carrito</a>
            </li>

            <li class="nav-item">
                <a class="nav-link" href="profile.html">
                    ${session.nombre}
                </a>
            </li>
        `;

        // Si es admin
        if (session.rol === "admin") {
            nav.innerHTML += `
                <li class="nav-item">
                    <a class="nav-link text-warning" href="admin.html">
                        Admin
                    </a>
                </li>
            `;
        }

        // Cerrar sesión
        nav.innerHTML += `
            <li class="nav-item">
                <a class="nav-link text-danger" href="#" onclick="cerrarSesion()">
                    Cerrar sesión
                </a>
            </li>
        `;
    }
}

// =========================
// INICIALIZACIÓN
// =========================
verificarSesion();
renderProductos();
renderCarrito();
renderCheckout();
renderNavbar();