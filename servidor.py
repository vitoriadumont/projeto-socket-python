import socket
import threading
import hashlib
from datetime import datetime


def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def registrar_log(texto):
    with open("log_chat.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(texto + "\n")


usuarios = {
    "vitoria": gerar_hash("dumont123"),
    "amanda": gerar_hash("oliveira123"),
    "bruna": gerar_hash("santana123"),
    "admin": gerar_hash("admin123")
}

port = 5050
servidor = "127.0.0.1"
addr = (servidor, port)

formato = 'utf-8'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(addr)
server.listen()
print(f"[SERVIDOR] Rodando em {servidor}:{port}")

clientes = []
nomes = []


def broadcast(mensagem):
    for cliente in clientes:
        cliente.send(mensagem.encode(formato))


def handle_cliente(conn):
    while True:
        try:
            msg = conn.recv(1024).decode(formato)
            if msg.startswith("msg="):
                mensagem = msg.split("=",1)[1]
                index = clientes.index(conn)
                nome = nomes[index]

                hora = datetime.now().strftime("%H:%M:%S")
                mensagem_formatada = f"msg={nome}={mensagem}={hora}"

                registrar_log(f"{hora} - {nome}: {mensagem}")
                broadcast(mensagem_formatada)
                conn.send("status= Sua mensagem foi recebida com sucesso!".encode(formato))

        except:
            
            if conn in clientes:
                index = clientes.index(conn)
                nome = nomes[index]
                registrar_log(f"{nome} desconectou.")
                clientes.remove(conn)
                nomes.pop(index)
                conn.close()
            break


def receber():
    while True:
        conn, addr = server.accept()
        print(f"[NOVA CONEXÃO] {addr}")


        nome_msg = conn.recv(1024).decode(formato).strip()
        if nome_msg.startswith("Nome="):
            nome = nome_msg.split("=",1)[1].strip()

            if nome not in usuarios:
                conn.send("auth= Usuário não cadastrado.".encode(formato))
                registrar_log("Usuário não cadastrado.")
                conn.close()
                continue

            conn.send("auth= Digite sua senha:".encode(formato))
            senha_msg = conn.recv(1024).decode(formato).strip()
            if not senha_msg.startswith("Senha="):
                conn.send("auth= Formato de senha inválido. Conexão encerrada.".encode(formato))
                registrar_log("Formato de senha inválido. Conexão encerrada.")
                conn.close()
                continue

            senha = senha_msg.split("=",1)[1].strip()
            if usuarios[nome] == gerar_hash(senha):
                conn.send("auth= Usuário autenticado com sucesso!".encode(formato))
                nomes.append(nome)
                clientes.append(conn)
                registrar_log(f"{nome} conectou.")
                conn.send(f"welcome=Bem-vindo(a), {nome}!".encode(formato))
                thread = threading.Thread(target=handle_cliente, args=(conn,))
                thread.start()
            else:
                conn.send("auth= Senha incorreta. Conexão encerrada.".encode(formato))
                registrar_log("Senha incorreta. Conexão encerrada.")
                conn.close()

receber()