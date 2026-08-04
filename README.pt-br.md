# Open Brewery Data Pipeline

Uma pipeline ETL (Extract, Transform, Load) leve em Python para consumir dados da API Open Brewery DB, processá-los em um esquema estruturado e persistir em formatos analíticos.

🌐 *Leia isto em [English](README.md).* 

## Funcionalidades

- **Extração automatizada:** cliente HTTP resiliente que obtém dados da Open Brewery DB com retries automáticos e tratamento de falhas.
- **Transformação de dados:** limpa, sanitiza e aplica esquema às respostas brutas da API usando `pandas` DataFrames.
- **Persistência dupla:** exporta os resultados da pipeline simultaneamente para CSV e Parquet para consumo em ferramentas de BI (Power BI/Streamlit).
- **Testado por unit tests:** suíte de testes cobrindo requisições do cliente, regras de transformação, handlers de armazenamento e orquestração principal.

## Tecnologias e Conceitos Aplicados

- **Python 3.11+**
- **Pandas & PyArrow:** manipulação de dados, enforcement de esquema e serialização Parquet colunar.
- **Requests:** comunicação HTTP resiliente com gerenciamento customizado de erros.
- **Pytest:** cobertura de testes unitários e de integração.
- **Arquitetura limpa & PEP 8:** camadas desacopladas (client, cleaner, storage) com type hints e docstrings.

## Instalação e Uso

### Quickstart

Clone o repositório e entre na pasta do projeto:
```bash
git clone https://github.com/YOUR_USERNAME/open-brewery-pipeline.git
cd open-brewery-pipeline
```

### Criar e ativar um ambiente virtual

No Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

No Linux/macOS (Bash):
```bash
python -m venv .venv
source .venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar a pipeline ETL

```bash
python main.py
```

### Saída

Os conjuntos de dados processados serão gravados em `data/processed/`:

- `breweries_clean.csv` — CSV em `UTF-8-sig` para fácil importação no Excel/Power BI
- `breweries_clean.parquet` — Parquet colunar para consultas performáticas em BI

Dica: abra a pasta após a execução para verificar os arquivos gerados:

Windows PowerShell:
```powershell
explorer.exe .\data\processed
```

Linux/macOS:
```bash
xdg-open data/processed || open data/processed
```

## Testes

Execute a suíte de testes com `pytest`:

```bash
pytest
```

## Estrutura do projeto

```
open-brewery-pipeline/
├── data/
│   └── processed/         # Conjuntos de dados gerados (.csv, .parquet)
├── src/
│   ├── client.py          # Camada de interação com a API
│   ├── cleaner.py         # Rotinas de transformação de dados
│   └── storage.py         # Handlers de persistência em arquivo
├── tests/
│   ├── test_cleaner.py
│   ├── test_client.py
│   ├── test_main.py
│   └── test_storage.py
├── main.py                # Ponto de entrada da pipeline
├── requirements.txt
└── README.pt-br.md
```
