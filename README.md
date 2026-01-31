# Cloudflare Stream Video Matcher

Script de automação desenvolvido em Python para cruzar bases de dados locais (CSV) com o catálogo de vídeos da API do Cloudflare Stream.

## 🚀 Funcionalidades

- **Consumo de API:** Busca e paginação automática de milhares de vídeos via API do Cloudflare.
- **Match Inteligente:** Algoritmo de normalização de texto que identifica vídeos mesmo com variações no nome (ex: remove sufixos de cópia, acentos e extensões).
- **Segurança de Dados:** Preenche apenas os dados faltantes, preservando IDs já existentes na base.
- **Relatórios:** Gera planilhas CSV atualizadas e arquivos de log com itens não encontrados.

## 🛠 Tecnologias

- Python 3
- Pandas (Manipulação de dados)
- Requests (Integração REST API)
- Regex & Unicodedata (Tratamento de Strings)

## 📦 Como usar

1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
Configure suas credenciais no main.py.

Coloque sua planilha na pasta inputs/.

Execute:

    ```bash
    python main.py
    ```