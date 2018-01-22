#!/usr/bin/make -f
# -*- mode:makefile -*-

all: mkdirs prepare-files up-grids

prepare-files:
	cp player/*.py icegrid/
	cp container/*.py icegrid/
	cp controller/*.py icegrid/
	cp interfaces/*.ice icegrid/
	chmod +777 icegrid/*.py
	icepatch2calc icegrid/.

mkdirs:
	mkdir -p /tmp/db/registry
	mkdir -p /tmp/db/player_node
	mkdir -p /tmp/db/container_node
	mkdir -p /tmp/db/controller_node
	mkdir -p /tmp/db/detector_node

up-grids:
	gnome-terminal --tab -e "icegridnode --Ice.Config=icegrid/container_node.config" &

	@echo -- waiting registry to start
	@while ! netstat -lptn 2> /dev/null | grep ":4067" > /dev/null; do \
		sleep 1; \
	done
	@echo -- registry up

	gnome-terminal --tab -e "icegridnode --Ice.Config=icegrid/controller_node.config" & \
	sleep 1
	gnome-terminal --tab -e "icegridnode --Ice.Config=icegrid/detector_node.config" & \
	sleep 1
	gnome-terminal --tab -e "icegridnode --Ice.Config=icegrid/player_node.config" &

	sleep 3

	icegridadmin --Ice.Config=icegrid/locator.config -u user -p pass -e "application add 'icegrid/drobots.xml'"

clean:
	rm -rf icegrid/*.py
	rm -rf icegrid/*.bz2
	rm -rf icegrid/*.ice
	rm -rf icegrid/*.sum
	icegridadmin --Ice.Config=icegrid/locator.config -u user -p pass -e "application remove 'drobots'"
	sudo killall icegridnode

