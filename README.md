Sistema de Transferência de Arquivos com FTP

Este projeto foi desenvolvido para a disciplina de Redes de Computadores e tem como objetivo implementar um sistema de transferência de arquivos utilizando o protocolo FTP em Python.

O sistema permite que usuários se conectem a um servidor FTP, naveguem entre diretórios e realizem transferências de arquivos entre cliente e servidor.

Tecnologias utilizadas
Python
Biblioteca pyftpdlib para criação do servidor FTP
Biblioteca ftplib para implementação do cliente FTP
Biblioteca colorama para melhorar a interface no terminal
Estrutura do projeto
projeto_ftp
│
├── servidor.py
├── cliente.py
│
└── ftp_files
    ├── vitoria
    ├── bruna
    └── amanda

Cada usuário possui um diretório próprio dentro da pasta ftp_files, garantindo organização e isolamento dos arquivos.

Funcionamento do sistema

O sistema é dividido em duas partes principais:

Servidor FTP

Responsável por:

criar e gerenciar usuários
autenticar conexões
armazenar arquivos enviados pelos clientes
controlar permissões de acesso
registrar conexões no terminal

O servidor utiliza a biblioteca pyftpdlib para implementar o protocolo FTP.

Cliente FTP

O cliente foi desenvolvido em Python utilizando a biblioteca ftplib e funciona através de um terminal interativo.

O usuário pode:

conectar ao servidor
navegar entre diretórios
enviar arquivos
baixar arquivos
visualizar arquivos disponíveis no servidor
Comandos disponíveis no cliente
Comando	Função
dir	Lista arquivos do diretório atual
cd pasta	Navega para um diretório
get arquivo	Baixa um arquivo do servidor
put arquivo	Envia um arquivo para o servidor
pwd	Mostra o diretório atual
mkdir pasta	Cria um diretório
help	Mostra os comandos disponíveis
quit	Encerra a conexão com o servidor

## Como executar o projeto
1️⃣ Instalar dependências
pip install pyftpdlib colorama
2️⃣ Iniciar o servidor
python servidor.py

## O servidor iniciará em:

Host: 0.0.0.0
Porta: 2120

3️⃣ Executar o cliente
python cliente.py
Usuários disponíveis
Usuário	Senha
vitoria	vitoria123
bruna	bruna123
amanda	amanda123

Cada usuário possui uma pasta própria no servidor.

Funcionalidades implementadas
Servidor FTP utilizando pyftpdlib
Autenticação de usuários
Criação automática de diretórios
Navegação entre pastas
Upload de arquivos
Download de arquivos
Interface de terminal com cores
Listagem de arquivos no servidor
Autoras

Projeto desenvolvido por:

Vitória
Bruna
Amanda

Disciplina: Redes de Computadores