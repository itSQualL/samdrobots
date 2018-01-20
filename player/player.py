import Ice
Ice.loadSlice('-I. --all ./interfaces/drobots.ice')
Ice.loadSlice('-I. --all ./interfaces/services.ice')

import drobots
import services


class PlayerI(drobots.Player):
    """
    Player interface implementation
    """

    def __init__(self, container_prx):
        self.container_prx = container_prx
        self.controller_factory_prx_1 = self.__get_controller_factory_prx(1)
        self.controller_factory_prx_2 = self.__get_controller_factory_prx(2)
        self.mine_index = 0
        self.mines = [
            drobots.Point(x=100, y=100),
            drobots.Point(x=100, y=300),
            drobots.Point(x=300, y=100),
            drobots.Point(x=300, y=300),
        ]


    def makeController(self, bot, current=None):
        if self.controller_factory_prx_1.amountCreated() < 2:
            controller = self.controller_factory_prx_1.makeController(bot)
        else:
            controller = self.controller_factory_prx_2.makeController(bot)

        return controller

    def makeDetectorController(self, current):
        return self.controller_factory_prx_1.makeDetectorController()

    def getMinePosition(self, current):
        """
        Pending implementation:
         Point getMinePosition();
        """
        pos = self.mines[self.mine_index]
        self.mine_index += 1
        return pos

    def win(self, current=None):
        """
        Received when we win the match
        """
        print("You win")
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        """
        Received when we lose the match
        """
        print("You lose :-(")
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current=None):
        """
        Received when the match is aborted (when there are not enough players
        to start a game, for example)
        """
        print("The game was aborted")
        current.adapter.getCommunicator().shutdown()

    def __get_controller_factory_prx(self, n):
        container_list = self.container_prx.list()
        controller_factory_prx = container_list["controller_factory_{0}".format(n)]
        controller_factory_prx = services.ControllerFactoryPrx.checkedCast(controller_factory_prx)

        return controller_factory_prx
