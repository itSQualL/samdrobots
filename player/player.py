import Ice
Ice.loadSlice('-I. --all ../interfaces/drobots.ice')

import drobots


class PlayerI(drobots.Player):
    """
    Player interface implementation
    """

    def __init__(self, controller_factory_prx):
        self.controller_factory_prx = controller_factory_prx
        self.detector_controller = None
        self.mine_index = 0
        self.mines = [
            drobots.Point(x=100, y=100),
            drobots.Point(x=100, y=300),
            drobots.Point(x=300, y=100),
            drobots.Point(x=300, y=300),
        ]

    def makeController(self, bot, current=None):
        return self.controller_factory_prx.make(bot)

    def makeDetectorController(self, current):
        return self.controller_factory_prx.makeDetectorController()

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
