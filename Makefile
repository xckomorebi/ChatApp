.PHONY: sync, test

sync:
	rsync -auv . xuchen@xc-mbp-16:~/Documents/repo/ChatApp/

test:
	@python test.py

clean_user:
	@echo "delete from user" | sqlite3 resource/chatapp.db

dummy_user:
	@echo "insert into user(name, ip, port, status) values('xc-m1', '192.168.0.233', 12345, 'yes'), ('xc-1', '192.168.0.222', 12344, 'yes')" | sqlite3 resource/chatapp.db

show_user:
	@echo "select * from user" | sqlite3 resource/chatapp.db

clean_msg:
	@echo "delete from message" | sqlite3 resource/chatapp.db

dummy_msg:
	@echo "insert into message(content, from_, 'to') values('test123', 'test1','test2')" | sqlite3 resource/chatapp.db

show_msg:
	@echo "select * from message" | sqlite3 resource/chatapp.db