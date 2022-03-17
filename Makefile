.PHONY: sync, test

sync:
	rsync -auv . xuchen@xc-mbp-16:~/Documents/repo/ChatApp/

test:
	@python test.py

clean_table:
	@echo "delete from user" | sqlite3 resource/chatapp.db

dummy_data:
	@echo "insert into user(name, ip, port, status) values('xc-m1', '192.168.0.233', 12345, 'yes'), ('xc-1', '192.168.0.222', 12344, 'yes')" | sqlite3 resource/chatapp.db

show_users:
	@echo "select * from user" | sqlite3 resource/chatapp.db