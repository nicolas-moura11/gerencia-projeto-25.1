# gerencia-projeto-25.1

O Receita Fácil foi criado para ajudar usuários a encontrar rapidamente receitas para qualquer ocasião. Seja você um cozinheiro experiente ou alguém que está apenas começando, nosso objetivo é fornecer instruções claras e fáceis de seguir.

Como Utilizar?

Siga este guia passo a passo para rodar o projeto em sua máquina.

Passo 1: Baixar o Projeto e o Docker

Acesse o repositório do projeto no GitHub:

Link: https://github.com/nicolas-moura11/gerencia-projeto-25.1

Verifique se você está na branch main!

Clique no botão verde "< > Code" e depois em "Download ZIP".

Se você ainda não o tem, baixe e instale o Docker Desktop:

Link para Download: https://www.docker.com/products/docker-desktop/

Passo 2: Preparar o Ambiente

Abra o aplicativo Docker Desktop e deixe-o rodando em segundo plano.

Vá até o diretório onde você salvou o arquivo .zip e extraia o seu conteúdo.

Abra a pasta extraída (normalmente chamada gerencia-projeto-25.1-main) no seu ambiente de desenvolvimento preferido (como o VS Code).

Passo 3: Configurar o Banco de Dados

Dentro da pasta gerencia-projeto-25.1-main, crie um novo arquivo chamado exatamente ".env".

Abra este novo arquivo ".env" e cole o seguinte conteúdo nele:

DATABASE_URL=postgresql://postgres:admin123@db:5432/recipesDB

Passo 4: Executar a Aplicação

Usando o explorador de arquivos do seu computador, navegue para dentro da pasta gerencia-projeto-25.1-main.

Encontre o arquivo de auto-instalação chamado "start_app" e dê um duplo clique para executá-lo.

Atenção: É provável que seu sistema operacional exiba um alerta de segurança. Se isso acontecer, clique em "Mais informações" e depois em "Executar assim mesmo" (ou uma opção semelhante).

Um terminal (Prompt de Comando) será aberto e começará a instalar todas as dependências do projeto. Aguarde a finalização.

Ao final do processo, você verá a mensagem: "Voce pode acessar em:" seguida pelo link local do projeto.

Para acessar, você pode clicar diretamente no link no terminal ou usar Ctrl + Clique.

Pronto! Agora você já pode usufruir do nosso produto.

Criadores:
Nícolas Moura,
João Víctor Batista,
Ian Vasconcelos
