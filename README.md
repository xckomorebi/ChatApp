ChatApp
===
__Name: Chen Xu__

__UNI: cx2255__

---

A simple chat application with at least 3 clients and a server using UDP (programming assignment 1 of CSEE4119 Computer Networks).

The program has two modes, the client mode and the server mode. The client instances communicate directly with each other. The server instance is used to set up clients and for book-keeping purposes.  The server is also used to store off-line messages  from clients and broadcast channel messages to all clients within a predefined communication channel (group chat).

Installation 
===

This app is supposed to run with minimum dependencies.

make sure you have `python3` and `sqlite3` installed on your machine

(update: `sqlite3` binary executable is optional, but make sure your `python3` comes with a sqlite3 module. On ubuntu 18.04 LTS this is by default, but I do know it's not always the case for all distros)

```bash
$ git clone "https://github.com/xckomorebi/ChatApp"
$ cd ChatApp

$ # if you want to add this script to /user/local/bin
$ make install
$ ChatApp <args>

$ # or just create the database
$ make init_db
$ python ChatApp.py <args>
```

Usage:
===
## start server
```bash
$ ChatApp -s PORT
(main loop start, no output)
```
or
```bash
$ ChatApp -s PORT &
[1] <pid>
$ 
```
to run server in background

## start client
```bash
$ ChatApp -c NAME SERVER-IP SERVER-PORT CLIENT-PORT
>>> [Welcome, you are registered.]
>>> <user input>
```

Command format
===
### Registration
```
>>> reg <username>
```



### Chatting
```
>>> send <name> <message>
```

### De-registration
```
>>> dereg <name>
```
### Group Chat
```
>>> send_all <message>
```


TODO
===

- [x] can't update table if a certain user log back in from silent leave

- [ ] ~~udp hole punching ### FATAL!!!!!!!!!!!!!!!!!!!!~~

- [x] Command options
- [x] Makefile
- [x] Chatting
- [x] Registration
  - [x] Client mode
  - [x] Server mode
- [x] De-registration
  - [x] Client
  - [x] Server
- [x] Offline Chat
  - [x] Client
  - [x] Server
- [x] Group Chat
  - [x] basic
  - [x] ack
- [x] Testing
- [ ] github pipeline (low priority)
- [ ] Logging (low priority)
- [ ] ~~Deployment~~
- [ ] Submission