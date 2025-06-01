document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");
    document.getElementById("reset-token").value = token;

    document.getElementById("reset-password-form").addEventListener("submit", async function(event) {
        event.preventDefault();

        const token = document.getElementById("reset-token").value;
        const newPassword = document.getElementById("reset-password").value;
        const confirmPassword = document.getElementById("reset-confirm-password").value;

        if (newPassword !== confirmPassword) {
            alert("As senhas não coincidem!");
            return;
        }

        try {
            const response = await fetch("/reset-password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ token: token, new_password: newPassword })
            });

            if (response.ok) {
                alert("Senha redefinida com sucesso!");
                window.location.href = "/auth";
            } else {
                const data = await response.json();
                alert(data.detail || "Erro ao redefinir a senha.");
            }
        } catch (error) {
            console.error("Erro ao redefinir a senha:", error);
            alert("Erro inesperado. Tente novamente.");
        }
    });
});