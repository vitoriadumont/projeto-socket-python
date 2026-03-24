import os
from colorama import Fore, init
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from datetime import datetime

init(autoreset=True)

HOST = "0.0.0.0"
PORT = 2120
USER = "user"
PASSWORD = "1234"
DIRETORIO = "ftp_files"

def log(msg):
    agora = datetime.now().strftime("%H:%M:%S")
    print(f"[{agora}] {msg}")

# Criar pasta base (se não existir)
os.makedirs(DIRETORIO, exist_ok=True)

authorizer = DummyAuthorizer()
authorizer.add_user(USER, PASSWORD, DIRETORIO, perm="elradfmw")

# Criando usuários 
usuarios = {
    "vitoria": "vitoria123",
    "bruna": "bruna123",
    "amanda": "amanda123"
}

for usuario, senha in usuarios.items():
    pasta_usuario = os.path.join(DIRETORIO, usuario)
    os.makedirs(pasta_usuario, exist_ok=True)
    authorizer.add_user(usuario, senha, pasta_usuario, perm="elradfmw")


# Criando usuário anônimo
authorizer.add_anonymous(DIRETORIO, perm="elr")

class MeuHandler(FTPHandler):

    def on_connect(self):
        log(Fore.LIGHTCYAN_EX + f"Conexão de {self.remote_ip}")

    def on_login(self, username):
        log(Fore.LIGHTGREEN_EX + f"Usuário '{username}' logado")

    def on_disconnect(self):
        log(Fore.RED + f"Usuário '{self.username}' desconectado")

handler = MeuHandler
handler.authorizer = authorizer

server = FTPServer((HOST, PORT), handler)

os.system('cls' if os.name == 'nt' else 'clear')

print(Fore.CYAN + "="*40)
print(Fore.CYAN + "             SERVIDOR FTP")
print(Fore.CYAN + "="*40 + "\n")
print(Fore.GREEN + "[✓] Servidor FTP iniciado" + "\n")
print(Fore.MAGENTA + f"Host: " + Fore.LIGHTBLUE_EX + f"{HOST}")
print(Fore.MAGENTA + f"Porta: " + Fore.LIGHTBLUE_EX + f"{PORT}")
print(Fore.MAGENTA + "Usuários cadastrados:" + Fore.LIGHTBLUE_EX + " Amanda | Bruna | Vitória" + "\n")
print()

log(Fore.YELLOW + "[i] Aguardando conexões...")

server.serve_forever()