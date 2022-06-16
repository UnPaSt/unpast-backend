# Requirements

- Docker
- Docker-compose

# DESMOND2 executable
- Currently the DESMOND2 git repository is added as submodule. To pull this dependency execute:

`git submodule update --init --recursive`

# Setup
- Pull required docker images and build local images

`docker-compose pull; docker-compose build`

- Start db and backend-containers

`docker-compose up -d`

- Shutdown containers:

`docker-compose down`