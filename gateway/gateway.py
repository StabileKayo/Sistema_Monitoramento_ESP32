import socket
import threading

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


def main():
    print("Gateway rodando. Pressione Ctrl+C para encerrar.")


if __name__ == "__main__":
    main()