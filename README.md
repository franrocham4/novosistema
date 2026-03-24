# NovoSistema - Dashboard de Controle de Pagamentos 2025

Sistema Django multi-módulo que lê automaticamente a planilha `CONTROLEDEPAGAMENTO2025.xlsm` e exibe os dados em um Dashboard interativo.

## Módulos

- **Dashboard Principal** – KPIs, gráficos e resumo executivo
- **Liquidação 2025** – Aba "LIQUIDAÇÃO 2025" com totais e filtros
- **Alteração Orçamentária** – Aba "ALT. ORÇ. E PROJ." com programa/projeto/ficha
- **Empenho** – Aba "EMPENHO" com saldos e liquidações

## Requisitos

- Python 3.10+
- pip

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/franrocham4/novosistema.git
cd novosistema

# 2. Crie e ative o ambiente virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o banco de dados
python manage.py migrate

# 5. (Opcional) Crie um superusuário para o painel admin
python manage.py createsuperuser

# 6. Execute o servidor
python manage.py runserver
```

Acesse: **http://localhost:8000**

## Configuração do arquivo Excel

O sistema lê o arquivo Excel automaticamente do caminho padrão:

```
C:\Users\danielcoelho\Desktop\Pasta\novosistema\CONTROLEDEPAGAMENTO2025.xlsm
```

Para alterar o caminho, defina a variável de ambiente `EXCEL_FILE_PATH`:

```bash
# Windows (PowerShell)
$env:EXCEL_FILE_PATH = "C:\outro\caminho\CONTROLEDEPAGAMENTO2025.xlsm"
python manage.py runserver

# Linux/Mac
EXCEL_FILE_PATH="/caminho/do/arquivo.xlsm" python manage.py runserver
```

O sistema também busca automaticamente o arquivo `CONTROLEDEPAGAMENTO2025.xlsm` na pasta raiz do projeto como alternativa.

## Exportação

Cada módulo possui botão de exportação CSV disponível na interface.

## API REST

- `GET /liquidacao/api/` – Dados de liquidação em JSON
- `GET /contratos/api/` – Dados de alterações orçamentárias em JSON
- `GET /empenho/api/` – Dados de empenho em JSON

## Stack

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5 + Chart.js
- **Banco de Dados**: SQLite
- **Leitura Excel**: openpyxl
