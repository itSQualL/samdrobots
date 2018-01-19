import sys
import Ice
Ice.loadSlice('services.ice')
import services


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        factory = services.ContainerFactoryPrx.checkedCast(proxy)

        b = factory.makeContainer()
        b.link("hola", factory)
        b.list()

        return 0


sys.exit(Client().main(sys.argv))
