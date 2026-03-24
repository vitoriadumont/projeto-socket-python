from ftplib import FTP, error_perm
import os
import getpass
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

os.system('cls' if os.name == 'nt' else 'clear')

HOST = "127.0.0.1"
PORT = 2120

# =========================
# CONTROLE BIN + HASH
# =========================
modo_binario = True
modo_hash = False

def mostrar_progresso(bloco):
    if modo_hash:
        print("#", end="", flush=True)

def mostrar_banner():
    print(Fore.CYAN + "="*45)
    print(Fore.CYAN + "               CLIENTE FTP")
    print(Fore.CYAN + "="*45)
    print(Fore.LIGHTGREEN_EX + "    Servidor:", HOST, "| " + Fore.LIGHTGREEN_EX + "Porta:", PORT)
    print(Fore.CYAN + "="*45 + Style.RESET_ALL + "\n")

mostrar_banner()

USER = input(Fore.MAGENTA + "Digite o nome de usuário: " + Style.RESET_ALL).strip()
PASSWORD = getpass.getpass(Fore.MAGENTA + "Digite a senha: " + Style.RESET_ALL)

ftp = FTP()

print(Fore.LIGHTYELLOW_EX + "[i] Conectando ao servidor FTP...\n")
ftp.connect(HOST, PORT)
ftp.login(USER, PASSWORD)

print(Fore.LIGHTGREEN_EX + f"[✓] Usuário '{USER}' conectado ao servidor FTP com sucesso!\n")
print(Fore.LIGHTCYAN_EX + "-> Digite " + Fore.LIGHTBLUE_EX + "help" + Fore.LIGHTCYAN_EX + " para visualizar os comandos disponíveis!\n")

while True:
    comando = input(Fore.YELLOW + f"{ftp.pwd()} ftp> " + Style.RESET_ALL).strip().lower()

    # LISTAR
    if comando == "dir":
        try:
            print(Fore.CYAN + "Listando arquivos no diretório atual:")
            ftp.retrlines('LIST')
            print(Fore.CYAN + "Fim da lista de arquivos." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[X] Erro ao listar arquivos: {e}")

    # CD
    elif comando.startswith("cd "):
        pasta = comando[3:].strip()
        if pasta == USER:
            print(Fore.YELLOW + "\n[i] Você já está no seu diretório pessoal.")
        else:
            try:
                ftp.cwd(pasta)
                print(Fore.GREEN + f"Diretório atual: {ftp.pwd()}")
            except Exception as e:
                print(Fore.RED + f"[X] Erro ao mudar de diretório: {e}")

    # =========================
    # GET (COM HASH + ERROR)
    # =========================
    elif comando.startswith("get "):
        arquivo = comando[4:].strip()
        try:
            with open(arquivo, 'wb') as f:
                print(Fore.CYAN + "Baixando arquivo...")
                ftp.retrbinary(f'RETR {arquivo}', lambda bloco: (f.write(bloco), mostrar_progresso(bloco)))
            print("\n" + Fore.GREEN + f"Arquivo '{arquivo}' baixado com sucesso!")
        except error_perm as e:
            print(Fore.RED + f"[X] Erro de permissão: {e}")
        except Exception as e:
            print(Fore.RED + f"[X] Erro ao baixar arquivo: {e}")

    # =========================
    # PUT (COM HASH + ERROR)
    # =========================
    elif comando.startswith("put "):
        arquivo = comando[4:].strip()
        if os.path.isfile(arquivo):
            try:
                with open(arquivo, 'rb') as f:
                    nome = os.path.basename(arquivo)
                    print(Fore.CYAN + "Enviando arquivo...")
                    ftp.storbinary(f'STOR {nome}', f, callback=mostrar_progresso)
                print("\n" + Fore.GREEN + f"Arquivo '{arquivo}' enviado com sucesso!")
            except error_perm as e:
                print(Fore.RED + f"[X] Erro de permissão: {e}")
            except Exception as e:
                print(Fore.RED + f"[X] Erro ao enviar arquivo: {e}")
        else:
            print(Fore.RED + f"[X] Arquivo '{arquivo}' não encontrado.")

    # =========================
    # HASH
    # =========================
    elif comando == "hash":
        modo_hash = not modo_hash
        status = "ativado" if modo_hash else "desativado"
        print(Fore.GREEN + f"[✓] Modo HASH {status}")

    # =========================
    # BIN
    # =========================
    elif comando == "bin":
        modo_binario = True
        print(Fore.GREEN + "[✓] Modo binário ativado")

    # HELP
    elif comando == "help":
        print(Fore.LIGHTCYAN_EX + "\n=============== Comandos disponíveis: ==============\n")
        print(Fore.MAGENTA + "  dir           -> Listar arquivos no diretório atual")
        print(Fore.MAGENTA + "  cd pasta      -> Mudar diretório")
        print(Fore.MAGENTA + "  get arquivo   -> Baixar arquivo")
        print(Fore.MAGENTA + "  put arquivo   -> Enviar arquivo")
        print(Fore.MAGENTA + "  hash          -> Mostrar progresso (#)")
        print(Fore.MAGENTA + "  bin           -> Ativar modo binário")
        print(Fore.MAGENTA + "  pwd           -> Diretório atual")
        print(Fore.MAGENTA + "  mkdir pasta   -> Criar diretório")
        print(Fore.MAGENTA + "  quit          -> Sair")
        print(Fore.LIGHTCYAN_EX + "\n==================================================" + Style.RESET_ALL)

    # PWD
    elif comando == "pwd":
        try:
            print(Fore.GREEN + f"Diretório atual: {ftp.pwd()}")
        except Exception as e:
            print(Fore.RED + f"[X] Erro: {e}")

    # MKDIR
    elif comando.startswith("mkdir "):
        nova_pasta = comando[6:].strip()
        try:
            ftp.mkd(nova_pasta)
            print(Fore.GREEN + f"Diretório '{nova_pasta}' criado com sucesso!")
        except Exception as e:
            print(Fore.RED + f"[X] Erro ao criar diretório: {e}")

    # =========================
    # QUIT MELHORADO
    # =========================
    elif comando == "quit":
        print(Fore.LIGHTYELLOW_EX + "Desconectando do servidor FTP...")
        try:
            ftp.quit()
        except Exception:
            ftp.close()
        print(Fore.CYAN + "Desconectado com sucesso. Até logo!")
        break

    else:
        print(Fore.RED + "[X] Comando não reconhecido. Tente novamente.")

    agora = datetime.now().strftime("%H:%M:%S")
    print(Fore.BLUE + f"\n[{agora}] Comando executado: {comando}\n" + Style.RESET_ALL)

    # Fim