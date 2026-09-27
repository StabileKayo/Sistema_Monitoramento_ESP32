import json
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


def processar_mensagem(protocolo_esperado, linha_bytes, conexao, origem=""):
    # Faz o parse do JSON recebido e grava no banco, tratando erros sem derrubar o listener inteiro
    # Um pacote inválido de um nó não pode travar o recebimento dos demais
    try:
        mensagem = json.loads(linha_bytes.decode("utf-8"))
        salvar_leitura(conexao, mensagem)
        print(f"[{protocolo_esperado}{origem}] Gravado: {mensagem}")
    except json.JSONDecodeError:
        # Pacote corrompido ou não-JSON: registra e segue em frente
        print(f"[{protocolo_esperado}{origem}] Mensagem inválida (não era JSON): {linha_bytes!r}")
    except mysql.connector.Error as erro:
        # Falha no banco (conexão caiu, tabela errada, etc): registra sem derrubar o listener
        print(f"[{protocolo_esperado}{origem}] Erro ao gravar no MySQL: {erro}")        


def escutar_udp():
    conexao_db = conectar_banco()
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((UDP_HOST, UDP_PORT))
    print(f"[UDP] Escutando em {UDP_HOST}:{UDP_PORT}")

    # UDP não tem conceito de "conexão": cada datagrama é uma mensagem completa e independente
    # então basta receber e processar em loop
    while True:
        dados, endereco = servidor.recvfrom(1024)
        processar_mensagem("UDP", dados, conexao_db, origem=f" {endereco}")


def main():
    print("Gateway rodando. Pressione Ctrl+C para encerrar.")
    escutar_udp()


if __name__ == "__main__":
    main()