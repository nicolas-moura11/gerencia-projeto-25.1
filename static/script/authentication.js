document.getElementById("forgot-password-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const email = document.getElementById("forgot-email").value;

    try {
        const response = await fetch("/forgot-password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert(data.message || "Link de recuperação enviado para o e-mail fornecido.", false);
            bootstrap.Modal.getInstance(document.getElementById('ForgotPasswordModal')).hide();
        } else {
            showAlert(data.detail || "Erro ao enviar o link de recuperação.", true);
        }
    } catch (error) {
        console.error("Erro ao enviar o link de recuperação:", error);
        showAlert("Erro inesperado. Tente novamente.", true);
    }
});

document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch("/token", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
            "username": username,
            "password": password
        })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        window.location.href = "/home";
    } else {
        showAlert("Erro no login. Tente novamente.", true);
    }
});

document.getElementById("register-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const username = document.getElementById("register-username").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const confirmedPassword = document.getElementById("register-confirm-password").value;
    const role = document.getElementById("register-role").value;

    if (password !== confirmedPassword) {
        showAlert("As senhas não são iguais!", true);
        return;
    }

    try {
        const response = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                role: role 
            })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert(data.message || "Registrado com sucesso!", false);
        } else {
            showAlert(data.detail || "Credencial já cadastrada, tente novamente!", true);
        }
    } catch (error) {
        console.error("Erro ao registrar:", error);
        showAlert("Ocorreu um erro ao tentar registrar. Tente novamente.", true);
    }
});

function showAlert(message, isError = false) {
    const alertMessage = document.getElementById("alert-message");
    const alertContainer = document.getElementById("alert-container");

    alertMessage.textContent = message;
    alertMessage.className = isError ? "alert alert-danger" : "alert alert-success";
    alertContainer.style.display = "block";

    setTimeout(() => {
        alertContainer.style.display = "none";
    }, 5000);
}