import sys
import Ice
Ice.loadSlice('--all drobots.ice')
Ice.loadSlice('--all services.ice')

import services
from container import ContainerI

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ContainerI()

        adapter = broker.createObjectAdapter("ContainerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("container"))
        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
