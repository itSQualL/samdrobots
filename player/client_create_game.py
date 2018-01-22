#!/usr/bin/python3

import sys
import Ice

Ice.loadSlice('-I. --all icegrid/drobots.ice')
Ice.loadSlice('-I. --all icegrid/services.ice')

import drobots
import services

from player import PlayerI

class ClientApp(Ice.Application):
    """
    Ice.Application specialization
    """
    def run(self, argv):
        """
        Entry-point method for every Ice.Application object.
        """

        broker = self.communicator()

        # Using PlayerAdapter object adapter forces to define a config file
        # where, at least, the property "PlayerAdapter.Endpoints" is defined
        adapter = broker.createObjectAdapter("PlayerAdapter")

        # Using "propertyToProxy" forces to define the property "GameProxy"
        game_factory_prx = broker.propertyToProxy("GameProxy")
        game_factory_prx = drobots.GameFactoryPrx.checkedCast(game_factory_prx)

        #Create container proxy
        container_prx = broker.propertyToProxy("ContainerProxy")
        container_prx = services.ContainerPrx.checkedCast(container_prx)

        # Using "getProperty" forces to define the property "PlayerName"
        name = broker.getProperties().getProperty("PlayerName")

        servant = PlayerI(container_prx)
        player_prx = adapter.addWithUUID(servant)
        player_prx = adapter.createDirectProxy(player_prx.ice_getIdentity())
        player_prx = drobots.PlayerPrx.uncheckedCast(player_prx)
        adapter.activate()


        try:
            game_prx = game_factory_prx.makeGame("isaac", 3)
            game_prx = drobots.GamePrx.checkedCast(game_prx)

            game_prx.login(player_prx, name)

            self.shutdownOnInterrupt()
            self.communicator().waitForShutdown()

        except Exception as ex:
            print("An error has occurred: {}".format(ex))
            return 1

        return 0


if __name__ == '__main__':
    client = ClientApp()
    retval = client.main(sys.argv)
    sys.exit(retval)

