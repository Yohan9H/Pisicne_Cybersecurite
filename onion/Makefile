IMAGE_NAME      := onion-service
CONTAINER_NAME  := my-onion-service
SSH_PORT        := 4242
USER            := user

.PHONY: all build run stop clean logs hostname ssh re help

all: build

build:
	@echo "Building Docker image: [$(IMAGE_NAME)]..."
	@docker build -t $(IMAGE_NAME) .

run:
	@echo "Running Docker container [$(CONTAINER_NAME)]..."
	@docker run -d -p $(SSH_PORT):4242 --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	@echo "Stopping Docker container [$(CONTAINER_NAME)]..."
	@docker stop $(CONTAINER_NAME) || true

clean:
	@echo "Stopping and removing Docker container [$(CONTAINER_NAME)]..."
	@docker stop $(CONTAINER_NAME) || true
	@docker rm $(CONTAINER_NAME) || true

logs:
	@echo "--- Showing logs for [$(CONTAINER_NAME)] ---"
	@docker logs $(CONTAINER_NAME)

hostname:
	@echo "Fetching .onion hostname..."
	@docker exec $(CONTAINER_NAME) cat /var/lib/tor/hidden_service/hostname

ssh:
	@echo "Connecting via SSH to $(USER)@localhost:$(SSH_PORT)..."
	@ssh $(USER)@localhost -p $(SSH_PORT)

re: clean build run
