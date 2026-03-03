import socket
import threading
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

port = 5050
servidor = "127.0.0.1"
addr = (servidor, port)
formato = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)


def mostrar_login():
    print(Fore.CYAN + "\n" + "="*35)
    print(Fore.CYAN + "        PROJETO SOCKET")
    print(Fore.CYAN + "="*35)
    print(Fore.CYAN + "            LOGIN")
    print(Fore.CYAN + "="*35 + "\n" + Style.RESET_ALL)

def enviar(mensagem):
    client.send(mensagem.encode(formato))

def handle_mensagens():
    while True:
        try:
            msg = client.recv(1024).decode()
            if not msg:
                continue

            if msg.startswith("status="):
                texto = msg.split("=",1)[1]
                print(Fore.GREEN + f"[SERVIDOR] {texto}" + Style.RESET_ALL)
            elif msg.startswith("msg="):
                partes = msg.split("=")
                print(f"{Fore.YELLOW}[{partes[3]}]{Style.RESET_ALL} "
                      f"{Fore.CYAN}{partes[1]}{Style.RESET_ALL}: {partes[2]}")
            elif msg.startswith("welcome="):
                texto = msg.split("=",1)[1]
                print(Fore.CYAN + "\n" + "="*40)
                print(Fore.CYAN + f"  {texto}")
                print(Fore.CYAN + "="*40 + "\n" + Style.RESET_ALL)
        except:
            print(Fore.RED + "[!] Conexão encerrada pelo servidor." + Style.RESET_ALL)
            break

def enviar_mensagem():
    while True:
        mensagem = input(Fore.YELLOW + "Digite sua mensagem: " + Style.RESET_ALL)
        enviar("msg=" + mensagem)

def enviar_nome():
    mostrar_login()
    

    nome = input(Fore.CYAN + 'Digite seu usuário: ' + Style.RESET_ALL)
    enviar(f"Nome={nome}")


    msg = client.recv(1024).decode()
    if msg.startswith("auth="):
        print(Fore.CYAN + msg.split("=",1)[1] + Style.RESET_ALL)


    senha = input(Fore.CYAN + 'Digite sua senha: ' + Style.RESET_ALL)
    enviar(f"Senha={senha}")


    msg = client.recv(1024).decode()
    if msg.startswith("auth="):
        print(Fore.GREEN + msg.split("=",1)[1] + Style.RESET_ALL)


    msg = client.recv(1024).decode()
    if msg.startswith("welcome="):
        texto = msg.split("=",1)[1]
        print(Fore.CYAN + "\n" + "="*40)
        print(Fore.CYAN + f"  {texto}")
        print(Fore.CYAN + "="*40 + "\n" + Style.RESET_ALL)


def iniciar():
    enviar_nome()  

    thread = threading.Thread(target=handle_mensagens, daemon=True)
    thread.start()
    enviar_mensagem() 

iniciar()