CREATE TABLE IF NOT EXISTS movimentacoes (
    id SERIAL PRIMARY KEY,
    data_movimentacao DATE,
    valor NUMERIC(15,2),
    descricao VARCHAR(255)
);

-- Coluna extra para evitar transações duplicadas quando há FITID.
ALTER TABLE movimentacoes ADD COLUMN IF NOT EXISTS fitid VARCHAR(255);
CREATE UNIQUE INDEX IF NOT EXISTS idx_movimentacoes_fitid
ON movimentacoes (fitid);

-- Consultar as movimentações.
SELECT * FROM movimentacoes ORDER BY data_movimentacao, id;

-- Conferir os totais.
SELECT
    SUM(CASE WHEN valor > 0 THEN valor ELSE 0 END) AS total_entradas,
    SUM(CASE WHEN valor < 0 THEN ABS(valor) ELSE 0 END) AS total_saidas,
    SUM(valor) AS saldo_calculado
FROM movimentacoes;
