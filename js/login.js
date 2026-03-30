const form = document.getElementById("login-form");

if (form) {
    form.addEventListener("submit", function(e) {
        e.preventDefault();

        const email = document.getElementById("login-email").value;
        const password = document.getElementById("login-password").value;

        const user = JSON.parse(localStorage.getItem("user"));

        if (!user) {
            alert("No hay usuario registrado");
            return;
        }

        if (email === user.email && password === user.password) {
            localStorage.setItem("session", JSON.stringify(user));

            alert("Login exitoso");

            // Redirección según rol
            if (user.rol === "admin") {
                window.location.href = "admin.html";
            } else {
                window.location.href = "index.html";
            }

        } else {
            alert("Credenciales incorrectas");
        }
    });
}