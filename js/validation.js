// Obtener formulario
const form = document.getElementById("register-form");

if (form) {
    form.addEventListener("submit", function(e) {
        e.preventDefault();

        let valido = true;

        const nombre = document.getElementById("nombre");
        const email = document.getElementById("email");
        const password = document.getElementById("password");
        const confirmPassword = document.getElementById("confirm-password");
        const passwordError = document.getElementById("password-error");

        // Reset clases
        [nombre, email, password, confirmPassword].forEach(input => {
            input.classList.remove("is-valid", "is-invalid");
        });

        // =========================
        // NOMBRE
        // =========================
        if (nombre.value.trim() === "") {
            nombre.classList.add("is-invalid");
            valido = false;
        } else {
            nombre.classList.add("is-valid");
        }

        // =========================
        // EMAIL
        // =========================
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email.value)) {
            email.classList.add("is-invalid");
            valido = false;
        } else {
            email.classList.add("is-valid");
        }

        // =========================
        // PASSWORD (4 validaciones)
        // =========================
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
            passwordError.innerText = errores.join(", ");
            valido = false;
        } else {
            password.classList.add("is-valid");
        }

        // =========================
        // CONFIRMAR PASSWORD
        // =========================
        if (password.value !== confirmPassword.value || confirmPassword.value === "") {
            confirmPassword.classList.add("is-invalid");
            valido = false;
        } else {
            confirmPassword.classList.add("is-valid");
        }

        // =========================
        // RESULTADO FINAL
        // =========================
        if (valido) {
            alert("Registro exitoso");

            // Simulación de guardado
            let user = {
                 nombre: nombre.value,
                email: email.value,
                password: password.value,
                rol: document.getElementById("rol").value
            };

            localStorage.setItem("user", JSON.stringify(user));

            window.location.href = "login.html";
        }
    });
}