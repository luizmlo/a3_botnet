### A3 - Botnets

Este é um repositório onde vou documentar todo o processo de pesquisa e desenvolvimento de uma botnet do zero com python, websockets e asyncio, com o objetivo de aprender networking e redes, programação assincrona e outros conceitos.  

Esta botnet será apresentada como demonstração durante a apresentação do trabalho de conclusão da matéria de Sistemas Computacionais e Segurança.  

O tema escolhido pelo meu grupo foi o de Botnets, uma coleção de tecnologias utilizada para controlar de maneira distribuida um exercito de dispositivos infectados, podendo gerar muitos impactos com o grande poder de processamento e geração de tráfego.

#

### Indice
- [**Resumo do Projeto**](#resumo-do-projeto)
  - [C2](#c2)
  - [Zumbi](#zumbi)
  - [Vitima](#vitima)
- [**Protocolos de Rede**](#protocolos-de-rede)
  - [Handshake](#handshake)
  - [Heartbeat](#heartbeat)
- [**Pacotes de Rede**](#pacotes-de-rede)
  - [handshake_ping](#handshake_ping)
  - [handshake_pong](#handshake_pong)
  - [handshake_success](#handshake_success)
  - [heartbeat_ping](#heartbeat_ping)
  - [heartbeat_pong](#heartbeat_pong)
- [**Setup**](#setup)
  - [Dependencias](#dependencias)
  - [Instalação](#instalação)
    - [Linux/Unix](#linuxunix)
  - [Executando](#executando)
  
[**Setup**](#setup)

#

<a name="resumo"></a>

## **Resumo do Projeto**

Este projeto vai ser complexo e contará com diversas partes, entre elas um servidor de controle que comandará os *zumbis*, um frontend malicioso que infecta as vítimas e um site que vai ser a vítima da botnet, sofrendo um ataque de DDoS durante a apresentação ao vivo.

#

<a name="c2"></a>

### C2

> O servidor de controle  

Este será um servidor feito em python utilizando as bibliotecas asyncio e websocket que irá fazer a gestão, controle e monitoramento dos zumbis.

Este será responsável por manter uma espécie de Heartbeat, um pulso que irá checar a conexão de todos os zumbis e enviar uma mensagem para todos os zumbis que não estão conectados ou perderam a conexão com o servidor de controle.

O servidor de c2 será responsável também por enviar o comando de ataque e parada para os zumbis, que irão agir de maneira coordenada e sobrecarregar a vítima, causando um ataque distribuido de negação de serviço, um ataque de DDoS.

#

<a name="zumbi"></a>

### Zumbi

> O frontend malicioso

![](https://i.imgur.com/KAzrLa3.png)

Esta é a aplicação web onde as vítimas irão se conectar e se comunicar com o servidor de controle, aguardando ordens de ataques utilizando a tecnologia de websockets.

Os clientes conectados respondem um pulso enviado a cada segundo pelo servidor de controle para provar que ainda estão conectados e ativos, esperando o comando e o alvo do ataque.

#

<a name="vitima"></a>

### Vitima

> A vítima do ataque distribuido

Este será um servidor de demonstração que irá sofrer o ataque coordenado da botnet e será sobrecarregado, tendo sua funcionalidade prejudicada pelos zumbis.  

Este irá contar com uma interface de monitoramento, onde iremos observar ao vivo o estado da vitima, quantas requisições estão chegando, a quantidade de banda, tráfego recebido e outras métricas.

#

<a name="protocolos"></a>

## **Protocolos de Rede**

### Handshake

> O processo começa com a abertura da conexão websocket, que é feita pelo cliente.  
> O servidor então responde com um pacote handshake_ping e uma chave aleatória de 4 bytes que será utilizada para criptografar as mensagens entre o cliente e o servidor.  
> O cliente então responde com um handshake_pong e outra chave aleatória de 4 bytes, além de um nome de tamanho entre 4 e 16 caracteres, usado para identificar o zumbi.  
> Usando o nome e as duas chaves trocadas, o servidor faz o hash da chave e envia um pacote do tipo handshake_success, contendo o hash.  
> O cliente então compara o hash local com o hash recebido pelo servidor e se os hashes forem iguais, envia outro pacote handshake_success, indicando ao servidor de controle que a comunicação foi iniciada e as rotinas de heartbeats e ataque deve começar.  

Linha do tempo: (C=cliente, S=servidor))  

1 C ---> S | C Abre conexão websocket  
2 C <--- S | S Envia handshake_ping e chave aleatória server_key  
3 C ---> S | C Envia handshake_pong, nome do zumbi e chave aleatória client_key  
4 C <--- S | S Envia handshake_success, hash sha256 do nome do zumbi e das duas chaves trocadas  
5 C ---> S | C Envia handshake_success após comparar os hashes sha256 do identificador do zumbi e o hash recebido pelo servidor, confirmando que a troca de chaves foi válida e que já está esperando as rotinas de heartbeat e ataque

Este processo é puramente por Proof of Concept e não é de fato um handshake real, já que este processo é feito por trás dos panos já que estamos usando a tecnologia de websockets.

**demo conexão handshake**

![](https://i.imgur.com/AgrAJAp.png)

**gif com o processo completo de comunicação, desde o handshake até os heartbeats, com 3 clientes simultâneos**

![](https://i.imgur.com/zBNBAuB.gif)

#

### Heartbeat

> O servidor de controle envia um pacote do tipo heartbeat_ping para todos os zumbis que estão conectados, que devem responder com um heartbeat_pong para comprovarem que estão ativos e esperando o comando de ataque.

**Teste com 100 zumbis conectados:**

![teste com 100 zumbis conectados](https://i.imgur.com/6MH3YfS.png)

#

## **Pacotes de Rede**

> Lista com os pacotes e conteudos trocados entre o servidor de controle e zumbis, serializados em formato JSON

- handshake_ping (C<--S)
- handshake_pong (C-->S)s
- handshake_success (C<--S)
- heartbeat_ping (C<--S)
- heartbeat_pong (C-->S)

<a name="handshake_ping"></a>

### handshake_ping

Pacote enviado do servidor de controle para um zumbi após uma nova conexão via websocket ser aberta, esperando como resposta um handshake pong contendo um nome completo para o cliente

> {  
> "type": "handshake_ping",  
> "server_key": "\<chave aleatoria\>"  
> }

<a name="handshake_pong"></a>

### handshake_pong

Pacote enviado do zumbi para o servidor de controle respondendo o handshake_ping, enviando também o nome/identificador do zumbi, composto por um nome escolhido pelo cliente ou gerado automaticamente, uma chave aleatória gerada no cliente e a chave recebida no handshake_ping e um checksum do nome completo, que será validado no servidor

> {  
> "type": "handshake_pong",  
> "client_name": "\<identificador zumbi\>",  
> "checksum": "\<checksum\>"  
> }

<a name="handshake_success"></a>

### handshake_success

Pacote enviado do servidor de controle para um zumbi confirmando a conexão bem sucedida e confirmando o inicio do pulso do heartbeat

> {  
> "type": "handshake_success",  
> "checksum": server_checksum  
> }

<a name="heartbeat_ping"></a>

### heartbeat_ping

Pacote enviado do servidor de controle para todos os zumbis a cada 1s, mantendo controle de todos os zumbis que ainda estão ativos e que perderam a conexão

> {  
> "type":"heartbeat_ping",  
> "seed": "\<numero aleatorio\>"  
> }

<a name="heartbeat_pong"></a>

### heartbeat_pong

Pacote enviado do zumbi ao servidor de controle respondendo um heartbeat_ping e realizando um Proof-of-Work (PoW) e retornando para o servidor de controle. Caso o PoW seja válido, o cliente é mantido na lista de zumbis ativos.  
Por ser um processo demonstrativo, o algorítmo de Proof of Work é só inverter a seed enviada pelo servidor.

> {  
> "type":"heartbeat_pong",  
> "pow": "\<numero aleatorio ao contrario\>"  
> }

#

<a name="setup"></a>

## **Setup**

> Work in progress, não está funcional  
> Para rodar o projeto em sua própria máquina, são necessárias algumas dependências.

### Dependencias

- python3 (3.9.7 foi usado para o desenvolvimento)
- python3-pip
- python3-venv

### Instalação

O repositório conta com um arquivo de setup que instala todas as dependências necessárias em sistemas Unix usando apt e outras utilidades do shell.

#### Linux/Unix

Para instalar com o projeto você precisa de um usuário com privilégios administrativos, ou seja, um usuário com permissão de root.

**Instalador**

```bash
chmod +x ./build
./build
```

**Instalando manualmente**

```bash
sudo apt install python3 python3-pip python3-venv
```

### Executando

Guia temporário, o projeto contará com instalador e utils para rodar  

servidor c2:

```bash
cd ./c2_server/; python ./server.py
```

webapp:

```bash
cd ./frontend/; python ./app.py
```
