IMAGE_NAME=rev-piscine

all: build

build:
	@echo "Construction de l'image Docker : $(IMAGE_NAME)"
	@docker build --platform=linux/amd64 -t $(IMAGE_NAME) .

shell: build
	@echo "Lancement d'un shell interactif dans le conteneur..."
	@docker run --privileged -it --rm -v "$(shell pwd)":/work -w /work $(IMAGE_NAME) /bin/bash

clean:
	@echo "Suppression de l'image Docker : $(IMAGE_NAME)"
	@docker image rm -f $(IMAGE_NAME)

fclean:
	@echo "Suppression complète de Docker pour $(IMAGE_NAME)"
	-@docker ps -a -q --filter "ancestor=$(IMAGE_NAME)" | xargs -r docker rm -f
	-@docker ps -a -q --filter "name=$(IMAGE_NAME)" | xargs -r docker rm -f
	-@docker image rm -f $(IMAGE_NAME) || true
	-@docker volume prune -f
	-@docker container prune -f
	-@docker builder prune -f

re: fclean all

.PHONY: all build shell clean re