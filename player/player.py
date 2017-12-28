import Ice

Ice.loadSlice('drobots.ice')
import drobots

class PlayerI(drobots.Player):
    """
    Player interface implementation
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





