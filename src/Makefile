CUR_DIR=$(shell pwd | sed 's/.*\///g')
CODE_VER=$(shell git describe --tags)
NAME=gitm-$(CODE_VER).tar.gz

release:
	@echo $(CUR_DIR)
	@echo $(NAME)
	@cd .. && tar --exclude='.git' -czf $(NAME) $(CUR_DIR)
	@cd .. && mv $(NAME) dist/
	@cd ../dist && ln -s $(NAME) gitm-latest.tar.gz

install:
	@sudo ./install.sh