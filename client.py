import sys
import Ice

Ice.loadSlice('drobots.ice')
import drobots

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
        game_prx = broker.propertyToProxy("GameProxy")
        game_prx = drobots.GamePrx.checkedCast(game_prx)

        # Using "getProperty" forces to define the property "PlayerName"
        name = broker.getProperties().getProperty("PlayerName")

        servant = PlayerI()
        player_prx = adapter.addWithUUID(servant)
        player_prx = drobots.PlayerPrx.uncheckedCast(player_prx)
        adapter.activate()

        print("Connecting to game {} with nickname {}".format(game_prx, name))

        try:
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