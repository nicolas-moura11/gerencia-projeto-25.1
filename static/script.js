document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-ingredientes");
    const resultado = document.getElementById("resultado");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const ingredientesSelecionados = Array.from(
            document.querySelectorAll('input[name="ingredientes"]:checked')
        ).map(cb => cb.value);

        const response = await fetch("/buscar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ ingredientes: ingredientesSelecionados })
        });

        const data = await response.json();
        resultado.innerHTML = `<p>Você buscou por: ${data.ingredientes.join(", ")}</p>`;
    });
});