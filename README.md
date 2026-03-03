# Projeto Socket - Cliente/Servidor em Python

## Descrição

Este projeto consiste em uma aplicação cliente-servidor desenvolvida em Python utilizando sockets TCP.

O sistema permite múltiplos usuários conectados simultaneamente, com autenticação por usuário e senha, controle administrativo e registro de logs.

O objetivo do projeto é aplicar conceitos de redes de computadores, concorrência com threads e segurança básica.


## Funcionalidades

- Comunicação via TCP
- Múltiplos clientes simultâneos (threads)
- Sistema de autenticação com hash (SHA-256)
- Modo administrador
- Comandos administrativos:
  - `/online` → lista usuários conectados
  - `/kick nome` → remove usuário
  - `/logs` → exibe últimos registros
- Registro de logs em arquivo
- Demonstração de vulnerabilidade via interceptação de tráfego


## Segurança

As senhas não são armazenadas em texto puro.

O sistema utiliza o algoritmo SHA-256 para gerar o hash das senhas antes de armazená-las.

Isso garante proteção no armazenamento das credenciais.

A comunicação não utiliza criptografia TLS, portanto pode ser interceptada.


## Tecnologias Utilizadas

- Python 3
- Socket (TCP)
- Threading
- Hashlib (SHA-256)
- Wireshark (para análise de tráfego)
- Git e GitHub (versionamento)