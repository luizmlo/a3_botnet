## A3 - Botnets

> Este é um repositório onde documentarei todo o processo de pesquisa e desenvolvimento do meu trabalho de conclusão de semestre da UC de Ambientes Computacionais e Segurança.  
> O tema escolhido pelo meu grupo foi o de Botnets, que é uma coleção de tecnologias que utilizam redes de computadores para comunicar-se entre si.  
> O projeto que escolhi fazer contará com uma botnet 100% funcional feita com websockets e Python, funcionando em cima do protocolo HTTP e rodando completamente no browser das "vítimas".

#

## Setup
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