docker build -t avl . : build container and name it avl
docker ps -all : see all containers
docker rm <image_id> : remove container

docker run <image_id> : create container from the image
docker run --network host avl : run avl container on host network

docker network ls : list networks
docker network rm <id> : delete network
docker image inspect avl: inpect image

docker exec -it my-container bash : execute bash shell in my-container and navigate inside container filesystem
