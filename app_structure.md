# Estrutura do Aplicativo Streamlit RPG Character Sheet

Esta é a estrutura de diretórios e arquivos sugerida para o aplicativo.

```
/
|-- app.py                     # Arquivo principal da aplicação Streamlit
|-- requirements.txt           # Dependências do projeto (streamlit)
|-- README.md                  # Descrição geral do projeto
|
|-- pages/                     # Diretório para as páginas da aplicação
|   |-- 1_➕_Create_Character.py # Página para criação de um novo personagem
|   `-- 2_📝_Edit_Character.py   # Página para carregar e editar uma ficha de personagem existente
|
|-- src/                       # Código fonte principal da aplicação
|   |-- __init__.py            # Inicializador do pacote src
|   |-- character.py           # Módulo para gerenciar a lógica e os dados do personagem
|   |-- components.py          # Módulo para componentes de UI reutilizáveis (ex: formulário de edição)
|   `-- utils.py               # Funções utilitárias (ex: manipulação de arquivos, download de template)
|
|-- templates/                 # Diretório para armazenar templates de arquivos
|   `-- character_sheet_template.md # Template da ficha de personagem em markdown
|
|-- characters/                # (Opcional) Diretório para salvar as fichas de personagens criadas
```

### Descrição dos Arquivos:

*   **`app.py`**: Ponto de entrada da aplicação. Irá conter a página inicial, talvez com uma breve descrição, e a navegação principal para as outras páginas.
*   **`pages/1_➕_Create_Character.py`**: Conterá o formulário para o usuário inserir os dados de um novo personagem. Ao final, permitirá o download da ficha em formato markdown.
*   **`pages/2_📝_Edit_Character.py`**: Esta página terá duas funções principais:
    1.  Permitir o upload de um arquivo `.md` de uma ficha de personagem.
    2.  Uma vez carregada, exibir os dados em um formulário editável para que o usuário possa fazer alterações (registrar sucessos, adicionar perícias, etc.) e baixar a versão atualizada.
    3.  Também pode incluir um botão para baixar um template vazio.
*   **`src/character.py`**: Definirá a estrutura de dados de um personagem (possivelmente uma classe `Character`) e os métodos para converter essa estrutura para e de uma string markdown.
*   **`src/components.py`**: Funções que criam widgets ou seções de UI reutilizáveis. Por exemplo, uma função `display_character_sheet(character)` que recebe um objeto de personagem e o exibe de forma bonita e editável no Streamlit.
*   **`src/utils.py`**: Funções de ajuda, como:
    *   `generate_markdown(character)`: Gera a string markdown a partir de um objeto de personagem.
    *   `parse_markdown(file_content)`: Extrai os dados de um arquivo markdown para um objeto de personagem.
    *   `create_download_link()`: Lógica para criar os botões de download dos arquivos.
*   **`templates/character_sheet_template.md`**: Um arquivo markdown pré-formatado que servirá como base para novas fichas e para o download do template.
*   **`characters/`**: Um lugar para armazenar as fichas geradas, se a aplicação precisar persistir os dados no lado do servidor. Para o escopo inicial, pode não ser necessário se o foco for apenas upload/download.
