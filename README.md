# Projeto OFX

Atividade de Python para ler um extrato bancário no formato OFX.

## O que o programa faz

- Mostra a data, o valor e a descrição de cada movimentação.
- Mostra a quantidade de movimentações.
- Calcula o total de entradas, saídas e o saldo.
- Tem uma parte extra para salvar as movimentações no PostgreSQL.
- Evita gravar novamente uma movimentação que tenha o mesmo FITID.

## Como executar no Windows

1. Coloque seu arquivo `extrato.ofx` nesta pasta, junto do `main.py`.
2. Abra o terminal nesta pasta.
3. Crie e ative o ambiente virtual:

```powershell
python -m venv venv
venv\Scripts\activate
```

4. Instale as bibliotecas e execute:

```powershell
pip install -r requirements.txt
python main.py
```

## Parte extra: PostgreSQL

1. Abra o arquivo `schema.sql` no DBeaver e execute os comandos no banco desejado.
2. No terminal do VS Code, configure a conexão. Troque `SUA_SENHA` pela senha do usuário PostgreSQL:

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="postgres"
$env:DB_USER="postgres"
$env:DB_PASSWORD="SUA_SENHA"
python main.py
```

3. Para conferir os dados no DBeaver, execute:

```sql
SELECT * FROM movimentacoes;
```

## Importante

O arquivo OFX pode conter informações bancárias pessoais, por isso ele não foi enviado para este repositório público. Coloque seu próprio arquivo `extrato.ofx` na pasta antes de executar. Não publique senhas ou extratos reais no GitHub.
