CUR_DIR=$(shell pwd | sed 's/.*\///g')
CODE_VER=$(shell git describe --tags)
NAME=gitm-$(CODE_VER).tar.gz

release:
	@cd .. && tar --exclude='.git' -czf $(NAME) $(CUR_DIR)
	@cd .. && cp $(NAME) dist/
	@cd .. && rm $(NAME)
	@cd ../dist && rm gitm-latest.tar.gz
	@cd ../dist && cp $(NAME) gitm-latest.tar.gz

install:
	@sudo ./install.sh