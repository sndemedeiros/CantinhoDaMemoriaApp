# 🌸 Cantinho da Memória 🌸

## Descrição
O Cantinho da Memória é um aplicativo interativo desenvolvido com Streamlit, projetado para ajudar você a registrar e organizar momentos especiais. Guarde lembretes, anote ideias importantes e salve memórias com fotos, tudo em um só lugar.

## Funcionalidades
- **Sistema de Usuários:** Crie sua conta ou faça login para ter acesso seguro às suas informações.
- **Lembretes:** Crie lembretes com tarefas e horários, com opções de repetição (diária, semanal, mensal).
- **Notas:** Anote pensamentos, ideias e informações importantes, com registro de data e hora.
- **Memórias com Fotos:** Registre lembranças especiais com um título, descrição e uma foto (opcional), armazenadas de forma segura.
- **Persistência de Dados:** Todas as informações são salvas no Firebase Firestore, garantindo que suas memórias estejam sempre seguras.
- **Armazenamento de Imagens:** As fotos são armazenadas no Cloudinary.

## Acessar o Aplicativo Online
Você pode acessar e usar o Cantinho da Memória diretamente pelo navegador aqui:
[Link para o seu App no Streamlit Community Cloud](https://cantinhodamemoria.streamlit.app/)

## Tecnologias Utilizadas
- **Python**
- **Streamlit:** Para a interface de usuário interativa.
- **Firebase Authentication:** Para gerenciamento de usuários.
- **Firebase Firestore:** Para o banco de dados das memórias, notas e lembretes.
- **Cloudinary:** Para armazenamento e gerenciamento das imagens.

## Como Rodar Localmente (Para Desenvolvedores)
Se você deseja rodar este projeto em sua máquina local:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/sndemedeiros/CantinhoDaMemoriaApp.git](https://github.com/sndemedeiros/CantinhoDaMemoriaApp.git)
    cd CantinhoDaMemoriaApp
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure suas chaves secretas:** Crie a pasta `.streamlit` e o arquivo `secrets.toml` dentro dela. Preencha-o com suas chaves do Firebase e Cloudinary, conforme o formato esperado pelo Streamlit.
5.  **Execute o aplicativo:**
    ```bash
    streamlit run app.py
    ```

## Autor
Desenvolvido por: [Suzana Medeiros/Usuário do GitHub]
