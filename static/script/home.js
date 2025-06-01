let listaDeCompras = [];

document.addEventListener("DOMContentLoaded", async function () {
    const authButton = document.getElementById("auth-button");
    const postButton = document.getElementById("post-button");

    const token = localStorage.getItem("token");

    if (token) {
        authButton.textContent = "Encerrar Sessão";
        authButton.classList.remove("btn-danger");
        authButton.classList.add("btn-secondary");

        authButton.addEventListener("click", function () {
            localStorage.removeItem("token");
            window.location.reload();
        });

        try {
            const response = await fetch("/me", {
                headers: { "Authorization": `Bearer ${token}` }
            });

            if (response.ok) {
                const user = await response.json();
                if (user.role === "creator") {
                    postButton.style.display = "block";
                }
            }
        } catch (error) {
            console.error("Erro ao verificar o usuário:", error);
        }

    } else {
        authButton.textContent = "Acessar Conta";
        authButton.classList.remove("btn-secondary");
        authButton.classList.add("btn-danger");

        authButton.addEventListener("click", function () {
            window.location.href = "/auth";
        });
    }

    document.getElementById("recipe-form").addEventListener("submit", async function(event) {
        event.preventDefault();

        const title = document.getElementById("title").value;
        const description = document.getElementById("description").value;
        const image_url = document.getElementById("image_url").value;
        const ingredients = document.getElementById("ingredients").value.split(',');

        try {
            const response = await fetch("/post-recipe", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ title, description, image_url, ingredients })
            });

            if (response.ok) {
                alert("Receita criada com sucesso!");
                document.getElementById("recipe-form").reset();
                const iframe = document.querySelector('iframe');
                iframe.src = iframe.src; 
                const modal = bootstrap.Modal.getInstance(document.getElementById('postRecipeModal'));
                modal.hide();
            } else {
                alert("Erro ao criar receita");
            }
        } catch (error) {
            console.error(error);
            alert("Erro de rede ao criar receita");
        }
    });
    adicionarListaComprasHome();
});


function adicionarListaComprasHome() {
    const lista = JSON.parse(localStorage.getItem('listaDeCompras')) || [];
    const ul = document.getElementById('listaCompras');

    // Limpa o conteúdo anterior
    ul.innerHTML = '';

    if (lista.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'Sua lista está vazia.';
        li.classList.add('list-group-item');
        ul.appendChild(li);
        return;
    }

    // Adiciona os itens com botão de remoção
    lista.forEach((item, index) => {
        const li = document.createElement('li');
        li.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');

        const itemText = document.createElement('span');
        itemText.textContent = item;

        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'Remover';
        removeBtn.classList.add('btn', 'btn-sm', 'btn-outline-danger');
        removeBtn.onclick = () => removerItemListaCompras(index);

        li.appendChild(itemText);
        li.appendChild(removeBtn);
        ul.appendChild(li);
    });
}

function removerItemListaCompras(index) {
    const lista = JSON.parse(localStorage.getItem('listaDeCompras')) || [];

    // Remove o item no índice especificado
    if (index >= 0 && index < lista.length) {
        lista.splice(index, 1);
        localStorage.setItem('listaDeCompras', JSON.stringify(lista));
        adicionarListaComprasHome(); // Atualiza a exibição
    }
}

function limparListaCompras() {
    localStorage.removeItem('listaDeCompras');
    adicionarListaComprasHome();
}