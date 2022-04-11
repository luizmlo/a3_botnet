## A3 - Botnets

> Este é um repositório onde documentarei todo o processo de pesquisa e desenvolvimento do meu trabalho de conclusão de semestre da UC de Ambientes Computacionais e Segurança.  
> O tema escolhido pelo meu grupo foi o de Botnets, que é uma coleção de tecnologias que utilizam redes de computadores para comunicar-se entre si.  
> O projeto que escolhi fazer contará com uma botnet 100% funcional feita com websockets e Python, funcionando em cima do protocolo HTTP e rodando completamente no browser das "vítimas".

#

Indice
- [A3 - Botnets](#a3---botnets)
  - [Resumo do Projeto](#resumo-do-projeto)
  - [C2](#c2)
  - [Zumbi](#zumbi)
  - [Vitima](#vitima)
  - [Protocolos de Rede](#protocolos-de-rede)
    - [Handshake](#handshake)
    - [Heartbeat](#heartbeat)
  - [Setup](#setup)

#

<a name="resumo"></a>
### Resumo do Projeto

Este projeto vai ser muito complexo e contará com diversas partes, entre elas um servidor de controle que comandará os *zumbis*, um frontend malicioso que infecta as vítimas e um site que servirá de vítima da botnet, sofrendo um ataque de DDoS durante a apresentação ao vivo.

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

Esta será uma aplicação web onde as vítimas irão se conectar e se comunicar com o servidor de controle, aguardando ordens de ataque por trás dos panos utilizando a tecnologia de websockets.

Os clientes conectados terão que responder um pulso enviado pelo servidor para provar que ainda estão conectados e ativos, esperando o comando e o alvo do ataque.

#

<a name="vitima"></a>
### Vitima
> A vítima do ataque distribuido

Este será um servidor de demonstração que irá sofrer o ataque coordenado da botnet e será sobrecarregado, tendo sua funcionalidade prejudicada pelos zumbis.

Este irá contar com uma interface de monitoramento, onde iremos observar ao vivo o estado da vitima, quantas requisições estão chegando, a quantidade de banda, tráfego recebido e outras métricas.

#

<a name="protocolos"></a>
### Protocolos de Rede  
#### Handshake
> O processo começa com a abertura da conexão websocket, que é feita pelo cliente.  
> O servidor então responde com um pacote handshake_ping e uma chave aleatória de 4 bytes que será utilizada para criptografar as mensagens entre o cliente e o servidor.  
> O cliente então responde com um handshake_pong e outra chave aleatória de 4 bytes, além de um nome de tamanho entre 4 e 16 caracteres, usado para identificar o zumbi.  
> Usando o nome e as duas chaves trocadas, o servidor faz o hash da chave e envia um pacote do tipo handshake_success, contendo o hash.  
> O cliente então compara o hash local com o hash recebido pelo servidor e se os hashes forem iguais, a conexão é aceita.  

Linha do tempo: (C=cliente, S=servidor))  

C ---> S | Abre conexão websocket  
C <--- S | S Envia handshake_ping e chave aleatória server_key  
C ---> S | C Envia handshake_pong, nome do zumbi e chave aleatória client_key  
C <--- S | S Envia handshake_success, hash do nome do zumbi e das duas chaves trocadas  
C ---> S | C Envia handshake_success, confirmando que a troca de chaves foi válida e que já está esperando as rotinas de heartbeat e ataque  

#

#### Heartbeat

#

<a name="setup"></a>
### Setup
> Work in progress, não está funcional ainda
Para rodar o projeto em sua própria máquina, são necessárias algumas dependências:
- python3 (3.9.7 foi usado para o desenvolvimento)
- python3-pip
- python3-venv

O repositório conta com um arquivo de setup que instala todas as dependências necessárias em sistemas Unix usando apt e outras utilidades do shell.

Para instalar com o *./build* você precisa ter o *sudo* habilitado.

```bash
chmod +x ./build
./build
```

Para rodar o servidor de controle e o frontend malicioso, utilize os comandos abaixo:

```bash
./start_c2
./start_front
```