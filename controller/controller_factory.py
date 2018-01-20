import Ice
Ice.loadSlice('-I. --all ./interfaces/services.ice')
import random
import math
import drobots
import services

class ControllerFactoryI(services.ControllerFactory):
    """
    ControllerFactory interface implementation
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

    def make(self, bot, current=None):
        self.mines = [
            drobots.Point(x=100, y=100),
            drobots.Point(x=100, y=300),
            drobots.Point(x=300, y=100),
            drobots.Point(x=300, y=300),
        ]

        """
        makeController is invoked by the game server. The method receives a
        "bot", instance of RobotPrx.

        It is mandatory to return a direct proxy, in case that you are using
        IceGrid
        """

        print("Make controller received bot {}".format(bot))
        if bot.ice_isA("::drobots::Attacker"):
            controller = RobotControllerAttacker(bot, self.mines)
            object_prx = current.adapter.addWithUUID(controller)
            controller_prx = drobots.RobotControllerPrx.checkedCast(object_prx)

        elif(bot.ice_isA("::drobots::Defender")):
            controller = RobotControllerDefender(bot, self.mines)
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

class RobotControllerAttacker(drobots.RobotController):
    """
    RobotController interface implementation.

    The implementation only retrieve and print the location of the assigned
    robot
    """
    def __init__(self, bot, mines):
        """
        ControllerI constructor. Accepts only a "bot" argument, that should be
        a RobotPrx object, usually sent by the game server.
        """
        print("CREADO ROBOT ATTACKER")
        self.turno = 0
        self.bot = bot
        self.mines = mines

    def turn(self, current):
        """
        Method that will be invoked remotely by the server. In this method we
        should communicate with out Robot
        """
        self.turno += 1


        print("*****************************")
        print("******TURNO "+str(self.turno) +" ATTACKER******")
        print("****************************")

        location = self.bot.location()
        print("Posicion: X = {}, Y = {}".format(location.x, location.y))


    def robotDestroyed(self, current):
        """
        Pending implementation:
        void robotDestroyed();
        """
        pass


class RobotControllerDefender(drobots.RobotController):
    """
    RobotController interface implementation.

    The implementation only retrieve and print the location of the assigned
    robot
    """
    def __init__(self, bot, mines):
        """
        ControllerI constructor. Accepts only a "bot" argument, that should be
        a RobotPrx object, usually sent by the game server.
        """
        print("CREADO ROBOT DEFENDER")
        self.bot = bot
        self.mines = mines
        self.turno = 0





    def turn(self, current):
        """
        Method that will be invoked remotely by the server. In this method we
        should communicate with out Robot
        """
        print("*****************************")
        print("******TURNO "+str(self.turno) +" DEFENDER******")
        print("****************************")


        

        location = self.bot.location()
        print("Posicion: X = {}, Y = {}".format(location.x, location.y))

        
        self.angulo = random.randint(0,359)
        if(self.bot.energy()>10):
            self.escanear()
        if(self.bot.energy()>60):
            self.move(location)

        print("*********FIN TURNO "+str(self.turno) + " DEFENDER*********")
        self.turno+=1

    def move(self, location):
        location=self.bot.location();
        
        if(location.x>390 and location.y<10):
            self.bot.drive(225,100)
            print("Se supone que me muevo con angulo: 225 velocidad: 100")
        elif(location.x<10 and location.y<10):
            self.bot.drive(315,100)
            print("Se supone que me muevo con angulo: 315 velocidad: 100")
        elif(location.y>390 and location.x<10):
            self.bot.drive(45,100)
            print("Se supone que me muevo con angulo: 45 velocidad: 100")
        elif(location.y>390 and location.x>390):
            self.bot.drive(135,100)
            print("Se supone que me muevo con angulo: 135 velocidad: 100")
        else:
            self.bot.drive(random.randint(0,360),100)
            print("Se supone que me muevo con angulo: random velocidad: 100")


    def escanear(self):
        angulo = random.randint(0,360)
        enemies = self.bot.scan(angulo,20)

        if enemies != 0:
            print("He encontrado enemigos, me vuevo en direccion contraria")
            if (angulo >= 180):
                angulo -=180
            else:
                angulo+=180

            self.bot.drive(angulo,100)


    def robotDestroyed(self, current):
        """
        Pending implementation:
        void robotDestroyed();
        """
        print("El robot ha muerto")
        pass



class DetectorControllerI(drobots.DetectorController):
    """
    DetectorController interface implementation.

    It implements the alert method.

    Remember: every alert call will include de position, so there is no need
    to create a DetectorControllerI servant for every detector, you can re-use
    the same servant (and its proxy) to every "makeDetectorController" petition
    on the PlayerI
    """
    def alert(self, pos, robots_detected, current):
        """
        Method that receives a Point with the coordinates where the detector is
        placed and the number of robots around it. This method is only invoked
        when at least 1 robot is near to the detector. If there is no robots
        around it, this method will never be called.
        """
        print("Alert: {} robots detected at {},{}".format(
            robots_detected, pos.x, pos.y))
