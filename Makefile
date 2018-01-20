all: container factory player

container:
	gnome-terminal --tab -e "python3 ./container/server.py --Ice.Config=container/server.config"

factory:
	gnome-terminal --tab -e "python3 ./controller/server.py --Ice.Config=controller/factory1.config"
	gnome-terminal --tab -e "python3 ./controller/server.py --Ice.Config=controller/factory2.config"

player:
	python3 ./player/client.py --Ice.Config=player/client.config

