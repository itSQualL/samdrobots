#!/usr/bin/python3

import sys
import Ice
Ice.loadSlice('-I. --all icegrid/services.ice')

import services
from controller_factory import ControllerFactoryI

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()

        container_prx = broker.propertyToProxy("ContainerProxy")
        container_prx = services.ContainerPrx.checkedCast(container_prx)
        container_list = container_prx.list()

        servant = ControllerFactoryI(container_prx)

        adapter = broker.createObjectAdapter("ControllerFactoryAdapter")
        controller_factory_prx = adapter.add(servant, broker.stringToIdentity("ControllerFactory"))
        adapter.activate()


        if not "controller_factory_1" in container_list:
            container_prx.link("controller_factory_1", controller_factory_prx)
        elif not "controller_factory_2" in container_list:
            container_prx.link("controller_factory_2", controller_factory_prx)
        else:
            container_prx.link("detector_factory_1", controller_factory_prx)

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))

