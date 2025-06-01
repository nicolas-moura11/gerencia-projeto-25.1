let listaDeCompras = [];
let todasReceitas = [];
let currentUserRole = null;
let receitaId = null; 

async function verificarUsuario() {
    const token = localStorage.getItem('token');

    if (token) {
        try {
            const response = await fetch('/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const user = await response.json();
                return { auth: true, role: user.role };
            }
        } catch (error) {
            console.error('Erro ao buscar dados do usuário:', error);
        }
    }
    return { auth: false, role: null };
}


async function carregarReceitas(userAuth, userRole) {
    document.getElementById('loading').style.display = 'block';
    const response = await fetch('/receitas');
    todasReceitas = await response.json();
    document.getElementById('loading').style.display = 'none';

    currentUserRole = userRole;

    todasReceitas.sort((a, b) => a.id - b.id);

    exibirReceitas(todasReceitas, currentUserRole);
}

function filtrarReceitas() {
    const query = document.getElementById('searchBar').value.toLowerCase();

    const termos = query.split(',').map(term => term.trim()).filter(term => term !== '');

    const receitasFiltradas = todasReceitas.filter(receita => {
        const tituloMatch = receita.title.toLowerCase().includes(query);

        const ingredientes = receita.ingredients.map(ing => ing.name.toLowerCase());

        const ingredientesMatch = termos.every(term =>
            ingredientes.some(ing => ing.includes(term))
        );

        return tituloMatch || ingredientesMatch;
    });

    exibirReceitas(receitasFiltradas, currentUserRole);
}

function exibirReceitas(receitas, userRole) {
    const container = document.getElementById('receitas');
    container.innerHTML = '';

    receitas.forEach((receita) => {
        const div = document.createElement('div');
        div.classList.add('col');

        const imageHTML = receita.image_url ?
            `<img src="${receita.image_url}" class="card-img-top img-fluid" style="height: 240px; object-fit: cover;" alt="${receita.title}">` :
            `<div class="card-img-top d-flex align-items-center justify-content-center text-secondary bg-light" style="height: 240px;">
                <i class="bi bi-image" style="font-size: 4rem;"></i>
            </div>`;

        const botoesHTML = `
            <div class="d-flex flex-wrap gap-2 align-items-center mt-auto pt-3 border-top">
                <button class="btn btn-primary btn-sm" type="button"
                    onclick="verPreparoComVerificacao('${receita.title.replace(/'/g, "\\'")}', \`${receita.description.replace(/`/g, '\\`')}\`)">
                    <i class="bi bi-book me-1"></i> Ver preparo
                </button>

                <button class="btn btn-success btn-sm" type="button"
                    onclick='salvarIngredientesNaLista(${JSON.stringify(receita.ingredients)})'>
                    <i class="bi bi-cart"></i> Adicionar à lista
                </button>

                <button id="btnCurtir-${receita.id}" class="btn btn-outline-danger btn-sm" onclick="curtirReceita(${receita.id})">
                    ❤️ <span id="qtdCurtidas-${receita.id}">${receita.likes || 0} </span>
                </button>
        

                ${userRole === "creator" ? `
                    <div class="dropdown">
                        <button class="btn btn-secondary btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Ações
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li>
                                <button class="dropdown-item text-danger" type="button"
                                    onclick="confirmarExclusao(${receita.id}, '${receita.title.replace(/'/g, "\\'")}')">
                                    <i class="bi bi-trash me-1"></i> Remover
                                </button>
                            </li>
                            <li>
                                <button class="dropdown-item" type="button"
                                    onclick="editarReceita(${receita.id})">
                                    <i class="bi bi-gear me-1"></i> Editar
                                </button>
                            </li>
                        </ul>
                    </div>` : ''
        }
            </div>
        `;

        div.innerHTML = `
            <div class="card h-100 shadow-sm rounded-3 overflow-hidden">
                ${imageHTML}
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title text-truncate mb-2">${receita.title}</h5>
                    
                    <p class="card-text text-muted small mb-3 flex-grow-1">
                        <strong class="text-dark">Ingredientes:</strong> ${receita.ingredients.map(i => i.name).join(', ')}
                    </p>

                    ${botoesHTML}
                </div>
            </div>
        `;

        container.appendChild(div);
    });
}


function abrirModal(titulo, descricao) {
    const modalTitle = document.getElementById('preparoModalLabel');
    const modalBody = document.getElementById('preparoModalBody');
    modalTitle.textContent = titulo;

    const passos = descricao
        .split(/\.\s+/)
        .filter(p => p.trim() !== '')
        .map(p => `<li>${p.trim()}.</li>`)
        .join('');

    modalBody.innerHTML = `<ol>${passos}</ol>`;
    const modal = new bootstrap.Modal(document.getElementById('preparoModal'));
    modal.show();
}

