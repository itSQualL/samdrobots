import Ice
Ice.loadSlice('services.ice')

import services
from container import ContainerI

class ContainerFactoryI(services.ContainerFactory):
    """
    ContainerFactory interface implementation
    """

    def makeContainer(self, current=None):
        """
        Creates a new container object and an associated proxy
        """
        servant = ContainerI()
        container_prx = current.adapter.addWithUUID(servant)
        container_prx = services.ContainerPrx.checkedCast(container_prx)

        print("Container proxy created {0}".format(container_prx))

        return container_prx
