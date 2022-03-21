ChatApp
===

A simple chat application with at least 3 clients and a server using UDP (programming assignment 1 of CSEE4119 Computer Networks).

The program has two modes, the client mode and the server mode. The client instances communicate directly with each other. The server instance is used to set up clients and for book-keeping purposes.  The server is also used to store off-line messages  from clients and broadcast channel messages to all clients within a predefined communication channel (group chat).

Installation
===
This app is supposed to run with minimum dependencies.

Server side: make sure you have `python3` and `sqlite3` installed on your machine

Client side: `python3`

```bash
$ git clone "https://github.com/xckomorebi/ChatApp"
$ cd ChatApp
$ make install # optional //TODO
```

Usage: (TODO)
===
### start server
```bash
$ ChatApp -s PORT
(some welcome message)
```

### start client
```bash
$ ChatApp -c NAME SERVER-IP SERVER-PORT CLIENT-PORT
(some welcome message)
>>>
```

Command format
===
### Registration
```
>>> reg <user>
```

### Chatting
```
>>> send <name> <message>
```

### De-registration
```
>>> dereg <name>
```
### Offline Chat
```
>>>
```

### Log back in
```
>>> reg <name>
```

### Group Chat
```
>>> send_all <message>
```


TODO
===

- [ ] can't update table if a certain user log back in from silent leave

~~- udp hole punching ### FATAL!!!!!!!!!!!!!!!!!!!!~~

- [x] Command options
- [x] Makefile
- [x] Chatting
- [ ] Logging
- [x] Registration
  - [x] Client mode
  - [x] Server mode
- [ ] De-registration
  - [ ] Client
  - [ ] Server
- [ ] Offline Chat
  - [ ] Client
  - [ ] Server
- [ ] Group Chat
  - [x] basic
  - [ ] ack
- [ ] Testing
- [ ] github pipeline (low priority)
- [ ] Deployment
- [ ] Submission