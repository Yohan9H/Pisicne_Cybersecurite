.PHONY: all build up down stop shell sh run clean re

all: build

build:
	@echo "Construction de l'image Docker..."
	@docker-compose build

up:
	@echo "Démarrage du conteneur Docker..."
	@docker-compose up -d

down:
	@echo "Arrêt et suppression du conteneur Docker..."
	@docker-compose down

shell:
	@echo "Accès au terminal du conteneur..."
	@docker-compose exec stockholm-dev bash


run:
	@echo "Exécution du programme dans le conteneur avec les arguments : $(ARGS)"
	@docker-compose exec stockholm-dev python3 stockholm.py $(ARGS)

clean:
	@echo "Nettoyage complet de l'environnement Docker (conteneur, image...)"
	@docker-compose down --rmi all -v

setup:
	@python setup_test_files.py

re: down up
	@echo "Environnement Docker recréé."
