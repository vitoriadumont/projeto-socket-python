import socket
import threading
import hashlib
import os
from datetime import datetime


def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def registrar_log(texto):
    caminho_base = os.path.dirname(os.path.abspath(__file__))
    caminho_log = os.path.join(caminho_base, "log_chat.txt")

    with open(caminho_log, "a", encoding="utf-8") as arquivo:
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
admin_nome = "admin"


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

                if mensagem.startswith("/"):

                    if nome != admin_nome:
                        conn.send("status= Comando permitido apenas para admin.".encode(formato))
                        continue

                    if mensagem == "/online":
                        lista = ", ".join(nomes)
                        conn.send(f"status= Usuários online: {lista}".encode(formato))
                        continue

                    elif mensagem.startswith("/kick "):
                        alvo = mensagem.split(" ",1)[1]

                        if alvo in nomes:
                            index_alvo = nomes.index(alvo)
                            conn_alvo = clientes[index_alvo]

                            conn_alvo.send("status= Você foi removido pelo admin.".encode(formato))
                            registrar_log(f"{alvo} foi removido pelo admin.")

                            conn_alvo.close()
                            clientes.remove(conn_alvo)
                            nomes.remove(alvo)

                            conn.send(f"status= Usuário {alvo} removido.".encode(formato))
                        else:
                            conn.send("status= Usuário não encontrado.".encode(formato))

                        continue

                    elif mensagem == "/logs":
                        try:
                            caminho_base = os.path.dirname(os.path.abspath(__file__))
                            caminho_log = os.path.join(caminho_base, "log_chat.txt")

                            with open(caminho_log, "r", encoding="utf-8") as f:
                                ultimas = f.readlines()[-5:]
                                for linha in ultimas:
                                    conn.send(f"status= {linha.strip()}".encode(formato))

                        except:
                            conn.send("status= Erro ao ler logs.".encode(formato))

                        continue

                    else:
                        conn.send("status= Comando inválido.".encode(formato))
                        continue

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

if __name__ == "__main__":
    receber()