import sys
import Ice

from player import PlayerI

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = PlayerI()

        adapter = broker.createObjectAdapter("PlayerAdapter")
        player_prx = adapter.addWithUUID(servant)
        player_prx = drobots.PlayerPrx.uncheckedCast(player_prx)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
