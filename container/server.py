import sys
import Ice
Ice.loadSlice('services.ice')

import services
from container_factory import ContainerFactoryI

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ContainerFactoryI()

        adapter = broker.createObjectAdapter("ContainerFactoryAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("containerFactory"))
        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
