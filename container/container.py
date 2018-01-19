import Ice
Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all services.ice')

import services

class ContainerI(services.Container):
    """
    Container interface implementation
    """

    def __init__(self):
        self.game_prxs = dict()

    def link(self, key, proxy, current=None):
        """
        link adds a new entry to the game_prxs dict.
        If it already exists, it will throw an AlreadyExists exception
        """
        if key in self.game_prxs: raise services.AlreadyExists(key)

        self.game_prxs[key] = proxy
        print("link: {0} -> {1}".format(key, proxy))

    def unlink(self, key, current=None):
        """
        unlink removes from game_prxs dict an existing key.
        If it doesn't have the passed key, it will throw an NoSuchKey exception
        """
        if not key in self.game_prxs: raise services.NoSuchKey(key)

        del(self.game_prxs[key])
        print("unlink: {0}".format(key))

    def list(self, current=None):
        """
        list all the keys for game_prxs
        """
        return self.game_prxs
