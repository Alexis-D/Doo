DEST=/usr/bin/doo

all: install

install:
	@cp -f doo.py ${DEST}
	@chmod +x ${DEST}

uninstall:
	@rm -f ${DEST}