function mostrarToastLoginObrigatorio() {
    const toastEl = document.getElementById('loginToast');
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

async function verPreparoComVerificacao(titulo, descricao) {
    try {
        const response = await fetch('/auth/status', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const user = await response.json();

        if (user.is_authenticated) {
            abrirModal(titulo, descricao);
        } else {
            mostrarToastLoginObrigatorio();
        }
    } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
        mostrarToastLoginObrigatorio();
    }
}

function confirmarExclusao(id, nome) {
    receitaId = id; 
    document.getElementById('receitaParaExcluirNome').textContent = nome;
    const modal = new bootstrap.Modal(document.getElementById('modalConfirmDelete'));
    modal.show();
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('confirmarDeleteBtn').addEventListener('click', async () => {
        try {
            const response = await fetch(`/receitas/${receitaId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (response.ok) {
                const ModalElement = document.getElementById('modalConfirmDelete');
                const modalInstance = bootstrap.Modal.getInstance(ModalElement);
                if (modalInstance) modalInstance.hide(); 

                const toast = new bootstrap.Toast(document.getElementById('toastSucesso'));
                toast.show();

                const { auth, role } = await verificarUsuario();
                carregarReceitas(auth, role);
            } else {
                alert('Erro ao excluir a receita.');
            }
        } catch (err) {
            console.error('Erro na exclusão:', err);
            alert('Erro inesperado.');
        }
    });
});


let receitaEditando = null;
function editarReceita(id) {
    const receita = todasReceitas.find(r => r.id === id);
    if (!receita) return alert("Receita não encontrada.");

    document.getElementById('editarId').value = receita.id;
    document.getElementById('editarTitulo').value = receita.title;
    document.getElementById('editarIngredientes').value = receita.ingredients.map(i => i.name).join(', ');
    document.getElementById('editarDescricao').value = receita.description;
    document.getElementById('editarImagem').value = receita.image_url || '';

    const modal = new bootstrap.Modal(document.getElementById('modalEditarReceita'));
    modal.show();
}

async function handleSalvarAlteracoes() {
    const id = document.getElementById('editarId').value;
    const titulo = document.getElementById('editarTitulo').value.trim();
    const ingredientes = document.getElementById('editarIngredientes').value.split(',').map(i => i.trim());
    const descricao = document.getElementById('editarDescricao').value.trim();
    const imagem = document.getElementById('editarImagem').value.trim();

    try {
        const response = await fetch(`/receitas/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                title: titulo,
                ingredients: ingredientes,
                description: descricao,
                image_url: imagem
            })
        });

        if (!response.ok) {
            const erro = await response.json();
            console.error("Erro na atualização:", erro);
            return alert("Erro ao atualizar receita.");
        }

        const modalInstance = bootstrap.Modal.getInstance(document.getElementById('modalEditarReceita'));
        if (modalInstance) modalInstance.hide();

        const { auth, role } = await verificarUsuario();
        carregarReceitas(auth, role);

    } catch (err) {
        console.error("Erro inesperado:", err);
        alert("Erro inesperado ao atualizar.");
    }
}

function salvarIngredientesNaLista(ingredientes) {
    const listaAtual = JSON.parse(localStorage.getItem('listaDeCompras')) || [];
    const nomesAtuais = listaAtual.map(item => item.toLowerCase());

    ingredientes.forEach(ing => {
        const nome = ing.name.trim();
        if (!nomesAtuais.includes(nome.toLowerCase())) {
            listaAtual.push(nome);
        }
    });

    localStorage.setItem('listaDeCompras', JSON.stringify(listaAtual));

    const toast = new bootstrap.Toast(document.getElementById('toastListaCompras'));
    toast.show();
}


document.addEventListener('DOMContentLoaded', async () => {
    const { auth, role } = await verificarUsuario();
    carregarReceitas(auth, role);
});

async function curtirReceita(receitaId) {
    const token = localStorage.getItem('token');

    if (!token) {
        const toast = new bootstrap.Toast(document.getElementById('toastCurtidaReceita'));
        toast.show();
        return;
    }

    try {
        const response = await fetch(`/receitas/${receitaId}/curtir`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Erro ao curtir/descurtir a receita');
        }

        const data = await response.json();

        // Atualiza a contagem de curtidas na interface
        const span = document.getElementById(`qtdCurtidas-${receitaId}`);
        let atual = parseInt(span.textContent) || 0;

        if (data.curtido) {
            span.textContent = atual + 1;
        } else {
            span.textContent = Math.max(atual - 1, 0);
        }

    } catch (error) {
        console.error('Erro ao curtir receita:', error);
        alert('Não foi possível registrar a curtida. Tente novamente.');
    }
}
