# Projeto de Videoconferência Descentralizada

Este projeto visa desenvolver uma aplicação de videoconferência descentralizada em Python usando comunicação por sockets. A aplicação permite que os usuários se registrem em um servidor e estabeleçam conexões Peer-to-Peer (P2P) para realizar videoconferências.

## Passos a Fazer

### ETAPA 1 (31/10/2023)

- [x] O socket cliente deve:
  - [x] Registrar-se no servidor utilizando um nome e um IP exclusivos e indicando a porta apta para receber o pedido de chamada
  - [x] Realizar consultas de endereços de portas por nomes específicos dos usuários.
  - [x] Caso o cliente deseje se desvincular do servidor de registro, ele deve enviar uma mensagem com esta solicitação.

- [x] O socket servidor deve:
  - [x] Armazenar e imprimir uma tabela dinâmica contendo informações dos clientes.
  - [x] Imprimir mensagem de confirmação de registro de novo usuário.
  - [x] Caso o usuário já esteja cadastrado, imprimir mensagem informando esta condição.
  - [x] Responder aos clientes o nome de um nó conectado e seus respectivos endereços e números de porta, quando assim solicitado.
  - [x] Caso o cliente solicite o fim da conexão, o servidor deve responder com mensagem de encerramento e, depois, fechar o socket.
  
### ETAPA 2 (28/11/2023)

- [ ] O socket cliente deve:
  - [ ] Solicitar a videochamada a um par IP:porta de destino utilizando uma mensagem específica, como se fosse a mensagem de INVITE do protocolo SIP. Assim, o receptor pode negar ou aceitar o pedido.
  - [ ] A reprodução da mídia deve ser iniciada assim que a chamada é aceita.
  - [ ] Conter métodos para encerrar a transmissão.

- [ ] O socket servidor deve:
  - [ ] Aceitar ou rejeitar a chamada.
  - [ ] Se a chamada for aceita, informar na resposta o número das portas para receber os fluxos de áudio e vídeo.

- [ ] Opcional
  - [ ] Interface gráfica
  - [ ] Tratativas de latência.
  - [ ] Tratativas de perda de pacotes.

## Como Executar

Execute o arquivo [server.py](src/server.py) em um terminal e o [cliente.py](src/client.py) em outro.

## Licença

Este projeto está sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.