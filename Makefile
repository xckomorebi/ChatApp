.PHONY: sync, test

sync:
	rsync -auv . xuchen@xc-mbp-16:~/Documents/repo/ChatApp/

test:
	@python test.py