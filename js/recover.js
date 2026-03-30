const form = document.getElementById("recover-form");

if (form) {
    form.addEventListener("submit", function(e) {
        e.preventDefault();

        const emailInput = document.getElementById("recover-email");
        const email = emailInput.value;

        emailInput.classList.remove("is-valid", "is-invalid");

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            emailInput.classList.add("is-invalid");
            return;
        }

        const user = JSON.parse(localStorage.getItem("user"));

        if (!user || user.email !== email) {
            emailInput.classList.add("is-invalid");
            alert("El correo no está registrado");
            return;
        }

        emailInput.classList.add("is-valid");

        // Simulación
        alert("Se ha enviado un enlace de recuperación (simulado)");

        window.location.href = "login.html";
    });
}