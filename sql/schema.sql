-- Cria o banco de dados usado pelo gateway

CREATE DATABASE IF NOT EXISTS monitoramento_iot;
USE monitoramento_iot;

-- Tabela onde cada leitura recebida (via TCP ou UDP) é armazenada
CREATE TABLE IF NOT EXISTS leituras(
	id INT AUTO_INCREMENT PRIMARY KEY,
    no_id VARCHAR(50) NOT NULL,
    protocolo VARCHAR(10) NOT NULL,
    timestamp_no DATETIME NOT NULL,                     -- momento em que o nó gerou a leitura
    recebido_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- momento em que o gateway recebeu
    temperatura FLOAT,
    umidade_ar FLOAT,
    umidade_solo FLOAT,
    
    -- acelera consultas filtrando por nó especifico ou por periodo de tempo
    INDEX idx_no_id(no_id),
    INDEX idx_recebido_em(recebido_em)
);