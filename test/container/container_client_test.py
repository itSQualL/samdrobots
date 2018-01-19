import sys
import Ice
Ice.loadSlice('--all services.ice')
import services


class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        container = services.ContainerPrx.checkedCast(proxy)

        container.link("hola", container)
        print(container.list())

        return 0


sys.exit(Client().main(sys.argv))
