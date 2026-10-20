from ofxparse import OfxParser
import os
from pathlib import Path

# O arquivo extrato.ofx deve ficar na mesma pasta deste programa.
arquivo_ofx = Path(__file__).parent / "extrato.ofx"

with open(arquivo_ofx, "rb") as arquivo:
    ofx = OfxParser.parse(arquivo)

transacoes = ofx.account.statement.transactions
entradas = 0
saidas = 0

print("\n========== EXTRATO BANCÁRIO ==========\n")

for t in transacoes:
    data = t.date.strftime("%d/%m/%Y")
    valor = float(t.amount)
    descricao = t.memo or "Sem descrição"

    print(f"Data: {data}")
    print(f"Valor: R$ {valor:.2f}")
    print(f"Descrição: {descricao}")
    print("--------------------------------------")

    if valor > 0:
        entradas += valor
    else:
        saidas += valor

saldo = entradas + saidas

print("\n============= RESUMO =============")
print(f"Quantidade de movimentações: {len(transacoes)}")
print(f"Total de entradas: R$ {entradas:.2f}")
print(f"Total de saídas: R$ {abs(saidas):.2f}")
print(f"Saldo calculado: R$ {saldo:.2f}")

# Parte extra: salva no PostgreSQL se as variáveis de conexão estiverem configuradas.
if os.getenv("DB_NAME") and os.getenv("DB_USER") and os.getenv("DB_PASSWORD"):
    try:
        import psycopg2

        conexao = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id SERIAL PRIMARY KEY,
                data_movimentacao DATE,
                valor NUMERIC(15,2),
                descricao VARCHAR(255)
            )
        """)
        cursor.execute("ALTER TABLE movimentacoes ADD COLUMN IF NOT EXISTS fitid VARCHAR(255)")
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_movimentacoes_fitid
            ON movimentacoes (fitid)
        """)

        novas = 0
        for t in transacoes:
            fitid = getattr(t, "id", None)
            if fitid:
                cursor.execute("""
                    INSERT INTO movimentacoes (data_movimentacao, valor, descricao, fitid)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (fitid) DO NOTHING
                """, (t.date.date(), t.amount, (t.memo or "Sem descrição")[:255], str(fitid)))
            else:
                cursor.execute("""
                    INSERT INTO movimentacoes (data_movimentacao, valor, descricao)
                    VALUES (%s, %s, %s)
                """, (t.date.date(), t.amount, (t.memo or "Sem descrição")[:255]))
            novas += cursor.rowcount

        conexao.commit()
        cursor.close()
        conexao.close()
        print(f"\nMovimentações novas salvas no PostgreSQL: {novas}")

    except ImportError:
        print("\nPara usar o PostgreSQL, instale as bibliotecas do requirements.txt.")
    except Exception as erro:
        print(f"\nNão foi possível salvar no PostgreSQL: {erro}")
else:
    print("\nPostgreSQL não configurado. A leitura do OFX foi feita normalmente.")
