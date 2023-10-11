include .env

NAME		=	activebot
COMPOSE		=	docker-compose -p $(NAME)
RM			=	rm -rf
SUDO		=	sudo
WEB         =   activebot_web_1

SSP_IP		:=	*

ifeq ($(shell uname), Darwin)
    HOST_IP := $(shell ipconfig getifaddr en0)
else 
    HOST_IP := $(shell hostname -I | awk '{print $$1}')
endif

all: up

build: update_ip create_dir
	$(COMPOSE) up -d --build
	@echo "Started service with host IP:\033[1;33m  http://${HOST_IP}/admin\033[1;0m"

up: update_ip create_dir
	@$(COMPOSE) up 
	@echo "\033[1;0mStarting service with host IP: \033[1;33m  http://${HOST_IP}/admin\033[1;0m"

migrate:
	@docker exec -it $(WEB) bash src/migrate.sh
stop:
	@$(COMPOSE) stop

fclean:	stop
	@$(COMPOSE) down -v
	@rm -Rf .env~

re:
	docker-compose restart $(WEB)

restart: stop build

reset:	prune all

prune:	fclean
	@docker system prune --volumes --force --all

bash:
	@docker exec -it $(WEB) bash

logs:
	@docker logs -f $(WEB)

update_ip:
	@if [ -f .env ]; then \
		if grep -q '^HOST_IP=' .env; then \
			sed -i~ 's/^HOST_IP=.*/HOST_IP=${HOST_IP}/' .env; \
		else \
			echo 'HOST_IP=${HOST_IP}' >> .env; \
		fi \
	else \
		echo '.env file not found'; \
	fi

ssp_ip:
	@if [ -f .env ]; then \
		if grep -q '^SSP_IP=' .env; then \
			sed -i~ 's/^SSP_IP=.*/SSP_IP=${SSP_IP}/' .env; \
		else \
			echo 'HOST_IP=${HOST_IP}' >> .env; \
		fi \
	else \
		echo '.env file not found'; \
	fi

create_dir:
	@if [ ! -d "data" ]; then \
		mkdir data; \
		echo "Directory 'data' created."; \
	else \
		echo "\033[0;30m Directory 'data' already exists.\033[1;0m"; \
	fi

help:
	@echo "\033[1;35mMakefile targets:"
	@echo "  \033[1;34mall        \033[1;0m - Alias for 'up'."
	@echo "  \033[1;34mbuild      \033[1;0m - Builds the Docker containers."
	@echo "  \033[1;34mup         \033[1;0m - Starts the Docker containers."
	@echo "  \033[1;34mmigrate    \033[1;0m - Makes necessary migrations"
	@echo "  \033[1;34mstop       \033[1;0m - Stops the Docker containers."
	@echo "  \033[1;34mfclean     \033[1;0m - Stops and removes the Docker containers and volumes, removes the '.env' file."
	@echo "  \033[1;34mre         \033[1;0m - Restarts the 'web' service(aka django app)."
	@echo "  \033[1;34mrestart    \033[1;0m - Stops and rebuilds the Docker containers."
	@echo "  \033[1;34mreset      \033[1;0m - Removes all Docker containers and volumes, recreates the 'data' directory, and starts the Docker containers."
	@echo "  \033[1;34mprune      \033[1;0m - Stops and removes all Docker containers and volumes."
	@echo "  \033[1;34mbash       \033[1;0m - Starts a Bash shell inside the 'web' container."
	@echo "  \033[1;34mlogs       \033[1;0m - Follows the logs of the 'web' container."
	@echo "  \033[1;34mupdate_ip  \033[1;0m - Updates the HOST_IP environment variable in the '.env' file."
	@echo "  \033[1;34mcreate_dir \033[1;0m - Creates the 'data' directory if it doesn't exist.(directory is needed for volume binding)"


	

.PHONY: all build up stop fclean re prune bash migrate build update_ip create_dir logs restart reset
