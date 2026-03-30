const form = document.getElementById("profile-form");

if (form) {

    let session = JSON.parse(localStorage.getItem("session"));
    let user = JSON.parse(localStorage.getItem("user"));

    // Protección básica
    if (!session) {
        window.location.href = "login.html";
    }

    // Cargar datos
    document.getElementById("profile-nombre").value = user.nombre;
    document.getElementById("profile-email").value = user.email;

    form.addEventListener("submit", function(e) {
        e.preventDefault();

        const nombre = document.getElementById("profile-nombre");
        const password = document.getElementById("profile-password");
        const error = document.getElementById("profile-password-error");

        let valido = true;

        nombre.classList.remove("is-invalid", "is-valid");
        password.classList.remove("is-invalid", "is-valid");

        // Validar nombre
        if (nombre.value.trim() === "") {
            nombre.classList.add("is-invalid");
            valido = false;
        } else {
            nombre.classList.add("is-valid");
        }

        // Validar password solo si se ingresa
        if (password.value !== "") {

            let errores = [];

            if (password.value.length < 8) {
                errores.push("Mínimo 8 caracteres");
            }
            if (!/[A-Z]/.test(password.value)) {
                errores.push("Debe tener una mayúscula");
            }
            if (!/[0-9]/.test(password.value)) {
                errores.push("Debe tener un número");
            }
            if (!/[!@#$%^&*]/.test(password.value)) {
                errores.push("Debe tener un carácter especial");
            }

            if (errores.length > 0) {
                password.classList.add("is-invalid");
                error.innerText = errores.join(", ");
                valido = false;
            } else {
                password.classList.add("is-valid");
            }
        }

        if (!valido) return;

        // Guardar cambios
        user.nombre = nombre.value;

        if (password.value !== "") {
            user.password = password.value;
        }

        localStorage.setItem("user", JSON.stringify(user));
        localStorage.setItem("session", JSON.stringify(user));

        alert("Perfil actualizado correctamente");
    });
}