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

PORT must be integer in range of 1024-65535, otherwise this program will exit with following message:

```
Port number should be an integer between 1024 and 65535!
```

## start client
```bash
$ ChatApp -c NAME SERVER-IP SERVER-PORT CLIENT-PORT
>>> [Welcome, you are registered.]
>>> <user input>
```

SERVER-IP can be valid ipv4 address, or address you configured in `/etc/hosts`

otherwise program will exit with:
```
You should enter a valid IP address!
```

Command format
===
### Registration
```
>>> reg <name>
```

If you run this program with command line arguments, a message like this will be automatically send to server, `<name>` is what you put in shell command.

If this is the first time you register a user (via command line or dereg and dereg to another name), you can see this message:

```
>>> [Welcome, you are registered.]
```

A returning user could see:

```
>>> [Welcome back!]
```

If the server is not responding, client will retry 5 times and exit with code 0.

Every time you register (new user or returning user) server will send you a table of all user. If you did not leave silently (close ssh window or Ctrl-C) and log back in, server will send all active user a update-table message (but only contains your information).

Any message (direct message and group message) sent to you when you are offline will be stored, once you reg back, these messages will show up.

### Chatting
```
>>> send <name> <message>
```

You will get an ack from the receiver if message is sent sucessfully. Otherwise your client will tell the server that the receiver is offline, and server will notify all active user to change the receiver's status.

If in your local table the receiver is offline. the message will directly send to server, and you will get ack from server that the message is saved and would be sent to that user once login.

If for some mysterious and strange reason, you think a user is offline but it's not true. The server will try to contact that user to see whether the receiver is really offline. Once the server get response from the user, it will give you an error message and update your local table.


### De-registration
```
>>> dereg <name>
```

Actually `<name>` is optional, and whatever you type after `dereg` the current user will logout. So just type `dereg` and it will tell the server you are offline. This update will be broadcast to all active user.

(In fact you are still receiving messages, but without any process until you reg back LOL)

### Group Chat
```
>>> send_all <message>
```

This message will be sent to server, and you will get ack from server. All active user will receive the message.

If any active user silently leave the channel, the server will store his message, and notify all other user that they are offline.

Additional features
===
### One username can only login to one device

If you login to another client, the server will check status of original instance, and take it offline.

It prevent the this situation from happening: someone else (maybe yourself) log into your account and you don't know, and you find yourself still able to send message, but can't hear from others.

### reg to another account in the same client program

Assume you have multiple accounts, you can switch between them in one program by `dereg` and `reg <another_name>`, all offline message will be process correctly

### silently leave

Server will know you are a returning user.

### update table only when necessery
If you silently leave the channel and log back in. There would be no different in server sql table, so there is no need to broadcast update-table command.


Tech details
===

ChatApp is a multithreading program.

Client side has two threads, one for sending message, one for receiving.

Server normally has one thread for listening, when server broadcasts messages, it will create one extra thread for each active receiver.

There are two sql tables: the user table and offline message table. You can find two corresponding data access object class in `models.py`.

All sent and received messages follows a customized format (see `ChatApp.msg.Msg`)
```python
Msg(content, type_, from_, to, to_server, addr)
```
message type_ is instance of Enum class `MsgType`, server and client process messages based on its type.

No fancy algorithm or data structure, no fancy design pattern. I created a lot of global variables which is not a good pratice (and evil), but I don't have time to refactor them.

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