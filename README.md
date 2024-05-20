# pdf-extractor

Olá. Este é um pequeno projeto que realizei para o teste técnico de uma vaga de AI Engineer. O desafio é composto de duas partes:

- Criar uma API, em Python, que extraia os dados de um arquivo de faturamento em formato ```.pdf``` e retorne as informações mais relevantes.
- Formular uma arquitetura para resolver o mesmo desafio da parte 1, dessa vez utilizando RAG e LLMs. É um trabalho escrito, que você pode checar clicando [aqui](www.google.com).

Abaixo, você pode conferir o funcionamento da API, assim como todas as suas instruções de uso.

## Overview

Essa aplicação foi desenvolvida com base em 3 ferramentas principais:

- **FastAPI**: Uma biblioteca para construir, de forma rápida e eficiente, APIs em Python.
- **PDF Plumber**: Uma biblioteca para manipular e extrair informações de arquivos PDF de forma detalhada.
- **Regex**: Apesar de ser algo bem comum entre desenvolvedores, decidi citar o regex pela importância do mesmo na implementação do processo que identifica os dados a serem coletados.

### Estrutura do projeto

A escolha das ferramentas se deu para se alinhar Às descrições da vaga (Django e FastAPI). No final, nosso projeto ficou dividido entre os sequintes subdiretorios:

```pdf_processor/
├── app/
|   ├── utils/
|   |   ├── __init__.py
|   |   └── pdf_processor.py
│   ├── __init__.py
│   └── app.py
├── include/
|       └── pdfs/
|           └── index.pdf
├── .gitignore
├── requirements.txt
├── main.py
└── README.md
```

O arquivo main.py executa a API na porta escolhida. Ela só tem uma rota, denominada ```\process-pdf```. Ela tem uma restrição para apenas receber arquivos ```.pdf``` e, ao receber uma requisição, executa a função ```extract_pdf_data()```, definida no arquivo ```pdf_processor.py```.

### Desenvolvimento

Pela aplicação ser simples, a implementação da mesma também é simples. A maior parte do desenvolvimento ficou por parte da construção das funções de processamento de pdfs, que constam com várias nuances. Todo o sistema roda em um único projeto escrito 100% em python, enquanto a tipagem e as docstrings foram geradas pelo Github Copilot.

Durante as fases iniciais e de definição das funções de ```process_data```,  tudo foi escrito de forma monolítica. Após isso, refatorei o código para melhorar elegibilidade e eficiência, deixando cada parte do json de resposta sendo processado por uma única função, facilitando também futuras manutenções.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/samurai-py/pdf-processor.git
    cd pdf-processor
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/MacOS
    venv\Scripts\activate  # Para Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute a aplicação:
    ```bash
    python main.py
    ```

## Uso

Faça uma requisição POST para `/process-pdf` com um arquivo PDF. Por exemplo, usando `curl`:
```bash
curl -X POST "http://127.0.0.1:8000/process-pdf/" -F "file=@/your/path/to-file/index.pdf"
```