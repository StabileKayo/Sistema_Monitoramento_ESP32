import socket
import threading

import mysql.connector

# Dados de conexão com o banco MySQL onde as leituras serão armazenadas
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "monitoramento_iot",
}

# Endereços e portas em que o gateway vai escutar cada protocolo.
# 0.0.0.0  significa "aceita conexões de qualquer interface de rede"

UDP_HOST = "0.0.0.0"
UDP_PORT = 5001


def conectar_banco():
    # Abre uma nova conexão com o MySQL. Cada thread chama isso uma vez,
    # pois conexões do mysql-connector não são seguras para uso concorrente
    return mysql.connector.connect(**DB_CONFIG)


def salvar_leitura(conexao, mensagem: dict):
    # Insere uma leitura na tabela "leituras". Usa .get() em vez de acesso direto
    # para não quebrar caso algum campo venha faltando na mensagem
    sql = """
        INSERT INTO leituras
            (no_id, protocolo, timestamp_no, temperatura, umidade_ar, umidade_solo)
        VALUES
            (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        mensagem.get("no_id"),
        mensagem.get("protocolo"),
        mensagem.get("timestamp"),
        mensagem.get("temperatura"),
        mensagem.get("umidade_ar"),
        mensagem.get("umidade_solo"),
    )
    cursor = conexao.cursor()
    cursor.execute(sql, valores)
    conexao.commit()
    cursor.close()


def main():
    print("Gateway rodando. Pressione Ctrl+C para encerrar.")


if __name__ == "__main__":
    main()