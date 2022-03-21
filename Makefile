mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

.PHONY: init_user, init_message, init_db, install

init_user: sql/user.sql
	@cat sql/user.sql | sqlite3 resource/chatapp.db

init_message: sql/message.sql
	@cat sql/message.sql | sqlite3 resource/chatapp.db

init_db: init_user, init_message

install: init_db
	@while true; do \
		read -p "Symlink ChatApp.py to /usr/local/bin/ChatApp [Y/N] " yn; \
		case $$yn in \
			[Yy]* ) ln -sF ${mkfile_dir}/ChatApp.py /usr/local/bin/ChatApp \
			&& echo ChatApp successfully installed!!; break;; \
			[Nn]* ) exit;; \
			* ) echo "Please answer yes or no.";;\
		esac;\
	done

# the following command is only for testing

sync:
	rsync -auv . xuchen@xc-mbp-16:~/Documents/repo/ChatApp/

test:
	@python test.py

clean_user:
	@echo "delete from user" | sqlite3 resource/chatapp.db

dummy_user:
	@echo "insert into user(name, ip, port, status) values('test1', '192.168.0.233', 10001, 'yes'), ('test2', '192.168.0.233', 10002, 'yes')" | sqlite3 resource/chatapp.db

alter_user:
	@echo "update user set status='no' where name='test2'" | sqlite3 resource/chatapp.db

show_user:
	@echo "select * from user" | sqlite3 resource/chatapp.db

clean_msg:
	@echo "delete from message" | sqlite3 resource/chatapp.db

dummy_msg:
	@echo "insert into message(content, from_, 'to') values('test123', 'test1','test2')" | sqlite3 resource/chatapp.db

show_msg:
	@echo "select * from message" | sqlite3 resource/chatapp.db

server:
	chatapp -s 12345

test1:
	chatapp -c test1 192.168.0.233 12345 10001

test2:
	chatapp -c test2 192.168.0.233 12345 10002

test3:
	chatapp -c test3 192.168.0.233 12345 10003