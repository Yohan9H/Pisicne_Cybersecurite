all: up

up:
	@echo "Starting up the environment..."
	docker-compose up --build -d


down:
	@echo "Shutting down the environment..."
	docker-compose down


clean:
	@echo "Stopping containers, removing volumes, and deleting images..."
	docker-compose down -v --rmi all


shell:
	@echo "Connecting to the attacker container..."
	docker-compose exec attacker /bin/bash


victim-shell:
	@echo "Connecting to the victim container..."
	docker-compose exec victim sh


status:
	@docker-compose ps


logs:
	@docker-compose logs -f

.PHONY: up down clean shell victim-shell status logs