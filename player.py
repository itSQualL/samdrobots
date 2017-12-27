import Ice

Ice.loadSlice('drobots.ice')
import drobots

from controller import ControllerI, DetectorControllerI

class PlayerI(drobots.Player):
    """
    Player interface implementation.

    It responds correctly to makeController, win, lose or gameAbort.
    """
    def __init__(self):
        self.detector_controller = None
        self.mine_index = 0
        self.mines = [
            drobots.Point(x=100, y=100),
            drobots.Point(x=100, y=300),
            drobots.Point(x=300, y=100),
            drobots.Point(x=300, y=300),
        ]

    def makeController(self, bot, current):
        """
        makeController is invoked by the game server. The method receives a
        "bot", instance of RobotPrx.

        It is mandatory to return a direct proxy, in case that you are using
        IceGrid
        """

        print("Make controller received bot {}".format(bot))
        controller = ControllerI(bot, self.mines)
        object_prx = current.adapter.addWithUUID(controller)
        controller_prx = drobots.RobotControllerPrx.checkedCast(object_prx)
        return controller_prx

    def makeDetectorController(self, current):
        """
        Pending implementation:
        DetectorController* makeDetectorController();
        """
        print("Make detector controller.")

        if self.detector_controller is not None:
            return self.detector_controller

        controller = DetectorControllerI()
        object_prx = current.adapter.addWithUUID(controller)
        self.detector_controller = \
            drobots.DetectorControllerPrx.checkedCast(object_prx)
        return self.detector_controller

    def getMinePosition(self, current):
        """
        Pending implementation:
         Point getMinePosition();
        """
        pos = self.mines[self.mine_index]
        self.mine_index += 1
        return pos

    def win(self, current):
        """
        Received when we win the match
        """
        print("You win")
        current.adapter.getCommunicator().shutdown()

    def lose(self, current):
        """
        Received when we lose the match
        """
        print("You lose :-(")
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current):
        """
        Received when the match is aborted (when there are not enough players
        to start a game, for example)
        """
        print("The game was aborted")
        current.adapter.getCommunicator().shutdown()
